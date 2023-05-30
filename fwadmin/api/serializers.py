"""Serializers, called by API Views for add/ediit actions."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer

from fwadmin.models import (
    DeviceGroup,
    DynamicList,
    Firewall,
    SessionRequest,
)


class DeviceGroupSerializer(NetBoxModelSerializer):
    """Serializer to validate DeviceGroup data."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:fwadmin-api:devicegroup-detail"
    )
    device_count = serializers.IntegerField(read_only=True)

    class Meta:
        """Serializer metadata."""

        model = DeviceGroup
        fields = "__all__"


class DynamicListSerializer(NetBoxModelSerializer):
    """Serializer to validate Diagram data."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:fwadmin-api:dynamiclist-detail"
    )
    device_count = serializers.IntegerField(read_only=True)

    class Meta:
        """Serializer metadata."""

        model = DynamicList
        fields = "__all__"


class FirewallSerializer(NetBoxModelSerializer):
    """Serializer to validate FirewallSerializer data."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:fwadmin-api:firewall-detail"
    )
    dynamiclist_count = serializers.IntegerField(read_only=True)

    class Meta:
        """Serializer metadata."""

        model = Firewall
        fields = "__all__"


class SessionRequestSerializer(NetBoxModelSerializer):
    """Serializer to validate SessionRequest data."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:fwadmin-api:sessionrequest-detail"
    )

    class Meta:
        """Serializer metadata."""

        model = SessionRequest
        fields = "__all__"
