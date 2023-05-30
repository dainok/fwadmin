"""Main class."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

import os
import pkgutil
import shutil

from django.conf import settings

from extras.plugins import PluginConfig


PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get("fwadmin", {})


class FWAdminConfig(PluginConfig):
    """Configuration class."""

    name = "fwadmin"
    verbose_name = "FWAdmin"
    description = "Firewall manager and viewer plugin for Netbox"
    version = "0.0.1-dev1"
    author = "Andrea Dainese"
    author_email = "andrea@adainese.it"
    base_url = "fwadmin"
    default_settings = {
        "EDL_UPDATE_INTERVAL": 300,
    }


config = FWAdminConfig  # pylint: disable=invalid-name

# Copy scripts
package = pkgutil.get_loader("fwadmin")
MODULE_PATH = os.path.dirname(package.path)
SCRIPTS_PATH = os.path.join(MODULE_PATH, "scripts")
for filename in os.listdir(SCRIPTS_PATH):
    src_file = os.path.join(SCRIPTS_PATH, filename)
    dst_file = os.path.join(settings.SCRIPTS_ROOT, filename)
    if (
        filename.startswith("__init__")
        or not filename.endswith(".py")
        or not os.path.isfile(src_file)
    ):
        # Not a script file
        continue
    # Copy file in Netbox root scripts path
    shutil.copy(src_file, dst_file)
