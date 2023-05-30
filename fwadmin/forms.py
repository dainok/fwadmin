"""Forms, called by Views."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from datetime import timedelta

from django import forms
from django.utils import timezone

from dcim.models import Device

from utilities.forms import DynamicModelMultipleChoiceField, DateTimePicker
from netbox.forms import NetBoxModelForm


from fwadmin.models import (
    DeviceGroup,
    DynamicList,
    Firewall,
    SessionRequest,
    FirewallChoices,
)

TMZ = str(timezone.get_current_timezone())

#
# DeviceGroup forms
#


class DeviceGroupForm(NetBoxModelForm):
    """Form used to add/edit DeviceGroup."""

    name = forms.CharField(help_text="Device group name", required=True)
    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(), required=False
    )

    class Meta:
        """Form metadata."""

        model = DeviceGroup
        fields = [
            "name",
            "devices",
            "tags",
        ]


class DynamicListForm(NetBoxModelForm):
    """Form used to add/edit DynamicList."""

    name = forms.CharField()
    description = forms.Textarea()
    device_groups = DynamicModelMultipleChoiceField(
        queryset=DeviceGroup.objects.all(), required=False
    )
    firewalls = DynamicModelMultipleChoiceField(queryset=Firewall.objects.all())
    rule = forms.CharField(required=True)

    class Meta:
        """Form metadata."""

        model = DynamicList
        fields = [
            "name",
            "description",
            "device_groups",
            "firewalls",
            "rule",
            "tags",
        ]


class FirewallForm(NetBoxModelForm):
    """Form used to add/edit Firewall."""

    name = forms.CharField()
    address = forms.CharField(help_text="IP address or FQDN used to connect to")
    model = forms.ChoiceField(choices=FirewallChoices)
    secret_key = forms.CharField(
        widget=forms.PasswordInput, help_text="Password or secret key"
    )

    class Meta:
        """Form metadata."""

        model = Firewall
        fields = [
            "name",
            "address",
            "model",
            "secret_key",
            "verify_cert",
            "tags",
        ]


class SessionRequestForm(NetBoxModelForm):
    """Form used to add SessionRequest."""

    request_reason = forms.Textarea(attrs={"rows": "5"})
    dynamic_lists = DynamicModelMultipleChoiceField(
        queryset=DynamicList.objects.all(),
        required=True,
        help_text="Select connecitons you want to enable",
    )
    start_at = forms.DateTimeField(
        widget=DateTimePicker(), help_text=f"Insert start date/time in {TMZ} timezone"
    )
    end_at = forms.DateTimeField(
        widget=DateTimePicker(), help_text=f"Insert end date/time in {TMZ} timezone"
    )

    class Meta:
        """Form metadata."""

        model = SessionRequest
        fields = [
            "dynamic_lists",
            "request_reason",
            "start_at",
            "end_at",
        ]

    def clean_start_at(self):
        """Check that start_at is now or in the future.

        Check also end_at. It could be invokated before or after clean_end_at.
        """
        start_date = self.cleaned_data.get("start_at")
        end_date = self.cleaned_data.get("end_at")

        if start_date <= timezone.now() - timedelta(hours=1):
            raise forms.ValidationError("Start date cannot be in the past.")

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("Start date must be before end date.")

        return start_date

    def clean_end_at(self):
        """Check that end_at is after start_at.

        It could be invokated before or after clean_end_at.
        """
        start_date = self.cleaned_data.get("start_at")
        end_date = self.cleaned_data.get("end_at")

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("Start date must be before end date.")

        return end_date
