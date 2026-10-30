# Architecture

EarA-mac starts from the EarA-linux wire protocol, not from its Linux platform
integration.

```text
CLI / future SwiftUI app
          |
portable session and device state
          |
portable protocol + model catalogue
          |
macOS Bluetooth transport (IOBluetooth / RFCOMM)
          |
Nothing / CMF earbuds
```

## Boundaries

`eara_mac.core` contains deterministic code. It must not import PyObjC, GTK,
BlueZ, D-Bus, Core Audio, or platform command-line tools.

`eara_mac.transport` owns discovery and byte transport. The public contract is
small enough to support a mock transport and future platform adapters.

The future audio layer will be separate from the control transport. Earbud
control over RFCOMM must keep working even when macOS audio-routing APIs do not
offer Linux feature parity.

## Synchronizing with EarA-linux

Until a shared package exists, protocol updates are brought over deliberately:

1. compare `eara/protocol.py` and `eara/models.py`;
2. copy only wire-format or catalogue changes;
3. copy or create matching fixtures and tests;
4. record the EarA-linux commit in the EarA-mac commit message;
5. never import BlueZ, PipeWire, GTK, or packaging code.

