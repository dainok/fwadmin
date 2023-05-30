"""Script used to manually import Discoverables."""  # pylint: disable=invalid-name

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from extras.scripts import Script

from fwadmin.tasks import terminate_sessions


class SessionFence(Script):
    """Script used to clear traffic sessions."""

    class Meta:
        """Script metadata."""

        name = "SessionFence"
        description = "Clear traffic sessions on firewalls."
        commit_default = True

    def run(self, data, commit):
        """Start the script."""
        return terminate_sessions(self)
