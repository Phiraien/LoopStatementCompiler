"""Headless integration checks for the GUI's compiler bridge."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from gui.compiler_runner import CompilerNotFound, CompilerRunner  # noqa: E402


class CompilerBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = CompilerRunner()

    def test_valid_for_returns_structured_ast(self):
        try:
            result = self.runner.compile_file(self.runner.project_root / "tests" / "valid_for.c")
        except CompilerNotFound:
            self.skipTest("loopcc is not built")
        self.assertEqual(result.returncode, 0)
        self.assertIsInstance(result.ast, dict)
        self.assertEqual(result.ast["type"], "program")
        encoded = json.dumps(result.ast)
        self.assertIn('"type": "for"', encoded)

    def test_invalid_syntax_has_no_ast(self):
        try:
            result = self.runner.compile_file(self.runner.project_root / "tests" / "invalid_syntax.c")
        except CompilerNotFound:
            self.skipTest("loopcc is not built")
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(result.ast)
        self.assertIn("syntax error", result.stderr)

    def test_empty_source_is_still_passed_to_compiler(self):
        try:
            result = self.runner.compile_text("")
        except CompilerNotFound:
            self.skipTest("loopcc is not built")
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(result.ast)


if __name__ == "__main__":
    unittest.main()
