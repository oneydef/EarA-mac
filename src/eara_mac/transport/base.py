from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class TransportUnavailable(RuntimeError):
    """The requested platform transport cannot be used in this environment."""


@dataclass(frozen=True)
class PairedDevice:
    address: str
    name: str


class BluetoothTransport(ABC):
    @abstractmethod
    def paired_devices(self) -> list[PairedDevice]:
        """Return devices already paired by the host operating system."""

    @abstractmethod
    def open_rfcomm(self, address: str, channel: int) -> object:
        """Open a bidirectional RFCOMM byte stream."""

