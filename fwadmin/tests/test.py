"""
Clean previous data, load lab-specific content, and test.

To make the process faster, the database is created once and resued:
    - /opt/netbox/venv/bin/python3 /opt/netbox/netbox/manage.py test fwadmin --verbosity=2 --keepdb
"""
from datetime import timedelta

from django.test import TestCase, Client
from django.utils import timezone

from dcim.models import (
    Device,
    DeviceRole,
    DeviceType,
    Manufacturer,
    Interface,
    Site,
)
from ipam.models import IPAddress

from fwadmin.models import DeviceGroup, DynamicList, SessionRequest, Firewall
from fwadmin.tasks import get_expired_items

NOW = timezone.now()


def load_scenario():
    """Purge old data and create basic objects."""
    Device.objects.all().delete()
    DeviceRole.objects.all().delete()
    DeviceType.objects.all().delete()
    Manufacturer.objects.all().delete()
    IPAddress.objects.all().delete()
    Interface.objects.all().delete()
    Site.objects.all().delete()
    Firewall.objects.all().delete()

    device_role_o = DeviceRole.objects.create(name="Testing role")
    manufacturer_o = Manufacturer.objects.create(name="Testing manufacturer")
    device_type_o = DeviceType.objects.create(
        model="Testing model", manufacturer=manufacturer_o
    )
    site_o = Site.objects.create(name="Testing site")

    device_1_o = Device.objects.create(
        name="device1",
        device_role=device_role_o,
        device_type=device_type_o,
        site=site_o,
    )
    device_1_ip_address_1_o = IPAddress.objects.create(address="10.0.0.1/24")
    device_1_ip_address_2_o = IPAddress.objects.create(address="10.0.1.1/24")
    device_1_ip_address_3_o = IPAddress.objects.create(address="192.168.1.1/24")
    device_1_eth0_o = Interface.objects.create(
        name="eth0", device=device_1_o, type="other"
    )
    device_1_eth1_o = Interface.objects.create(
        name="eth1", device=device_1_o, type="other"
    )
    device_1_eth0_o.ip_addresses.add(device_1_ip_address_1_o, device_1_ip_address_2_o)
    device_1_eth1_o.ip_addresses.add(device_1_ip_address_3_o)

    device_2_o = Device.objects.create(
        name="device2",
        device_role=device_role_o,
        device_type=device_type_o,
        site=site_o,
    )
    device_2_ip_address_1_o = IPAddress.objects.create(address="10.0.0.2/24")
    device_2_ip_address_2_o = IPAddress.objects.create(address="10.0.1.2/24")
    device_2_ip_address_3_o = IPAddress.objects.create(address="192.168.1.2/24")
    device_2_eth0_o = Interface.objects.create(
        name="eth0", device=device_2_o, type="other"
    )
    device_2_eth1_o = Interface.objects.create(
        name="eth1", device=device_2_o, type="other"
    )
    device_2_eth0_o.ip_addresses.add(device_2_ip_address_1_o, device_2_ip_address_2_o)
    device_2_eth1_o.ip_addresses.add(device_2_ip_address_3_o)

    device_3_o = Device.objects.create(
        name="device3",
        device_role=device_role_o,
        device_type=device_type_o,
        site=site_o,
    )
    device_3_ip_address_1_o = IPAddress.objects.create(address="10.0.0.3/24")
    device_3_eth0_o = Interface.objects.create(
        name="eth0", device=device_3_o, type="other"
    )
    device_3_eth0_o.ip_addresses.add(device_3_ip_address_1_o)

    device_4_o = Device.objects.create(
        name="device4",
        device_role=device_role_o,
        device_type=device_type_o,
        site=site_o,
    )
    device_4_ip_address_1_o = IPAddress.objects.create(address="10.0.0.4/24")
    device_4_eth0_o = Interface.objects.create(
        name="eth0", device=device_4_o, type="other"
    )
    device_4_eth0_o.ip_addresses.add(device_4_ip_address_1_o)

    device_5_o = Device.objects.create(
        name="device5",
        device_role=device_role_o,
        device_type=device_type_o,
        site=site_o,
    )
    device_5_eth0_o = Interface.objects.create(
        name="eth0", device=device_5_o, type="other"
    )
    device_5_ip_address_1_o = IPAddress.objects.create(address="10.0.0.5/24")
    device_5_eth0_o.ip_addresses.add(device_5_ip_address_1_o)

    device_6_o = Device.objects.create(
        name="device6",
        device_role=device_role_o,
        device_type=device_type_o,
        site=site_o,
    )
    device_6_ip_address_1_o = IPAddress.objects.create(address="10.0.0.6/24")
    device_6_eth0_o = Interface.objects.create(
        name="eth0", device=device_6_o, type="other"
    )
    device_6_eth0_o.ip_addresses.add(device_6_ip_address_1_o)

    device_7_o = Device.objects.create(
        name="device7",
        device_role=device_role_o,
        device_type=device_type_o,
        site=site_o,
    )
    device_7_ip_address_1_o = IPAddress.objects.create(address="10.0.0.7/24")
    device_7_eth0_o = Interface.objects.create(
        name="eth0", device=device_7_o, type="other"
    )
    device_7_eth0_o.ip_addresses.add(device_7_ip_address_1_o)

    device_8_o = Device.objects.create(
        name="device8",
        device_role=device_role_o,
        device_type=device_type_o,
        site=site_o,
    )
    device_8_ip_address_1_o = IPAddress.objects.create(address="10.0.0.8/24")
    device_8_eth0_o = Interface.objects.create(
        name="eth0", device=device_8_o, type="other"
    )
    device_8_eth0_o.ip_addresses.add(device_8_ip_address_1_o)

    firewall_1_o = Firewall.objects.create(  # nosec
        name="firewall1",
        address="firewall1.example.com",
        model="paloalto-panos",
        secret_key="secretkey1",
    )
    firewall_2_o = Firewall.objects.create(  # nosec
        name="firewall2",
        address="firewall2.example.com",
        model="paloalto-panos",
        secret_key="secretkey1",
    )
    firewall_3_o = Firewall.objects.create(  # nosec
        name="firewall3",
        address="firewall3.example.com",
        model="paloalto-panos",
        secret_key="secretkey1",
    )
    firewall_4_o = Firewall.objects.create(  # nosec
        name="firewall4",
        address="firewall4.example.com",
        model="paloalto-panos",
        secret_key="secretkey1",
    )

    device_group_even_o = DeviceGroup.objects.create(name="group_even")
    device_group_even_o.devices.add(device_2_o, device_4_o, device_6_o, device_8_o)

    device_group_odd_o = DeviceGroup.objects.create(name="group_odd")
    device_group_odd_o.devices.add(device_1_o, device_3_o, device_5_o, device_7_o)

    dynamic_list_all_o = DynamicList.objects.create(name="edl_all", rule="EDL_ALL")
    dynamic_list_all_o.device_groups.add(device_group_even_o, device_group_odd_o)
    dynamic_list_all_o.firewalls.add(
        firewall_1_o, firewall_2_o, firewall_3_o, firewall_4_o
    )

    dynamic_list_odd_o = DynamicList.objects.create(name="edl_odd", rule="EDL_ODD")
    dynamic_list_odd_o.device_groups.add(device_group_odd_o)
    dynamic_list_odd_o.firewalls.add(firewall_1_o, firewall_3_o)

    dynamic_list_even_o = DynamicList.objects.create(name="edl_even", rule="EDL_EVEN")
    dynamic_list_even_o.device_groups.add(device_group_even_o)
    dynamic_list_even_o.firewalls.add(firewall_2_o, firewall_4_o)

    dynamic_list_empty_o = DynamicList.objects.create(
        name="edl_empty", rule="EDL_EMPTY"
    )

    return {
        "device_role": device_role_o,
        "manufacturer": manufacturer_o,
        "device_type": device_type_o,
        "site": site_o,
        "devices": [device_1_o, device_2_o, device_3_o, device_4_o],
        "firewalls": [firewall_1_o, firewall_2_o, firewall_3_o, firewall_4_o],
        "device_group_even": device_group_even_o,
        "device_group_odd": device_group_odd_o,
        "dynamic_list_all": dynamic_list_all_o,
        "dynamic_list_odd": dynamic_list_odd_o,
        "dynamic_list_even": dynamic_list_even_o,
        "dynamic_list_empty": dynamic_list_empty_o,
    }


