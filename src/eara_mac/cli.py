from __future__ import annotations

import argparse
import json
import platform
import sys

from eara_mac import __version__
from eara_mac.core.models import model_from_name
from eara_mac.core.protocol import DIR_GET, CMD_BATTERY, build_frame
from eara_mac.transport.base import TransportUnavailable
from eara_mac.transport.iobluetooth import MacOSBluetoothTransport


def _doctor() -> int:
    report = {
        "eara_mac": __version__,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "iobluetooth": False,
        "paired_devices": None,
    }
    try:
        transport = MacOSBluetoothTransport()
        devices = transport.paired_devices()
        report["iobluetooth"] = True
        report["paired_devices"] = len(devices)
    except TransportUnavailable as exc:
        report["transport_error"] = str(exc)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["iobluetooth"] else 1


def _devices() -> int:
    try:
        devices = MacOSBluetoothTransport().paired_devices()
    except TransportUnavailable as exc:
        print(f"eara-mac: {exc}", file=sys.stderr)
        return 1
    if not devices:
        print("No paired Bluetooth devices found.")
        return 0
    for device in devices:
        model = model_from_name(device.name)
        marker = "compatible-name" if model.base != "unknown" else "unclassified"
        print(f"{device.address}\t{device.name}\t{marker}")
    return 0


def _protocol_selftest() -> int:
    frame = build_frame(CMD_BATTERY, DIR_GET, seq=1)
    print(frame.hex())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="eara-mac")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="check the lightweight macOS environment")
    sub.add_parser("devices", help="list devices already paired by macOS")
    sub.add_parser("protocol-selftest", help="build a battery request without hardware")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        return _doctor()
    if args.command == "devices":
        return _devices()
    return _protocol_selftest()

