# EarA-mac

Experimental macOS companion for Nothing and CMF earbuds.

EarA-mac is a separate, lightweight port of the portable protocol core from
[EarA-linux](https://github.com/oneydef/EarA-linux). It intentionally does not
carry BlueZ, D-Bus, PipeWire, GTK, Flatpak, AppImage, or Linux packaging code.

## Current status

- Portable Nothing/CMF frame protocol and model catalogue are imported.
- Core tests run without Bluetooth hardware or GUI dependencies.
- The macOS transport can inspect devices already paired by macOS through
  Apple's IOBluetooth framework.
- Opening the RFCOMM data stream is the next hardware milestone.
- Audio routing and a native GUI are not implemented yet.

This is pre-alpha developer software. EarA-mac is unofficial and is not
affiliated with Nothing Technology or CMF.

## Lite development setup

Full Xcode is not required for the first protocol and Bluetooth-probe phase.

```bash
xcode-select --install
brew install python@3.13

python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[macos,dev]'

eara-mac doctor
eara-mac devices
python -m unittest discover -s tests -v
```

Use macOS Settings to pair the earbuds before running `eara-mac devices`.

## Development principles

1. Keep the protocol core independent from macOS frameworks.
2. Put all Apple-specific work behind small transport and audio interfaces.
3. Keep hardware-free fixtures for every discovered protocol behavior.
4. Validate Bluetooth control in the CLI before building a GUI.
5. Avoid downloading Apple platform simulators; EarA-mac needs only macOS.

See [ARCHITECTURE.md](ARCHITECTURE.md).

## License

GPL-3.0-or-later. The protocol and model catalogue are derived from EarA-linux
under the same license.
