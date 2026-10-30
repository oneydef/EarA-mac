import io
import unittest
from contextlib import redirect_stdout

from eara_mac.cli import main


class CLITests(unittest.TestCase):
    def test_protocol_selftest_runs_without_macos(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["protocol-selftest"])
        self.assertEqual(code, 0)
        self.assertTrue(output.getvalue().strip().startswith("556001"))


if __name__ == "__main__":
    unittest.main()

