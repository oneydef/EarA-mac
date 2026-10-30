import unittest

from eara_mac.transport.base import TransportUnavailable
from eara_mac.transport.iobluetooth import MacOSBluetoothTransport


class _Device:
    def __init__(self, address, name):
        self._address = address
        self._name = name

    def addressString(self):
        return self._address

    def name(self):
        return self._name


class _DeviceClass:
    @staticmethod
    def pairedDevices():
        return [_Device("aa-bb-cc-dd-ee-ff", "Nothing Ear (a)")]


class _Framework:
    IOBluetoothDevice = _DeviceClass


class IOBluetoothBoundaryTests(unittest.TestCase):
    def test_paired_devices_are_normalized(self):
        transport = MacOSBluetoothTransport(_Framework(), platform="darwin")
        devices = transport.paired_devices()
        self.assertEqual(devices[0].address, "AA-BB-CC-DD-EE-FF")
        self.assertEqual(devices[0].name, "Nothing Ear (a)")

    def test_non_macos_environment_is_explicit(self):
        with self.assertRaises(TransportUnavailable):
            MacOSBluetoothTransport(platform="linux")

    def test_rfcomm_is_an_explicit_next_milestone(self):
        transport = MacOSBluetoothTransport(_Framework(), platform="darwin")
        with self.assertRaisesRegex(TransportUnavailable, "not implemented"):
            transport.open_rfcomm("AA-BB-CC-DD-EE-FF", 15)


if __name__ == "__main__":
    unittest.main()

