"""Tables, called by Views."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn

from fwadmin import models


class DeviceGroupTable(NetBoxTable):
    """DeviceGroup list table used in DeviceGroupView."""

    name = tables.Column(linkify=True)
    device_count = tables.Column()

    class Meta(NetBoxTable.Meta):
        """Table metadata."""

        model = models.DeviceGroup
        fields = [
            "pk",
            "id",
            "name",
            "device_count",
            "last_updated",
            "created",
        ]
        default_columns = [
            "name",
            "device_count",
        ]


class DynamicListTable(NetBoxTable):
    """DynamicList list table used in DynamicListView."""

    name = tables.Column(linkify=True)
    device_count = tables.Column()

    class Meta(NetBoxTable.Meta):
        """Table metadata."""

        model = models.DynamicList
        fields = [
            "pk",
            "id",
            "name",
            "rule",
            "device_count",
            "last_updated",
            "created",
        ]
        default_columns = [
            "name",
            "rule",
            "device_count",
        ]


class FirewallTable(NetBoxTable):
    """Firewall list table used in FirewallView."""

    name = tables.Column(linkify=True)
    model = ChoiceFieldColumn()
    dynamiclist_count = tables.Column()

    class Meta(NetBoxTable.Meta):
        """Table metadata."""

        model = models.Firewall
        fields = [
            "pk",
            "id",
            "name",
            "address",
            "model",
            "verify_cert",
            "dynamiclist_count",
            "last_updated",
            "created",
        ]
        default_columns = [
            "name",
            "address",
            "model",
            "verify_cert",
            "dynamiclist_count",
        ]


class SessionRequestTable(NetBoxTable):
    """SessionRequest list table used in SessionRequestlView."""

    name = tables.Column(linkify=True)
    model = ChoiceFieldColumn()
    dynamiclist_count = tables.Column()
    is_active = tables.BooleanColumn()
    actions = []

    class Meta(NetBoxTable.Meta):
        """Table metadata."""

        model = models.SessionRequest
        fields = [
            "pk",
            "id",
            "requested_by",
            "managed_by",
            "status",
            "start_at",
            "end_at",
            "cleared",
            "last_updated",
            "created",
            "is_active",
            "request_reason",
        ]
        default_columns = [
            "id",
            "requested_by",
            "managed_by",
            "status",
            "start_at",
            "end_at",
            "is_active",
            "request_reason",
        ]
