"""Sidebar navigation buttons."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from extras.plugins import PluginMenuButton, PluginMenuItem, PluginMenu
from utilities.choices import ButtonColorChoices

devicegroup_buttons = [
    PluginMenuButton(
        link="plugins:fwadmin:devicegroup_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
        permissions=["fwadmin.add_devicegroup"],
    ),
]

dynamiclist_buttons = [
    PluginMenuButton(
        link="plugins:fwadmin:dynamiclist_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
        permissions=["fwadmin.add_dynamiclist"],
    ),
]

firewall_buttons = [
    PluginMenuButton(
        link="plugins:fwadmin:firewall_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
        permissions=["fwadmin.add_firewall"],
    ),
]

sessionrequest_buttons = [
    PluginMenuButton(
        link="plugins:fwadmin:sessionrequest_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        color=ButtonColorChoices.GREEN,
        permissions=["fwadmin.add_sessionrequest"],
    ),
]

menu_edl = (
    PluginMenuItem(
        link="plugins:fwadmin:devicegroup_list",
        link_text="Device groups",
        buttons=devicegroup_buttons,
        permissions=["fwadmin.view_devicegroup"],
    ),
    PluginMenuItem(
        link="plugins:fwadmin:dynamiclist_list",
        link_text="Dynamic lists",
        buttons=dynamiclist_buttons,
        permissions=["fwadmin.view_dynamiclist"],
    ),
    PluginMenuItem(
        link="plugins:fwadmin:sessionrequest_list",
        link_text="Session requests",
        buttons=sessionrequest_buttons,
        permissions=["fwadmin.view_sessionrequest"],
    ),
)

menu = PluginMenu(
    label="FWAdmin",
    groups=(
        (
            "Firewalls",
            (
                PluginMenuItem(
                    link="plugins:fwadmin:firewall_list",
                    link_text="Firewalls",
                    buttons=firewall_buttons,
                    permissions=["fwadmin.view_firewall"],
                ),
            ),
        ),
        ("EDL", menu_edl),
    ),
)
