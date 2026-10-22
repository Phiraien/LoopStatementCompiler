"""Dark Tkinter IDE for the Loop Statement Compiler."""
from __future__ import annotations

import queue
from pathlib import Path
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from .ast_viewer import ASTViewer
from .compiler_runner import CompilerNotFound, CompilerRunner, ProcessResult
from .syntax_highlighter import SyntaxHighlighter


SAMPLES = {
    "Simple for loop": """{
    int i = 0;
    for (i = 0; i < 5; i = i + 1) {
        int twice = i * 2;
    }
}
""",
    "Simple while loop": """{
    int count = 3;
    while (count > 0) {
        count = count - 1;
    }
}
""",
    "Simple do-while loop": """{
    int value = 0;
    do {
        value = value + 1;
    } while (value < 2);
}
""",
    "Nested loops": """{
    int i = 0;
    for (i = 0; i < 3; i = i + 1) {
        int j = 0;
        while (j < 2) {
            j = j + 1;
        }
    }
}
""",
    "Arithmetic expressions": """{
    int result = (4 + 3) * 2;
    result = result % 3;
}
""",
    "Invalid syntax": """{
    int i = 0;
    while (i < 3) {
        i = i + 1
    }
}
""",
    "Undeclared variable": """{
    int value = 1;
    missing = value + other;
}
""",
}


