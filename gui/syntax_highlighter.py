"""Small dependency-free syntax highlighter for the supported C subset."""
from __future__ import annotations

import re
import tkinter as tk


class SyntaxHighlighter:
    KEYWORDS = re.compile(r"\b(?:int|for|while|do)\b")
    NUMBERS = re.compile(r"\b\d+\b")
    COMMENTS = re.compile(r"//[^\n]*|/\*[\s\S]*?\*/")
    OPERATORS = re.compile(r"==|!=|<=|>=|[+*/%<>=!()-]")
    IDENTIFIERS = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")

    def __init__(self, text: tk.Text) -> None:
        self.text = text
        for tag, color in {
            "keyword": "#c586c0", "number": "#b5cea8", "comment": "#6a9955",
            "operator": "#d4d4d4", "identifier": "#9cdcfe",
        }.items():
            self.text.tag_configure(tag, foreground=color)
        self.text.bind("<KeyRelease>", self._on_change, add="+")
        self.text.bind("<<Paste>>", self._on_change, add="+")

    def _on_change(self, _event: tk.Event) -> None:
        self.apply()

    def apply(self) -> None:
        for tag in ("keyword", "number", "comment", "operator", "identifier"):
            self.text.tag_remove(tag, "1.0", "end")
        content = self.text.get("1.0", "end-1c")
        for tag, pattern in (
            ("comment", self.COMMENTS), ("keyword", self.KEYWORDS),
            ("number", self.NUMBERS), ("operator", self.OPERATORS),
        ):
            for match in pattern.finditer(content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text.tag_add(tag, start, end)
        for match in self.IDENTIFIERS.finditer(content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            if not self.text.tag_ranges("keyword"):
                self.text.tag_add("identifier", start, end)
            else:
                covered = False
                for first, last in zip(self.text.tag_ranges("keyword")[::2], self.text.tag_ranges("keyword")[1::2]):
                    if self.text.compare(start, ">=", first) and self.text.compare(end, "<=", last):
                        covered = True
                        break
                if not covered:
                    self.text.tag_add("identifier", start, end)
