"""API View, called by API URLs."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from netbox.api.viewsets import NetBoxModelViewSet

from fwadmin import models
from fwadmin.api.serializers import (
    DeviceGroupSerializer,
    DynamicListSerializer,
    FirewallSerializer,
    SessionRequestSerializer,
)


class DeviceGroupViewSet(NetBoxModelViewSet):
    """API View for add/edit Credential."""

    queryset = models.DeviceGroup.objects.prefetch_related("tags")
    serializer_class = DeviceGroupSerializer


class DynamicListViewSet(NetBoxModelViewSet):
    """API View for add/edit Diagram."""

    queryset = models.DynamicList.objects.prefetch_related("tags")
    serializer_class = DynamicListSerializer


class FirewalliewSet(NetBoxModelViewSet):
    """API View for add/edit Firewall."""

    queryset = models.Firewall.objects.prefetch_related("tags")
    serializer_class = FirewallSerializer


class SessionRequestiewSet(NetBoxModelViewSet):
    """API View for add/edit DiscoveryLog."""

    queryset = models.SessionRequest.objects.prefetch_related("tags")
    serializer_class = SessionRequestSerializer
