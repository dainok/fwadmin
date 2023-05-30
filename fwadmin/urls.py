"""URLs."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from fwadmin import models, views


urlpatterns = (
    #
    # DeviceGroup urls
    #
    path("devicegroup/", views.DeviceGroupListView.as_view(), name="devicegroup_list"),
    path(
        "devicegroup/add/", views.DeviceGroupEditView.as_view(), name="devicegroup_add"
    ),
    path(
        "devicegroup/delete/",
        views.DeviceGroupBulkDeleteView.as_view(),
        name="devicegroup_bulk_delete",
    ),
    path("devicegroup/<int:pk>/", views.DeviceGroupView.as_view(), name="devicegroup"),
    path(
        "devicegroup/<int:pk>/edit/",
        views.DeviceGroupEditView.as_view(),
        name="devicegroup_edit",
    ),
    path(
        "devicegroup/<int:pk>/delete/",
        views.DeviceGroupDeleteView.as_view(),
        name="devicegroup_delete",
    ),
    path(
        "devicegroup/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="devicegroup_changelog",
        kwargs={"model": models.DeviceGroup},
    ),
    #
    # DynamicList urls
    #
    path("dynamiclist/", views.DynamicListListView.as_view(), name="dynamiclist_list"),
    path(
        "dynamiclist/add/", views.DynamicListEditView.as_view(), name="dynamiclist_add"
    ),
    path(
        "dynamiclist/text/<slug:slug>/",
        views.DynamicListText.as_view(),
        name="dynamiclist_text",
    ),
    path(
        "dynamiclist/delete/",
        views.DynamicListBulkDeleteView.as_view(),
        name="dynamiclist_bulk_delete",
    ),
    path("dynamiclist/<int:pk>/", views.DynamicListView.as_view(), name="dynamiclist"),
    path(
        "dynamiclist/<int:pk>/edit/",
        views.DynamicListEditView.as_view(),
        name="dynamiclist_edit",
    ),
    path(
        "dynamiclist/<int:pk>/delete/",
        views.DynamicListDeleteView.as_view(),
        name="dynamiclist_delete",
    ),
    path(
        "dynamiclist/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="dynamiclist_changelog",
        kwargs={"model": models.DynamicList},
    ),
    #
    # Firewall urls
    #
    path("firewall/", views.FirewallListView.as_view(), name="firewall_list"),
    path("firewall/add/", views.FirewallEditView.as_view(), name="firewall_add"),
    path(
        "firewall/delete/",
        views.FirewallBulkDeleteView.as_view(),
        name="firewall_bulk_delete",
    ),
    path("firewall/<int:pk>/", views.FirewallView.as_view(), name="firewall"),
    path(
        "firewall/<int:pk>/edit/",
        views.FirewallEditView.as_view(),
        name="firewall_edit",
    ),
    path(
        "firewall/<int:pk>/delete/",
        views.FirewallDeleteView.as_view(),
        name="firewall_delete",
    ),
    path(
        "firewall/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="firewall_changelog",
        kwargs={"model": models.Firewall},
    ),
    #
    # SessionRequest urls
    #
    path(
        "sessionrequest/",
        views.SessionRequestListView.as_view(),
        name="sessionrequest_list",
    ),
    path(
        "sessionrequest/add/",
        views.SessionRequestAddView.as_view(),
        name="sessionrequest_add",
    ),
    path(
        "sessionrequest/manage/",
        views.SessionRequestBulkManageView.as_view(),
        name="sessionrequest_bulk_manage",
    ),
    path(
        "sessionrequest/<int:pk>/",
        views.SessionRequestView.as_view(),
        name="sessionrequest",
    ),
    path(
        "sessionrequest/<int:pk>/manage/",
        views.SessionRequestManageView.as_view(),
        name="sessionrequest_manage",
    ),
    path(
        "sessionrequest/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="sessionrequest_changelog",
        kwargs={"model": models.SessionRequest},
    ),
)
