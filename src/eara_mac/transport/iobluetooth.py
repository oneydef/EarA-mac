from __future__ import annotations

import sys
from typing import Any

from .base import BluetoothTransport, PairedDevice, TransportUnavailable


class MacOSBluetoothTransport(BluetoothTransport):
    """Thin boundary around Apple's classic Bluetooth IOBluetooth framework."""

    def __init__(self, framework: Any | None = None, *, platform: str | None = None) -> None:
        platform = platform or sys.platform
        if framework is None:
            if platform != "darwin":
                raise TransportUnavailable("IOBluetooth is available only on macOS")
            try:
                import IOBluetooth as framework
            except ImportError as exc:
                raise TransportUnavailable(
                    "Install the macOS extra: python -m pip install -e '.[macos]'"
                ) from exc
        self._framework = framework

    def paired_devices(self) -> list[PairedDevice]:
        devices = self._framework.IOBluetoothDevice.pairedDevices() or []
        result: list[PairedDevice] = []
        for device in devices:
            address = str(device.addressString() or "").upper()
            name = str(device.name() or "Unknown Bluetooth device")
            if address:
                result.append(PairedDevice(address=address, name=name))
        return result

    def open_rfcomm(self, address: str, channel: int) -> object:
        raise TransportUnavailable(
            "RFCOMM streaming is not implemented yet; device discovery is the first milestone"
        )

