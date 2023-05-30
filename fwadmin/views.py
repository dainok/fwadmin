"""Views, called by URLs."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

import logging

from django.db.models import Count, Q, BooleanField, ExpressionWrapper
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound

from ipam.models import IPAddress
from netbox.views import generic
from dcim.tables.devices import DeviceTable
from utilities.forms import ConfirmationForm
from utilities.htmx import is_htmx
from utilities.permissions import get_permission_for_model
from utilities.utils import get_viewname

from fwadmin import models, tables, forms, filtersets, workflows


#
# DeviceGroup views
#


class DeviceGroupListView(generic.ObjectListView):
    """Summary view listing all DeviceGroup objects."""

    queryset = models.DeviceGroup.objects.annotate(
        device_count=Count("devices")
    ).order_by("name")
    table = tables.DeviceGroupTable
    filterset = filtersets.DeviceGroupFilterSet


class DeviceGroupView(generic.ObjectView):
    """Detailed DeviceGroup view."""

    queryset = models.DeviceGroup.objects.annotate(device_count=Count("devices"))

    def get_extra_context(self, request, instance):
        """Get associated Device objects."""
        table = DeviceTable(instance.devices.all().order_by("name"))
        table.configure(request)

        return {
            "device_table": table,
        }


class DeviceGroupEditView(generic.ObjectEditView):
    """Edit DeviceGroup view."""

    queryset = models.DeviceGroup.objects.all()
    form = forms.DeviceGroupForm


class DeviceGroupDeleteView(generic.ObjectDeleteView):
    """Delete DeviceGroup view."""

    queryset = models.DeviceGroup.objects.all()
    default_return_url = "plugins:fwadmin:devicegroup_list"


class DeviceGroupBulkDeleteView(generic.BulkDeleteView):
    """Bulk delete DeviceGroup view."""

    queryset = models.DeviceGroup.objects.all()
    table = tables.DeviceGroupTable
    default_return_url = "plugins:fwadmin:devicegroup_list"
    filterset = filtersets.DeviceGroupFilterSet


#
# DynamicList views
#


class DynamicListListView(generic.ObjectListView):
    """Summary view listing all DynamicList objects."""

    queryset = models.DynamicList.objects.annotate(
        device_count=Count("device_groups__devices")
    ).order_by("name")
    table = tables.DynamicListTable
    filterset = filtersets.DynamicListFilterSet


class DynamicListView(generic.ObjectView):
    """Detailed DynamicList view."""

    queryset = models.DynamicList.objects.annotate(
        device_count=Count("device_groups__devices")
    )

    def get_extra_context(self, request, instance):
        """Get associated Firewall objects."""
        firewall_table = tables.FirewallTable(instance.firewalls.all().order_by("name"))
        firewall_table.configure(request)
        devicegroup_table = tables.DeviceGroupTable(
            instance.device_groups.all().order_by("name")
        )
        devicegroup_table.configure(request)

        return {
            "firewall_table": firewall_table,
            "devicegroup_table": devicegroup_table,
        }


class DynamicListEditView(generic.ObjectEditView):
    """Edit DynamicList view."""

    queryset = models.DynamicList.objects.all()
    form = forms.DynamicListForm


class DynamicListDeleteView(generic.ObjectDeleteView):
    """Delete DynamicList view."""

    queryset = models.DynamicList.objects.all()
    default_return_url = "plugins:fwadmin:dynamiclist_list"


class DynamicListBulkDeleteView(generic.BulkDeleteView):
    """Bulk delete DynamicList view."""

    queryset = models.DynamicList.objects.all()
    table = tables.DynamicListTable
    default_return_url = "plugins:fwadmin:dynamiclist_list"
    filterset = filtersets.DynamicListFilterSet


class DynamicListText(View):
    """Print the content of the EDL in text format."""

    def get(self, request, slug=None):  # pylint: disable=unused-argument
        """Get the content of the list in text/plain format."""
        ip_list = []
        now = timezone.now()

        # Load the list
        try:
            dynamiclist_o = models.DynamicList.objects.get(slug=slug)
        except models.DynamicList.DoesNotExist:  # pylint: disable=no-member
            # List not found
            return HttpResponseNotFound()

        # Get all session requests attached to this list with active sessions
        sessionrequest_qs = models.SessionRequest.objects.filter(
            dynamic_lists=dynamiclist_o,
            start_at__lt=now,
            end_at__gt=now,
            status__contains="approved",
        )
        if sessionrequest_qs:
            # Found at least one session request
            # Get Interface IDs
            interface_ids = list(
                dynamiclist_o.device_groups.values_list(
                    "devices__interfaces__pk", flat=True
                )
            )
            ip_list = [
                f"{ipaddress_o.ip}/32"
                for ipaddress_o in IPAddress.objects.filter(
                    interface__in=interface_ids
                ).values_list("address", flat=True)
            ]

        if not ip_list:
            # Empty IP list
            ip_list = ["0.0.0.0/32"]

        ip_list.sort()
        return HttpResponse("\n".join(ip_list), content_type="text/plain")


#
# Firewall views
#


class FirewallListView(generic.ObjectListView):
    """Summary view listing all Firewall objects."""

    queryset = models.Firewall.objects.annotate(
        dynamiclist_count=Count("dynamic_lists")
    ).order_by("name")
    table = tables.FirewallTable
    filterset = filtersets.FirewallFilterSet


class FirewallView(generic.ObjectView):
    """Detailed Firewall view."""

    queryset = models.Firewall.objects.annotate(
        dynamiclist_count=Count("dynamic_lists")
    )

    def get_extra_context(self, request, instance):
        """Get associated DynamicList objects."""
        table = tables.DynamicListTable(instance.dynamic_lists.all().order_by("name"))
        table.configure(request)

        return {
            "dynamiclist_table": table,
        }


class FirewallEditView(generic.ObjectEditView):
    """Edit Firewall view."""

    queryset = models.Firewall.objects.all()
    form = forms.FirewallForm


class FirewallDeleteView(generic.ObjectDeleteView):
    """Delete Firewall view."""

    queryset = models.Firewall.objects.all()
    default_return_url = "plugins:fwadmin:firewall_list"


class FirewallBulkDeleteView(generic.BulkDeleteView):
    """Bulk delete Firewall view."""

    queryset = models.Firewall.objects.all()
    table = tables.FirewallTable
    default_return_url = "plugins:fwadmin:firewall_list"
    filterset = filtersets.FirewallFilterSet


#
# SessionRequest views
#


class SessionRequestListView(generic.ObjectListView):
    """Summary view listing all SessionRequest objects."""

    queryset = models.SessionRequest.objects.annotate(
        is_active=ExpressionWrapper(
            Q(end_at__gt=timezone.now()), output_field=BooleanField()
        )
    ).order_by("-id")
    table = tables.SessionRequestTable
    filterset = filtersets.SessionRequestFilterSet
    template_name = "fwadmin/sessionrequest_list.html"
    actions = [
        "add",
        "export",
        "bulk_approve",
        "bulk_selfapprove",
        "bulk_reject",
    ]

    def get_queryset(self, request):
        """Return queryset based on permissions.

        If can edit (manage), return everything.
        Else, return owned.
        """
        if request.user.has_perm("fwadmin.change_sessionrequest"):
            # Can edit (approve), return everythin
            return self.queryset.order_by("-id")

        return self.queryset.filter(requested_by=request.user).order_by("-id")


class SessionRequestView(generic.ObjectView):
    """Detailed SessionRequest view."""

    queryset = models.SessionRequest.objects.all()
    actions = ["add"]

    def get_extra_context(self, request, instance):
        """Get associated DynamicList obhects."""
        table = tables.DynamicListTable(instance.dynamic_lists.all().order_by("name"))
        table.configure(request)

        return {
            "dynamiclist_table": table,
        }


class SessionRequestAddView(generic.ObjectEditView):
    """Add SessionRequest view. Edit is not used."""

    queryset = models.SessionRequest.objects.all()
    form = forms.SessionRequestForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        """Set requested_by based on request.user."""
        obj = models.SessionRequest(requested_by=request.user)
        return obj


class SessionRequestManageView(generic.ObjectDeleteView):
    """SessionRequest approval view."""

    queryset = models.SessionRequest.objects.all()
    template_name = "fwadmin/sessionrequest_manage.html"

    def get_required_permission(self):
        """Check permissions."""
        return get_permission_for_model(self.queryset.model, "view")

    #
    # Request handlers
    #

    def get(self, request, *args, **kwargs):
        """Return the confirmation page."""
        obj = self.get_object(**kwargs)
        form = ConfirmationForm(initial=request.GET)
        action = request.GET.get("action")

        # If this is an HTMX request, return only the rendered deletion form as modal content
        if is_htmx(request):
            # Called from SessionRequestView
            viewname = get_viewname(self.queryset.model, action="manage")
            form_url = reverse(viewname, kwargs={"pk": obj.pk})
            return render(
                request,
                "fwadmin/htmx/manage_form.html",
                {
                    "object": obj,
                    "object_type": self.queryset.model._meta.verbose_name,  # pylint: disable=protected-access
                    "form": form,
                    "form_url": form_url,
                    "action": action,
                    **self.get_extra_context(request, obj),
                },
            )

        # Called from DiscoverableViewList
        return render(
            request,
            self.template_name,
            {
                "object": obj,
                "form": form,
                "return_url": self.get_return_url(request, obj),
                **self.get_extra_context(request, obj),
            },
        )

    def post(self, request, *args, **kwargs):
        """Manage a single SessionRequest."""
        logger = logging.getLogger("netbox.plugins.fwadmin")
        obj = self.get_object(**kwargs)
        form = ConfirmationForm(request.POST)
        completed = False

        if form.is_valid():
            logger.debug("Form validation was successful")
            action = request.POST.get("action")

            if request.user.has_perm("fwadmin.change_sessionrequest") and action in [
                "approve",
                "reject",
            ]:
                if action == "approve" and obj.requested_by == request.user:
                    # Same user, use self_approve
                    action = "self_approve"
                # Can Approve and Reject
                try:
                    wkflow = workflows.SimpleWorkflow(obj.status)
                    obj.status = wkflow.transition(action)
                    obj.managed_by = request.user
                    obj.save()
                    completed = True
                except ValueError:
                    # Invalid state or transition
                    pass

            if (
                obj.requested_by == request.user
                and action in ["self_approve"]
                and request.user.has_perm("fwadmin.view_sessionrequest")
                and not request.user.has_perm("fwadmin.change_sessionrequest")
            ):
                # Can Self-Approve
                try:
                    wkflow = workflows.SimpleWorkflow(obj.status)
                    obj.status = wkflow.transition(action)
                    obj.managed_by = request.user
                    obj.save()
                    completed = True
                except ValueError:
                    # Invalid state or transition
                    pass

            if completed:
                return_url = form.cleaned_data.get("return_url")
                if return_url and return_url.startswith("/"):
                    return redirect(return_url)
                return redirect(self.get_return_url(request, obj))

        # Otherwise permission is denied
        messages.error(request, "Unauthorized")
        logger.debug("Form validation failed")

        return redirect(self.get_return_url(request, obj))


class SessionRequestBulkManageView(generic.BulkDeleteView):
    """SessionRequest bulk approval view."""

    template_name = "fwadmin/sessionrequest_bulk_manage.html"
    queryset = models.SessionRequest.objects.all()
    table = tables.SessionRequestTable
    default_return_url = "plugins:fwadmin:sessionrequest_list"

    def get_required_permission(self):
        """Check permissions."""
        return get_permission_for_model(self.queryset.model, "view")

    def get_queryset(self, request):
        """Return queryset based on permissions.

        If can edit (manage), return everything.
        Else, return owned.
        """
        if request.user.has_perm("fwadmin.change_sessionrequest"):
            # Can edit (approve), return everythin
            return self.queryset.order_by("-id")

        return self.queryset.filter(requested_by=request.user).order_by("-id")

    def post(self, request, **kwargs):
        """Manage SessionRequest."""
        logger = logging.getLogger("netbox.plugins.fwadmin")
        model = self.queryset.model
        action = request.POST.get("action")

        # Are we managing *all* objects in the queryset or just a selected subset?
        if request.POST.get("_all"):
            queryset = model.objects.all()
            pk_list = queryset.only("pk").values_list("pk", flat=True)
        else:
            pk_list = [int(pk) for pk in request.POST.getlist("pk")]

        form_cls = self.get_form()

        if "_confirm" in request.POST:
            form = form_cls(request.POST)
            if form.is_valid():
                logger.debug("Form validation was successful")
                queryset = self.queryset.filter(pk__in=pk_list, status="requested")

                if request.user.has_perm("fwadmin.change_sessionrequest"):
                    # Can approve and reject
                    if action == "reject":
                        # Reject
                        queryset.update(status="rejected", managed_by=request.user)
                    if action == "approve":
                        # Self-Approved
                        queryset.filter(requested_by=request.user).update(
                            status="self_approved", managed_by=request.user
                        )
                        # Approved
                        queryset.exclude(requested_by=request.user).update(
                            status="approved", managed_by=request.user
                        )

                if request.user.has_perm(
                    "fwadmin.view_sessionrequest"
                ) and not request.user.has_perm("fwadmin.view_sessionrequest"):
                    # Can self_approve
                    queryset.filter(requested_by=request.user).update(
                        status="self_approved", managed_by=request.user
                    )

                return redirect(self.get_return_url(request))

            logger.debug("Form validation failed")

        else:
            form = form_cls(
                initial={
                    "pk": pk_list,
                    "return_url": self.get_return_url(request),
                }
            )

        # Retrieve objects being deleted
        table = self.table(self.queryset.filter(pk__in=pk_list), orderable=False)
        if not table.rows:
            messages.warning(
                request,
                f"No {model._meta.verbose_name_plural} were selected.",  # pylint: disable=protected-access
            )
            return redirect(self.get_return_url(request))

        return render(
            request,
            self.template_name,
            {
                "model": model,
                "form": form,
                "table": table,
                "action": action,
                "return_url": self.get_return_url(request),
                **self.get_extra_context(request),
            },
        )
