"""Advanced filters."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from django import template
from django.urls import reverse

from utilities.utils import get_viewname

register = template.Library()


@register.inclusion_tag("fwadmin/buttons/approve.html")
def approve_button(instance):
    """Add approve button.

    Used in templates/fwadmin.
    """
    viewname = get_viewname(instance, "manage")
    url = reverse(viewname, kwargs={"pk": instance.pk})

    return {
        "url": url,
    }


@register.inclusion_tag("fwadmin/buttons/reject.html")
def reject_button(instance):
    """Add reject button.

    Used in templates/fwadmin.
    """
    viewname = get_viewname(instance, "manage")
    url = reverse(viewname, kwargs={"pk": instance.pk})

    return {
        "url": url,
    }


@register.inclusion_tag("fwadmin/buttons/self_approve.html")
def self_approve_button(instance):
    """Add self_approve button.

    Used in templates/fwadmin.
    """
    viewname = get_viewname(instance, "manage")
    url = reverse(viewname, kwargs={"pk": instance.pk})

    return {
        "url": url,
    }
