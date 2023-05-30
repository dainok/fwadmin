"""Advanced filters."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from fwadmin.models import (
    DeviceGroup,
    DynamicList,
    Firewall,
    SessionRequest,
)


class DeviceGroupFilterSet(NetBoxModelFilterSet):
    """FilterSet used in DeviceGroupListView."""

    class Meta:
        """FilterSet metadata."""

        model = DeviceGroup
        fields = []

    def search(self, queryset, name, value):
        """Generic (quick) search."""
        return queryset.filter(
            Q(ip_address__icontains=value)
            | Q(mac_address__icontains=value)
            | Q(interface__name__icontains=value)
            | Q(interface__device__name__icontains=value)
            | Q(vendor__icontains=value)
        )


class DynamicListFilterSet(NetBoxModelFilterSet):
    """FilterSet used in DynamicListListView."""

    class Meta:
        """FilterSet metadata."""

        model = DynamicList
        fields = []

    def search(self, queryset, name, value):
        """Generic (quick) search."""
        return queryset.filter(
            Q(ip_address__icontains=value)
            | Q(mac_address__icontains=value)
            | Q(interface__name__icontains=value)
            | Q(interface__device__name__icontains=value)
            | Q(vendor__icontains=value)
        )


class FirewallFilterSet(NetBoxModelFilterSet):
    """FilterSet used in FirewallListView."""

    class Meta:
        """FilterSet metadata."""

        model = Firewall
        fields = []

    def search(self, queryset, name, value):
        """Generic (quick) search."""
        return queryset.filter(
            Q(ip_address__icontains=value)
            | Q(mac_address__icontains=value)
            | Q(interface__name__icontains=value)
            | Q(interface__device__name__icontains=value)
            | Q(vendor__icontains=value)
        )


class SessionRequestFilterSet(NetBoxModelFilterSet):
    """FilterSet used in SessionRequestListView."""

    class Meta:
        """FilterSet metadata."""

        model = SessionRequest
        fields = []

    def search(self, queryset, name, value):
        """Generic (quick) search."""
        return queryset.filter(
            Q(ip_address__icontains=value)
            | Q(mac_address__icontains=value)
            | Q(interface__name__icontains=value)
            | Q(interface__device__name__icontains=value)
            | Q(vendor__icontains=value)
        )
