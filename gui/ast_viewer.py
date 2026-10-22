"""AST Treeview rendering for the compiler's structured JSON output."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any


LABELS = {
    "program": "Program",
    "block": "Block",
    "declaration": "Declaration",
    "assignment": "Assignment",
    "expression_statement": "Expression Statement",
    "for": "For Loop",
    "while": "While Loop",
    "do_while": "Do-While Loop",
    "initialization": "Initialization",
    "condition": "Condition",
    "update": "Update",
    "body": "Body",
    "integer": "Integer",
    "identifier": "Identifier",
    "binary": "Binary Expression",
    "unary": "Unary Expression",
}


class ASTViewer(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.tree = ttk.Treeview(self, columns=("line",), show="tree headings")
        self.tree.heading("#0", text="AST")
        self.tree.heading("line", text="Line")
        self.tree.column("#0", minwidth=260, width=560, stretch=True)
        self.tree.column("line", minwidth=50, width=70, anchor="center", stretch=False)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def clear(self) -> None:
        self.tree.delete(*self.tree.get_children())

    def show_ast(self, document: dict[str, Any]) -> None:
        self.clear()
        root = self.tree.insert("", "end", text="Program", values=(document.get("line", 0),), open=True)
        for child in document.get("children", []):
            self._insert(root, child, open_node=True)

    def _insert(self, parent: str, node: dict[str, Any], open_node: bool = False) -> str:
        node_type = str(node.get("type", "unknown"))
        label = LABELS.get(node_type, node_type.replace("_", " ").title())
        details = []
        for key in ("name", "operator", "value"):
            if key in node:
                details.append(str(node[key]))
        if details:
            label += ": " + " ".join(details)
        item = self.tree.insert(parent, "end", text=label, values=(node.get("line", 0),), open=open_node)
        for child in node.get("children", []):
            self._insert(item, child, open_node=False)
        return item
