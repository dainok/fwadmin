"""Workflows, called by Views."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"


class SimpleWorkflow:
    """Simple and basic workflow for fwadmin."""

    current_status = None
    status = [
        "requested",
        "approved",
        "self_approved",
        "rejected",
    ]
    transitions = {
        "requested": {
            "approve": "approved",
            "self_approve": "self_approved",
            "reject": "rejected",
        },
    }

    def __init__(self, status):
        """Setup the workflow."""
        if status in self.status:
            self.current_status = status
        else:
            raise ValueError("Invalid status")

    def transition(self, action):
        """Move to another state."""
        if action in self.transitions.get(self.current_status):
            return self.transitions.get(self.current_status).get(action)
        raise ValueError("Invalid action")
