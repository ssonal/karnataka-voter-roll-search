import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scripts.investigate_rolls import classify, gdown_base, search_text


class NameMatchingTests(unittest.TestCase):
    def test_exact_name_with_trailing_initial(self):
        row = "62 145 ZUI5515010 VICTORIA BRUNDA A  ANTHONY (Father) (78) Death"
        self.assertEqual(classify("Victoria Brunda A", row), "exact")

    def test_trailing_initial_does_not_match_unrelated_short_name(self):
        row = "567 1188 ZUI5279559 R.ARUNA  RAJENDRAN (Father) (31) Permanently Shifted"
        self.assertIsNone(classify("Victoria Brunda A", row))

    def test_exact_two_token_name(self):
        row = "571 1150 ZUI6195135 APARNA IYER  SHRIDHARAN VIVEK IYER (Husband) (34) Permanently Shifted"
        self.assertEqual(classify("Aparna Iyer", row), "exact")

    def test_exact_surname_in_another_name_is_surname_only(self):
        row = "570 1149 ZUI6195127 SHRIDHARAN VIVEK IYER  RAMADURAI IYER (Father) (37) Permanently Shifted"
        self.assertEqual(classify("Aparna Iyer", row), "surname-only")

    def test_small_typo_in_full_name_is_likely(self):
        row = "1 1 ABC1234567 ANITA SAMPLE  RELATIVE SAMPLE (Father) (45) Shifted"
        self.assertEqual(classify("Aneta Sample", row), "likely")

    def test_search_ignores_wrapped_line_without_epic(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "part.txt"
            path.write_text("IYER\n")
            self.assertEqual(search_text("Aparna Iyer", path), [])


class GdownInterfaceTests(unittest.TestCase):
    @patch("scripts.investigate_rolls.shutil.which")
    def test_uvx_pins_json_capable_gdown(self, which):
        which.side_effect = lambda command: "/usr/bin/uvx" if command == "uvx" else None
        self.assertEqual(gdown_base(), ["uvx", "--from", "gdown>=6.1.0", "gdown"])

    @patch("scripts.investigate_rolls.subprocess.run")
    @patch("scripts.investigate_rolls.shutil.which")
    def test_standalone_gdown_must_expose_json(self, which, run):
        which.side_effect = lambda command: "/usr/bin/gdown" if command == "gdown" else None
        run.return_value = SimpleNamespace(returncode=0, stdout="--folder", stderr="")
        with self.assertRaisesRegex(SystemExit, "gdown>=6.1.0"):
            gdown_base()

    @patch("scripts.investigate_rolls.subprocess.run")
    @patch("scripts.investigate_rolls.shutil.which")
    def test_standalone_gdown_with_json_is_supported(self, which, run):
        which.side_effect = lambda command: "/usr/bin/gdown" if command == "gdown" else None
        run.return_value = SimpleNamespace(returncode=0, stdout="--folder --json", stderr="")
        self.assertEqual(gdown_base(), ["gdown"])


if __name__ == "__main__":
    unittest.main()
