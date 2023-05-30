"""Models (ORM).

Define ORM models for FWAdmin objects:
* A Discoverable is a device willed to be discovered using a specific mode.
* Credential is associated to one or more Discoverables.
* A DiscoveryLog is the output for a specific discovery command executed in a Discoverable.
"""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from utilities.choices import ChoiceSet
from netbox.models import NetBoxModel


class SessionRequestStatusChoices(ChoiceSet):
    """SessionRequest status."""

    CHOICES = [
        ("requested", "Requested"),
        ("approved", "Approved"),
        ("self_approved", "Self-approved"),
        ("rejected", "Rejected"),
    ]


class FirewallChoices(ChoiceSet):
    """Supported firewalls."""

    CHOICES = [
        ("paloalto-panos", "Palo Alto Networks NGFW"),
    ]


#
# DeviceGroup model
#


class DeviceGroup(NetBoxModel):
    """
    Model for DeviceGroup.

    Administrators configured one or mode DeviceGroup objects so they can be reused with multiple
    DynamicList objects.
    """

    devices = models.ManyToManyField(
        to="dcim.Device",
        related_name="+",
        blank=True,
    )
    name = models.CharField(max_length=100, help_text="Group name")

    class Meta:
        """Database metadata."""

        ordering = ["name"]
        unique_together = ["name"]
        verbose_name = "Device group"
        verbose_name_plural = "Device groups"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return str(self.name)

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("plugins:fwadmin:devicegroup", args=[self.pk])


#
# DynamicList model
#


class DynamicList(NetBoxModel):
    """
    Model for DynamicList.

    Users can request access for one or more DynamicList. DynamicList are configured
    by administrators and referenced one or more DeviceGroup objects.
    DynamicList publish a set of IP addresses of Netbox devices associated via device groups.
    Device IP addresses are available via DynamicList if at least one SessionRequest is active.

    Protocol, port, application are configured in the firewall rule; the EDL replace the source (or
    the destination) address field. The DeviceGroup name/description should mention
    protocol/port/application thus users can select the proper ones.

    Users see DynamicList objects as connections to be requested. In fact DynamicList objects
    reference firewall rules which specify which connections can pass.
    """

    description = models.TextField(help_text="Description", default="", blank=True)
    device_groups = models.ManyToManyField(
        to="DeviceGroup",
        related_name="dynamic_lists",
        blank=True,
    )
    name = models.CharField(max_length=100, help_text="List name")
    slug = models.UUIDField(
        default=uuid.uuid4, editable=False
    )  # The UUID componing the EDL url
    # Needed to drop connections
    firewalls = models.ManyToManyField(
        "Firewall", related_name="dynamic_lists"
    )  # The firewalls referencing this rule
    rule = models.CharField(
        max_length=100, help_text="Rule name or ID"
    )  # The rule name defined in the firewalls

    class Meta:
        """Database metadata."""

        ordering = ["name"]
        unique_together = [["name"], ["slug"]]
        verbose_name = "Dynamic list"
        verbose_name_plural = "Dynamic lists"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return str(self.name)

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("plugins:fwadmin:dynamiclist", args=[self.pk])


#
# Firewall model
#


class Firewall(NetBoxModel):
    """
    Model for Firewall.

    Firewalls are configured by administrators and referenced by cleaning scripts. Cleaning is
    necessary to drop active connections after IP addresses are removed from DynamicList
    objects. Firewall operations require administrative access.
    """

    name = models.CharField(max_length=100, help_text="Firewall name")
    address = models.CharField(
        max_length=100, help_text="Management FQDN or IP address"
    )
    model = models.CharField(
        max_length=100, choices=FirewallChoices, default="paloalto-panos"
    )
    secret_key = models.CharField(max_length=200, help_text="Password or secret token")
    verify_cert = models.BooleanField(
        default=True, help_text="Validate firewall's certificate"
    )

    class Meta:
        """Database metadata."""

        ordering = ["name"]
        unique_together = [["name"], ["address"]]
        verbose_name = "Firewall"
        verbose_name_plural = "Firewalls"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return str(self.name)

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("plugins:fwadmin:firewall", args=[self.pk])


#
# SessionRequest model
#


class SessionRequest(NetBoxModel):
    """
    SessionRequest model.

    SessionRequest objects can be requested by users for a specific time frame.
    SessionRequest objects can also be permanent or recurrent.
    SessionRequest objects are associated to hardcoded workflows.

    Approved SessionRequest populates the EDLs.
    """

    dynamic_lists = models.ManyToManyField(
        "DynamicList", related_name="requests", help_text="Select required connections"
    )
    cleared = models.BooleanField(
        default=False, help_text="Cleared", editable=False
    )  # The connection has been cleared by the script
    end_at = models.DateTimeField(help_text="Closes at")
    request_reason = models.TextField(help_text="Request reason")
    start_at = models.DateTimeField(help_text="Starts at")
    status = models.CharField(
        max_length=100,
        choices=SessionRequestStatusChoices,
        default="requested",
        editable=False,
    )
    requested_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, editable=False, related_name="+"
    )
    managed_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, editable=False, related_name="+"
    )

    class Meta:
        """Database metadata."""

        ordering = ["-end_at"]
        unique_together = []
        verbose_name = "Session request"
        verbose_name_plural = "Session requests"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return str(self.pk)

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("plugins:fwadmin:sessionrequest", args=[self.pk])
