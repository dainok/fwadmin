"""API URLs, called by Views, used for add/edit actions."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from netbox.api.routers import NetBoxRouter
from fwadmin.api import views


app_name = "fwadmin"  # pylint: disable=invalid-name

router = NetBoxRouter()
router.register("devicegroup", views.DeviceGroupViewSet)
router.register("dynamiclist", views.DynamicListViewSet)
router.register("firewall", views.FirewalliewSet)
router.register("sessionrequest", views.SessionRequestiewSet)

urlpatterns = router.urls
