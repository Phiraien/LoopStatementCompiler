import tkinter as tk
from dataclasses import fields, is_dataclass
from tkinter import messagebox, ttk

from main import compile_code


class CompilerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Loop Statement Mini Compiler")
        root.geometry("1150x750")
        root.minsize(850, 600)
        self.bg = "#f4f6f9"
        self.root.configure(bg=self.bg)
        self._style()
        self._widgets()
        self.load_for_example()

    def _style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TNotebook", background=self.bg, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=(18, 10))
        style.configure("Treeview", font=("Consolas", 11), rowheight=28)

    def _widgets(self):
        header = tk.Frame(self.root, bg="#1e293b", height=78)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="LOOP STATEMENT MINI COMPILER", font=("Arial", 21, "bold"), fg="white", bg="#1e293b").pack(pady=(12, 0))
        tk.Label(header, text="Lexical Analysis  •  Syntax Analysis  •  AST  •  Semantic Analysis", fg="#cbd5e1", bg="#1e293b").pack()

        container = tk.Frame(self.root, bg=self.bg)
        container.pack(fill="both", expand=True, padx=18, pady=15)
        tk.Label(container, text="SOURCE CODE EDITOR", font=("Arial", 13, "bold"), bg=self.bg, fg="#1e293b").pack(anchor="w")
        editor_frame = tk.Frame(container)
        editor_frame.pack(fill="both", expand=True, pady=(8, 10))
        self.code_editor = tk.Text(editor_frame, font=("Consolas", 12), bg="white", fg="#1e293b", undo=True, wrap="none", padx=12, pady=12)
        scroll = ttk.Scrollbar(editor_frame, orient="vertical", command=self.code_editor.yview)
        self.code_editor.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.code_editor.pack(side="left", fill="both", expand=True)

        buttons = tk.Frame(container, bg=self.bg)
        buttons.pack(fill="x", pady=(0, 12))
        for text, command, color in (("▶ Compile", self.compile_program, "#2563eb"), ("Clear", self.clear_all, "#64748b"), ("For Loop", self.load_for_example, "#0f766e"), ("While Loop", self.load_while_example, "#0f766e"), ("Do-While Loop", self.load_do_while_example, "#0f766e")):
            tk.Button(buttons, text=text, command=command, bg=color, fg="white", relief="flat", padx=16, pady=8).pack(side="left", padx=(0, 8))

        tk.Label(container, text="COMPILATION RESULTS", font=("Arial", 13, "bold"), bg=self.bg, fg="#1e293b").pack(anchor="w")
        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True, pady=(8, 0))
        self.token_tab = ttk.Frame(self.notebook); self.ast_tab = ttk.Frame(self.notebook); self.semantic_tab = ttk.Frame(self.notebook); self.output_tab = ttk.Frame(self.notebook)
        for tab, name in ((self.token_tab, "Lexical Tokens"), (self.ast_tab, "Abstract Syntax Tree"), (self.semantic_tab, "Semantic Analysis"), (self.output_tab, "Compiler Output")):
            self.notebook.add(tab, text=name)
        self._token_table(); self._ast_tree(); self._text_views()
        self.status = tk.Label(self.root, text="Ready to compile", anchor="w", bg="#e2e8f0", fg="#1e293b", padx=15, pady=10)
        self.status.pack(fill="x")

    def _token_table(self):
        frame = ttk.Frame(self.token_tab); frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.token_table = ttk.Treeview(frame, columns=("no", "type", "value"), show="headings")
        for col, title, width in (("no", "No.", 70), ("type", "Token Type", 200), ("value", "Token Value", 250)):
            self.token_table.heading(col, text=title); self.token_table.column(col, width=width, anchor="center")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.token_table.yview); self.token_table.configure(yscrollcommand=scroll.set); scroll.pack(side="right", fill="y"); self.token_table.pack(fill="both", expand=True)

    def _ast_tree(self):
        frame = ttk.Frame(self.ast_tab); frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.ast_tree = ttk.Treeview(frame, show="tree"); scroll = ttk.Scrollbar(frame, orient="vertical", command=self.ast_tree.yview); self.ast_tree.configure(yscrollcommand=scroll.set); scroll.pack(side="right", fill="y"); self.ast_tree.pack(fill="both", expand=True)

    def _text_views(self):
        self.semantic_text = self._text_tab(self.semantic_tab, "white", "#1e293b")
        self.output_text = self._text_tab(self.output_tab, "#0f172a", "#e2e8f0")

    @staticmethod
    def _text_tab(parent, background, foreground):
        text = tk.Text(parent, font=("Consolas", 11), bg=background, fg=foreground, padx=15, pady=15, wrap="word", state="disabled")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        return text

    @staticmethod
    def _set_text(widget, value):
        widget.config(state="normal"); widget.delete("1.0", tk.END); widget.insert(tk.END, value); widget.config(state="disabled")

    def insert_ast(self, parent, node, label=None):
        if isinstance(node, list):
            item = self.ast_tree.insert(parent, "end", text=label or "Statements", open=True)
            for child in node: self.insert_ast(item, child)
        elif is_dataclass(node):
            name = type(node).__name__ if not label else f"{label}: {type(node).__name__}"
            item = self.ast_tree.insert(parent, "end", text=name, open=True)
            for field in fields(node): self.insert_ast(item, getattr(node, field.name), field.name)
        elif label is not None:
            self.ast_tree.insert(parent, "end", text=f"{label}: {node}")

    def compile_program(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Empty Code", "Please enter source code."); return
        for item in self.token_table.get_children(): self.token_table.delete(item)
        for item in self.ast_tree.get_children(): self.ast_tree.delete(item)
        result = compile_code(code)
        for index, (token_type, token_value) in enumerate(result["tokens"], 1):
            if token_type != "EOF": self.token_table.insert("", "end", values=(index, token_type, token_value))
        if result["ast"] is not None: self.insert_ast("", result["ast"])
        if result["success"]:
            self._set_text(self.semantic_text, "SEMANTIC ANALYSIS\n========================\n\n✓ Variable declarations checked\n✓ Variable initialization checked\n✓ Variable usage checked\n✓ Loop expressions analyzed\n\nResult: No semantic errors found.")
            self._set_text(self.output_text, "COMPILATION SUCCESSFUL\n========================\n\nLexical Analysis : PASSED\nSyntax Analysis  : PASSED\nSemantic Analysis: PASSED\n\n" + result["message"])
            self.status.config(text="✓ Compilation Successful", fg="#15803d")
        else:
            self._set_text(self.semantic_text, "COMPILATION FAILED\n\n" + result["message"])
            self._set_text(self.output_text, "COMPILATION ERROR\n========================\n\n" + result["message"])
            self.status.config(text="✗ Compilation Failed", fg="#dc2626")
        self.notebook.select(self.output_tab)

    def clear_all(self):
        self.code_editor.delete("1.0", tk.END)
        for item in self.token_table.get_children(): self.token_table.delete(item)
        for item in self.ast_tree.get_children(): self.ast_tree.delete(item)
        self._set_text(self.semantic_text, ""); self._set_text(self.output_text, ""); self.status.config(text="Ready to compile", fg="#1e293b")

    def load_code(self, code): self.clear_all(); self.code_editor.insert("1.0", code)
    def load_for_example(self): self.load_code("for (int i = 0; i < 5; i++) {\n    i++;\n}")
    def load_while_example(self): self.load_code("int i = 0;\n\nwhile (i < 5) {\n    i++;\n}")
    def load_do_while_example(self): self.load_code("int i = 0;\n\ndo {\n    i++;\n} while (i < 5);")


if __name__ == "__main__":
    root = tk.Tk(); CompilerGUI(root); root.mainloop()