def test_edl(test_o, edl_o, ip_addresses=None):
    """Test EDL url and content."""
    if not ip_addresses:
        ip_addresses = ["0.0.0.0/32"]
    ip_addresses.sort()

    session = Client()
    response = session.get("/plugins/fwadmin/dynamiclist/text/" + str(edl_o.slug) + "/")
    test_o.assertEquals(response.status_code, 200)
    test_o.assertEquals(response.content.decode("utf-8"), "\n".join(ip_addresses))


def test_edl_to_be_cleared(test_o, edl_ids=None):
    """Test EDLs to be cleared."""
    if not edl_ids:
        edl_ids = []

    # Load expired data
    (
        dynamiclists_to_be_cleared_qs,
        uncleared_sessionrequests_qs,  # pylint: disable=unused-variable
    ) = get_expired_items()

    # Test length
    test_o.assertEquals(len(edl_ids), len(dynamiclists_to_be_cleared_qs))

    # Test if edl_ids are in test_edl_to_be_cleared
    for dynamiclists_to_be_cleared__o in dynamiclists_to_be_cleared_qs:
        test_o.assertIn(dynamiclists_to_be_cleared__o.id, edl_ids)


class RequestTests(TestCase):
    """Automated request tests for FWadmin."""

    def test_no_request(self):
        """Check EDLs without requests."""
        basic_data = load_scenario()
        test_edl(self, basic_data.get("dynamic_list_all"))
        test_edl(self, basic_data.get("dynamic_list_odd"))
        test_edl(self, basic_data.get("dynamic_list_even"))
        test_edl(self, basic_data.get("dynamic_list_empty"))
        test_edl_to_be_cleared(self)

    def test_expired_session(self):
        """Check EDLs with an expired request."""
        basic_data = load_scenario()
        start_at_o = NOW - timedelta(days=14)
        end_at_o = NOW - timedelta(days=10)
        expired_session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="approved",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        expired_session_o.dynamic_lists.add(basic_data.get("dynamic_list_all"))
        test_edl(self, basic_data.get("dynamic_list_all"))
        test_edl(self, basic_data.get("dynamic_list_odd"))
        test_edl(self, basic_data.get("dynamic_list_even"))
        test_edl(self, basic_data.get("dynamic_list_empty"))
        test_edl_to_be_cleared(self, edl_ids=[basic_data.get("dynamic_list_all").id])

    def test_future_session(self):
        """Check EDLs with an expired request."""
        basic_data = load_scenario()
        start_at_o = NOW + timedelta(days=7)
        end_at_o = NOW + timedelta(days=9)
        session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="approved",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        session_o.dynamic_lists.add(basic_data.get("dynamic_list_all"))
        test_edl(self, basic_data.get("dynamic_list_all"))
        test_edl(self, basic_data.get("dynamic_list_odd"))
        test_edl(self, basic_data.get("dynamic_list_even"))
        test_edl(self, basic_data.get("dynamic_list_empty"))
        test_edl_to_be_cleared(self)

    def test_active_session_w_all_edls(self):
        """Check EDLs with an active session."""
        basic_data = load_scenario()
        start_at_o = NOW - timedelta(days=1)
        end_at_o = NOW + timedelta(days=1)
        session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="approved",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        session_o.dynamic_lists.add(
            basic_data.get("dynamic_list_all"),
            basic_data.get("dynamic_list_odd"),
            basic_data.get("dynamic_list_even"),
            basic_data.get("dynamic_list_empty"),
        )
        test_edl(
            self,
            basic_data.get("dynamic_list_all"),
            ip_addresses=[
                "192.168.1.1/32",
                "10.0.0.1/32",
                "10.0.1.1/32",
                "192.168.1.2/32",
                "10.0.0.2/32",
                "10.0.1.2/32",
                "10.0.0.3/32",
                "10.0.0.4/32",
                "10.0.0.5/32",
                "10.0.0.6/32",
                "10.0.0.7/32",
                "10.0.0.8/32",
            ],
        )
        test_edl(
            self,
            basic_data.get("dynamic_list_odd"),
            ip_addresses=[
                "192.168.1.1/32",
                "10.0.0.1/32",
                "10.0.1.1/32",
                "10.0.0.3/32",
                "10.0.0.5/32",
                "10.0.0.7/32",
            ],
        )
        test_edl(
            self,
            basic_data.get("dynamic_list_even"),
            ip_addresses=[
                "192.168.1.2/32",
                "10.0.0.2/32",
                "10.0.1.2/32",
                "10.0.0.4/32",
                "10.0.0.6/32",
                "10.0.0.8/32",
            ],
        )
        test_edl(self, basic_data.get("dynamic_list_empty"))
        test_edl_to_be_cleared(self)

    def test_active_session_w_one_edls(self):
        """Check EDLs with an active session."""
        basic_data = load_scenario()
        start_at_o = NOW - timedelta(days=1)
        end_at_o = NOW + timedelta(days=1)
        session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="approved",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        session_o.dynamic_lists.add(basic_data.get("dynamic_list_odd"))
        test_edl(self, basic_data.get("dynamic_list_all"))
        test_edl(
            self,
            basic_data.get("dynamic_list_odd"),
            ip_addresses=[
                "192.168.1.1/32",
                "10.0.0.1/32",
                "10.0.1.1/32",
                "10.0.0.3/32",
                "10.0.0.5/32",
                "10.0.0.7/32",
            ],
        )
        test_edl(self, basic_data.get("dynamic_list_even"))
        test_edl(self, basic_data.get("dynamic_list_empty"))
        test_edl_to_be_cleared(self)

    def test_active_rejected_session(self):
        """Check EDLs with an active session."""
        basic_data = load_scenario()
        start_at_o = NOW - timedelta(days=1)
        end_at_o = NOW + timedelta(days=1)
        session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="rejected",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        session_o.dynamic_lists.add(
            basic_data.get("dynamic_list_all"),
            basic_data.get("dynamic_list_odd"),
            basic_data.get("dynamic_list_even"),
            basic_data.get("dynamic_list_empty"),
        )
        test_edl(self, basic_data.get("dynamic_list_all"))
        test_edl(self, basic_data.get("dynamic_list_odd"))
        test_edl(self, basic_data.get("dynamic_list_even"))
        test_edl(self, basic_data.get("dynamic_list_empty"))
        test_edl_to_be_cleared(self)

    def test_active_requested_session(self):
        """Check EDLs with an active session."""
        basic_data = load_scenario()
        start_at_o = NOW - timedelta(days=1)
        end_at_o = NOW + timedelta(days=1)
        session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="requested",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        session_o.dynamic_lists.add(
            basic_data.get("dynamic_list_all"),
            basic_data.get("dynamic_list_odd"),
            basic_data.get("dynamic_list_even"),
            basic_data.get("dynamic_list_empty"),
        )
        test_edl(self, basic_data.get("dynamic_list_all"))
        test_edl(self, basic_data.get("dynamic_list_odd"))
        test_edl(self, basic_data.get("dynamic_list_even"))
        test_edl(self, basic_data.get("dynamic_list_empty"))
        test_edl_to_be_cleared(self)

    def test_expired_and_active_sessions(self):
        """Check EDLs with an expired and an active sessions."""
        basic_data = load_scenario()
        start_at_o = NOW - timedelta(days=1)
        end_at_o = NOW + timedelta(days=1)
        active_session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="approved",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        active_session_o.dynamic_lists.add(
            basic_data.get("dynamic_list_odd"),
        )
        start_at_o = NOW - timedelta(days=7)
        end_at_o = NOW - timedelta(days=3)
        expired_session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="approved",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        expired_session_o.dynamic_lists.add(
            basic_data.get("dynamic_list_odd"),
        )
        test_edl(self, basic_data.get("dynamic_list_all"))
        test_edl(
            self,
            basic_data.get("dynamic_list_odd"),
            ip_addresses=[
                "192.168.1.1/32",
                "10.0.0.1/32",
                "10.0.1.1/32",
                "10.0.0.3/32",
                "10.0.0.5/32",
                "10.0.0.7/32",
            ],
        )
        test_edl(self, basic_data.get("dynamic_list_even"))
        test_edl(self, basic_data.get("dynamic_list_empty"))
        test_edl_to_be_cleared(self)

    def test_expired_and_future_sessions(self):
        """Check EDLs with an expired and a future sessions."""
        basic_data = load_scenario()
        start_at_o = NOW + timedelta(days=3)
        end_at_o = NOW + timedelta(days=7)
        future_session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="approved",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        future_session_o.dynamic_lists.add(
            basic_data.get("dynamic_list_odd"),
        )
        start_at_o = NOW - timedelta(days=7)
        end_at_o = NOW - timedelta(days=3)
        expired_session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="approved",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        expired_session_o.dynamic_lists.add(
            basic_data.get("dynamic_list_odd"),
        )
        test_edl(self, basic_data.get("dynamic_list_all"))
        test_edl(self, basic_data.get("dynamic_list_odd"))
        test_edl(self, basic_data.get("dynamic_list_even"))
        test_edl(self, basic_data.get("dynamic_list_empty"))
        test_edl_to_be_cleared(self, edl_ids=[basic_data.get("dynamic_list_odd").id])

    def test_just_expired_session(self):
        """Check EDLs with a just expired request."""
        basic_data = load_scenario()
        start_at_o = NOW - timedelta(days=14)
        end_at_o = NOW - timedelta(seconds=1)
        expired_session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="approved",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        expired_session_o.dynamic_lists.add(basic_data.get("dynamic_list_all"))
        test_edl(self, basic_data.get("dynamic_list_all"))
        test_edl(self, basic_data.get("dynamic_list_odd"))
        test_edl(self, basic_data.get("dynamic_list_even"))
        test_edl(self, basic_data.get("dynamic_list_empty"))
        test_edl_to_be_cleared(self)

    def test_expired_session_w_unapproved_session(self):
        """Check EDLs with an expired request and a future pending request."""
        basic_data = load_scenario()
        start_at_o = NOW - timedelta(days=3)
        end_at_o = NOW + timedelta(days=7)
        pending_session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="requested",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        pending_session_o.dynamic_lists.add(
            basic_data.get("dynamic_list_odd"),
        )
        start_at_o = NOW - timedelta(days=7)
        end_at_o = NOW - timedelta(days=3)
        expired_session_o = SessionRequest.objects.create(
            request_reason="Test session",
            status="approved",
            requested_by=None,
            managed_by=None,
            start_at=start_at_o,
            end_at=end_at_o,
        )
        expired_session_o.dynamic_lists.add(
            basic_data.get("dynamic_list_odd"),
        )
        test_edl(self, basic_data.get("dynamic_list_all"))
        test_edl(self, basic_data.get("dynamic_list_odd"))
        test_edl(self, basic_data.get("dynamic_list_even"))
        test_edl(self, basic_data.get("dynamic_list_empty"))
        test_edl_to_be_cleared(self, edl_ids=[basic_data.get("dynamic_list_odd").id])