class LineNumberedEditor(ttk.Frame):
    def __init__(self, master: tk.Misc, on_modified) -> None:
        super().__init__(master)
        self.on_modified = on_modified
        self.line_numbers = tk.Canvas(self, width=42, background="#252526", highlightthickness=0)
        self.text = tk.Text(
            self, undo=True, wrap="none", background="#1e1e1e", foreground="#d4d4d4",
            insertbackground="#ffffff", selectbackground="#264f78", borderwidth=0,
            font=("Consolas", 12), padx=8, pady=8, tabs=("4c",),
        )
        yscroll = ttk.Scrollbar(self, orient="vertical", command=self._scroll_y)
        xscroll = ttk.Scrollbar(self, orient="horizontal", command=self._scroll_x)
        self.text.configure(yscrollcommand=self._on_text_scroll, xscrollcommand=xscroll.set)
        self.line_numbers.grid(row=0, column=0, sticky="ns")
        self.text.grid(row=0, column=1, sticky="nsew")
        yscroll.grid(row=0, column=2, sticky="ns")
        xscroll.grid(row=1, column=1, sticky="ew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.text.bind("<KeyRelease>", self._changed, add="+")
        self.text.bind("<<Modified>>", self._modified, add="+")
        self.text.bind("<Tab>", self._tab)
        self.text.bind("<Return>", self._newline_indent)
        self.text.bind("<Configure>", lambda _event: self.redraw())
        self.text.bind("<MouseWheel>", lambda _event: self.redraw())
        self.redraw()

    def _scroll_y(self, *args) -> None:
        self.text.yview(*args)
        self.redraw()

    def _scroll_x(self, *args) -> None:
        self.text.xview(*args)

    def _on_text_scroll(self, first, last) -> None:
        self.line_numbers.yview_moveto(first)
        self.redraw()

    def _modified(self, _event=None) -> None:
        if self.text.edit_modified():
            self.on_modified()
            self.text.edit_modified(False)

    def _changed(self, _event=None) -> None:
        self.redraw()

    def _tab(self, _event=None):
        self.text.insert("insert", "    ")
        return "break"

    def _newline_indent(self, _event=None):
        line = self.text.get("insert linestart", "insert")
        indent = re.match(r"\s*", line).group(0)
        if line.rstrip().endswith("{"):
            indent += "    "
        self.text.insert("insert", "\n" + indent)
        return "break"

    def redraw(self) -> None:
        self.line_numbers.delete("all")
        first = int(self.text.index("@0,0").split(".")[0])
        last = int(self.text.index(f"@0,{self.winfo_height()}").split(".")[0]) + 1
        for line in range(first, last + 1):
            bbox = self.text.bbox(f"{line}.0")
            if bbox:
                self.line_numbers.create_text(36, bbox[1] + 2, anchor="ne", text=str(line), fill="#858585", font=("Consolas", 10))


class CompilerApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Loop Statement Compiler")
        self.geometry("1250x820")
        self.minsize(900, 600)
        self.configure(background="#181818")
        self.runner = CompilerRunner()
        self.current_path: Optional[Path] = None
        self.dirty = False
        self.result_queue: queue.Queue[tuple[str, object]] = queue.Queue()
        self._configure_style()
        self._build_ui()
        self._load_text(SAMPLES["Simple for loop"])
        self.after(100, self._poll_queue)
        self.protocol("WM_DELETE_WINDOW", self._close)

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#181818")
        style.configure("Toolbar.TFrame", background="#252526")
        style.configure("TLabel", background="#181818", foreground="#d4d4d4")
        style.configure("Title.TLabel", background="#252526", foreground="#ffffff", font=("Segoe UI", 13, "bold"))
        style.configure("Status.TLabel", background="#252526", foreground="#9cdcfe")
        style.configure("TButton", background="#333333", foreground="#eeeeee", padding=(9, 5))
        style.map("TButton", background=[("active", "#454545")])
        style.configure("TNotebook", background="#181818", borderwidth=0)
        style.configure("TNotebook.Tab", background="#2d2d2d", foreground="#cccccc", padding=(12, 6))
        style.configure("TCombobox", fieldbackground="#333333", background="#333333", foreground="#eeeeee")
        style.configure("Treeview", background="#1e1e1e", fieldbackground="#1e1e1e", foreground="#d4d4d4", borderwidth=0)
        style.map("Treeview", background=[("selected", "#264f78")])

    def _build_ui(self) -> None:
        toolbar = ttk.Frame(self, style="Toolbar.TFrame", padding=8)
        toolbar.pack(fill="x")
        ttk.Label(toolbar, text="◈  Loop Statement Compiler", style="Title.TLabel").pack(side="left", padx=(0, 18))
        for label, command in (("New", self.new_file), ("Open", self.open_file), ("Save", self.save_file), ("Save As", self.save_as), ("Compile", self.compile), ("Run Tests", self.run_tests), ("Clear Output", self.clear_output)):
            ttk.Button(toolbar, text=label, command=command).pack(side="left", padx=2)
        self.sample_var = tk.StringVar(value="Samples")
        samples = ttk.Combobox(toolbar, textvariable=self.sample_var, values=list(SAMPLES), state="readonly", width=24)
        samples.pack(side="left", padx=(12, 4))
        samples.bind("<<ComboboxSelected>>", self.load_sample)
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(toolbar, textvariable=self.status_var, style="Status.TLabel").pack(side="right")

        self.editor = LineNumberedEditor(self, self.mark_dirty)
        self.highlighter = SyntaxHighlighter(self.editor.text)
        self.editor.pack(fill="both", expand=True, padx=8, pady=(8, 0))

        self.notebook = ttk.Notebook(self, height=245)
        self.output_text = self._add_text_tab("Output")
        self.errors_text = self._add_text_tab("Errors")
        self.ast_viewer = ASTViewer(self.notebook)
        self.notebook.add(self.ast_viewer, text="AST")
        self.tests_text = self._add_text_tab("Tests")
        self.notebook.pack(fill="x", padx=8, pady=8)
        self.errors_text.bind("<Double-Button-1>", self._jump_to_error)

    def _add_text_tab(self, title: str) -> tk.Text:
        frame = ttk.Frame(self.notebook)
        text = tk.Text(frame, height=10, background="#1e1e1e", foreground="#d4d4d4", insertbackground="#ffffff", font=("Consolas", 10), borderwidth=0)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.notebook.add(frame, text=title)
        return text

    def _load_text(self, content: str) -> None:
        self.editor.text.delete("1.0", "end")
        self.editor.text.insert("1.0", content)
        self.editor.text.edit_modified(False)
        self.dirty = False
        self.highlighter.apply()
        self.editor.redraw()
        self._update_title()

    def mark_dirty(self) -> None:
        self.dirty = True
        self._update_title()

    def _update_title(self) -> None:
        name = self.current_path.name if self.current_path else "Untitled"
        self.title(("*" if self.dirty else "") + name + " — Loop Statement Compiler")

    def _confirm_discard(self) -> bool:
        if not self.dirty:
            return True
        choice = messagebox.askyesnocancel("Unsaved changes", "Save changes before continuing?")
        if choice is None:
            return False
        return self.save_file() if choice else True

    def new_file(self) -> None:
        if self._confirm_discard():
            self.current_path = None
            self._load_text("{\n    \n}\n")

    def open_file(self) -> None:
        if not self._confirm_discard(): return
        chosen = filedialog.askopenfilename(filetypes=[("C source", "*.c"), ("All files", "*.*")])
        if chosen:
            self.current_path = Path(chosen)
            self._load_text(self.current_path.read_text(encoding="utf-8"))

    def save_file(self) -> bool:
        if self.current_path is None:
            return self.save_as()
        self.current_path.write_text(self.editor.text.get("1.0", "end-1c") + "\n", encoding="utf-8")
        self.dirty = False
        self._update_title()
        return True

    def save_as(self) -> bool:
        chosen = filedialog.asksaveasfilename(defaultextension=".c", filetypes=[("C source", "*.c"), ("All files", "*.*")])
        if not chosen: return False
        self.current_path = Path(chosen)
        return self.save_file()

    def load_sample(self, _event=None) -> None:
        if self._confirm_discard():
            self.current_path = None
            self._load_text(SAMPLES[self.sample_var.get()])

    def compile(self) -> None:
        source = self.editor.text.get("1.0", "end-1c")
        if not source.strip():
            self.status_var.set("Compile failed: empty source")
            self._set_text(self.errors_text, "Source is empty. Enter a program before compiling.\n")
            return
        self.status_var.set("Compiling…")
        self._set_text(self.output_text, "Compiling with the existing C compiler…\n")
        self._set_text(self.errors_text, "")
        threading.Thread(target=self._compile_worker, args=(source,), daemon=True).start()

    def _compile_worker(self, source: str) -> None:
        try:
            result = self.runner.compile_text(source)
            self.result_queue.put(("compile", result))
        except CompilerNotFound as exc:
            self.result_queue.put(("compile-error", str(exc)))
        except Exception as exc:  # keep the GUI alive and report internal failures
            self.result_queue.put(("compile-error", f"Internal GUI error: {exc}"))

    def run_tests(self) -> None:
        self.status_var.set("Running tests…")
        self._set_text(self.tests_text, "Running tests…\n")
        threading.Thread(target=self._test_worker, daemon=True).start()

    def _test_worker(self) -> None:
        self.result_queue.put(("tests", self.runner.run_tests()))

    def _poll_queue(self) -> None:
        try:
            while True:
                kind, payload = self.result_queue.get_nowait()
                if kind == "compile": self._show_compile(payload)  # type: ignore[arg-type]
                elif kind == "compile-error": self._show_compile_error(str(payload))
                elif kind == "tests": self._show_tests(payload)  # type: ignore[arg-type]
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    def _show_compile(self, result: ProcessResult) -> None:
        if result.returncode == 0 and result.ast is not None:
            self.status_var.set(f"✓ Compile succeeded ({result.elapsed_ms} ms)")
            self._set_text(self.output_text, result.stdout or "Compilation succeeded.\n")
            self._set_text(self.errors_text, result.stderr or "No errors.\n")
            self.ast_viewer.show_ast(result.ast)
            self.notebook.select(self.ast_viewer)
        else:
            self.status_var.set(f"✗ Compile failed (exit {result.returncode})")
            self._set_text(self.output_text, result.stdout or "Compilation failed.\n")
            self._set_text(self.errors_text, result.stderr or "Compiler returned a failure without diagnostics.\n")
            self.ast_viewer.clear()
            self.notebook.select(self.errors_text.master)

    def _show_compile_error(self, message: str) -> None:
        self.status_var.set("✗ Compiler unavailable")
        self._set_text(self.errors_text, message + "\n")
        self.ast_viewer.clear()

    def _show_tests(self, result: ProcessResult) -> None:
        self.status_var.set("✓ Tests passed" if result.returncode == 0 else f"✗ Tests failed (exit {result.returncode})")
        self._set_text(self.tests_text, result.stdout + result.stderr)
        self.notebook.select(self.tests_text.master)

    @staticmethod
    def _set_text(widget: tk.Text, content: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", content)
        widget.configure(state="disabled")

    def clear_output(self) -> None:
        for widget in (self.output_text, self.errors_text, self.tests_text):
            self._set_text(widget, "")
        self.ast_viewer.clear()
        self.status_var.set("Ready")

    def _jump_to_error(self, _event=None) -> None:
        line_text = self.errors_text.get("insert linestart", "insert lineend")
        match = re.search(r"line\s+(\d+)", line_text, re.IGNORECASE)
        if match:
            self.editor.text.see(f"{match.group(1)}.0")
            self.editor.text.mark_set("insert", f"{match.group(1)}.0")
            self.editor.text.focus_set()

    def _close(self) -> None:
        if self._confirm_discard():
            self.destroy()


def main() -> None:
    CompilerApp().mainloop()


if __name__ == "__main__":
    main()
