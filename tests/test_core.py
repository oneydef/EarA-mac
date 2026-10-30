import unittest

from eara_mac.core.models import model_from_name, model_from_serial
from eara_mac.core.protocol import (
    DIR_SET,
    FrameParser,
    build_frame,
    crc16_arc,
    parse_battery,
)


class CoreTests(unittest.TestCase):
    def test_known_anc_frame_matches_linux_reference(self):
        frame = build_frame(0x0F, DIR_SET, bytes([1, 7, 0]), seq=0xCB)
        self.assertEqual(frame.hex(), "5560010ff00300cb010700c5af")

    def test_parser_roundtrip(self):
        raw = build_frame(0x07, 0xC0, b"", seq=9)
        parser = FrameParser()
        parser.feed(raw)
        frame = next(parser.frames())
        self.assertEqual((frame.command, frame.direction, frame.seq), (0x07, 0xC0, 9))

    def test_crc_reference(self):
        body = bytes.fromhex("5560010ff00300cb010700")
        self.assertEqual(crc16_arc(body), 0xAFC5)

    def test_battery_parser(self):
        battery = parse_battery(bytes([3, 2, 80, 3, 75, 4, 50 | 0x80]))
        self.assertEqual(battery["left"]["level"], 80)
        self.assertTrue(battery["case"]["charging"])

    def test_model_catalogue(self):
        self.assertEqual(model_from_name("Nothing Ear (a)").base, "B162")
        self.assertEqual(model_from_serial("63ABC").base, "B162")


if __name__ == "__main__":
    unittest.main()

