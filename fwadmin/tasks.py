"""Tasks executed via Netbox scripts or manually."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from datetime import timedelta
import requests

from django.conf import settings
from django.utils import timezone

from fwadmin import models

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get("fwadmin", {})


def get_expired_items():
    """
    Return EDLs and sessions to be cleared because of expired non-cleared sessions.

    Expired means end_time + Firewall_Update_interval < now.
    """
    dynamiclists_to_be_cleared_ids = []

    # Shift now and consider firewall update interval
    now = timezone.now() - timedelta(seconds=PLUGIN_SETTINGS.get("EDL_UPDATE_INTERVAL"))

    # Clear rejected sessions
    models.SessionRequest.objects.filter(
        status__contains="rejected", cleared=False
    ).exclude(end_at__gt=now).update(cleared=True)

    # Get EDLs with uncleared sessions excluding the ones with active sessions
    for dynamiclists_to_be_cleared_o in models.DynamicList.objects.filter(
        requests__cleared=False, requests__end_at__lt=now
    ):
        activesessions_qs = dynamiclists_to_be_cleared_o.requests.filter(
            start_at__lt=now,
            end_at__gt=now,
            status__contains="approved",
        )
        if not activesessions_qs:
            # There is no active session, the EDL can be cleared
            dynamiclists_to_be_cleared_ids.append(dynamiclists_to_be_cleared_o.id)

    dynamiclists_to_be_cleared_qs = models.DynamicList.objects.filter(
        id__in=dynamiclists_to_be_cleared_ids
    )

    # Get uncleared sessions
    uncleared_sessionrequests_qs = models.SessionRequest.objects.filter(
        status__contains="approved", cleared=False, end_at__lt=now
    )

    return dynamiclists_to_be_cleared_qs, uncleared_sessionrequests_qs


def terminate_sessions(script_handler=None):
    """Terminate expired sessions acting on firewalls."""
    # Get expired items
    (
        dynamiclists_to_be_cleared_qs,
        uncleared_sessionrequests_qs,
    ) = get_expired_items()

    if script_handler:
        script_handler.log_info(
            f"{len(uncleared_sessionrequests_qs)} sessions to be cleared"
            + f" referencing {len(dynamiclists_to_be_cleared_qs)} EDLs"
        )

    for dynamiclist_to_be_cleared_o in dynamiclists_to_be_cleared_qs:
        # Clear EDLs on each associated firewall
        for firewall_o in dynamiclist_to_be_cleared_o.firewalls.all():
            if script_handler:
                script_handler.log_info(
                    "Clearing session using rule "
                    + dynamiclist_to_be_cleared_o.rule
                    + f" in firewall {firewall_o.name} ({firewall_o.model})"
                )

            if firewall_o.model == "paloalto-panos":
                url = (
                    f"https://{firewall_o.address}/api/?type=op&cmd=<clear><session>"
                    + "<all><filter>"
                    + f"<rule>{dynamiclist_to_be_cleared_o.rule}</rule>"
                    + "</filter></all>"
                    + f"</session></clear>&key={firewall_o.secret_key}"
                )
                req = requests.get(url, verify=firewall_o.verify_cert, timeout=15)
                if req.status_code != 200:
                    if script_handler:
                        script_handler.log_error(
                            "Failed to clear session " + dynamiclist_to_be_cleared_o.id
                        )
                        return req.text

                # EDL has been cleared
                script_handler.log_info(
                    f"Cleared EDL {dynamiclist_to_be_cleared_o.name} on {firewall_o.name}"
                )
            else:
                raise ValueError(f"Unsupported firewall model {firewall_o.model }")

    # Everything is fine, mark sessions as cleared
    uncleared_sessionrequests_qs.update(cleared=True)

    return ""
