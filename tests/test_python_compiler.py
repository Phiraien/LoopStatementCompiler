import unittest
from pathlib import Path

from main import compile_code


EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


class PythonCompilerTests(unittest.TestCase):
    def test_valid_for(self):
        result = compile_code((EXAMPLES / "valid.txt").read_text(encoding="utf-8"))
        self.assertTrue(result["success"], result["message"])

    def test_valid_while(self):
        result = compile_code("int i = 0; while (i < 10) { i++; }")
        self.assertTrue(result["success"], result["message"])

    def test_valid_do_while(self):
        result = compile_code("int i = 0; do { i++; } while (i < 10);")
        self.assertTrue(result["success"], result["message"])

    def test_syntax_error(self):
        result = compile_code((EXAMPLES / "invalid.txt").read_text(encoding="utf-8"))
        self.assertFalse(result["success"])
        self.assertIn("Expected SEMICOLON", result["message"])

    def test_undeclared_variable(self):
        result = compile_code("while (x < 10) { x++; }")
        self.assertFalse(result["success"])
        self.assertIn("Variable 'x' is not declared", result["message"])

    def test_duplicate_declaration(self):
        result = compile_code("int i = 0; int i = 5;")
        self.assertFalse(result["success"])
        self.assertIn("Variable 'i' already declared", result["message"])

    def test_nested_loops(self):
        result = compile_code("for (int i = 0; i < 5; i++) { for (int j = 0; j < 3; j++) { j++; } }")
        self.assertTrue(result["success"], result["message"])


if __name__ == "__main__":
    unittest.main()
