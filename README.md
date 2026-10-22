# Loop Statement Compiler

A beginner-friendly Compiler Design mini project that recognizes and validates `for`, `while`, and `do-while` statements using Python. The project demonstrates lexical analysis, recursive-descent parsing, AST construction, semantic analysis, error handling, testing, and a Tkinter GUI.

## Features

- Lexical analysis with regular expressions.
- Recursive-descent syntax analysis.
- Dataclass-based AST nodes.
- Integer declarations and assignments.
- Arithmetic and comparison expressions.
- `for`, `while`, and `do-while` loops.
- Nested loops and blocks.
- Duplicate-declaration checks.
- Undeclared-variable checks.
- Use-before-initialization checks.
- Token, AST, semantic, and compiler-output GUI tabs.
- No third-party Python packages are required.

This is an educational subset of C-like syntax, not a complete C compiler. It does not generate machine code or execute loops.

## Project structure

```text
Loop_Statement_Compiler/
├── main.py                 Compilation pipeline and CLI
├── lexer.py                Regular-expression lexer
├── parser.py               Recursive-descent parser
├── semantic.py             Scope and semantic checks
├── ast_nodes.py            Dataclass AST node definitions
├── gui.py                  Tkinter GUI for the Python compiler
├── launch_python_gui.bat   Windows GUI launcher
├── requirements.txt        Dependency note
├── examples/
│   ├── valid.txt
│   └── invalid.txt
├── tests/
│   └── test_python_compiler.py
└── screenshots/
    └── README.md
```

## Requirements

- Python 3.9 or newer.
- Tkinter for the GUI. It is included with the standard Windows Python installer.
- No `pip install` command is required.

Check Python and Tkinter:

```bash
python --version
python -c "import tkinter; print(tkinter.TkVersion)"
```

On Windows, `py -3` can be used instead of `python`.

## Run the compiler from the terminal

```bash
python main.py
```

Enter a program line by line. Type `END` on its own line to compile it.

Example:

```text
for (int i = 0; i < 10; i++) {
    i++;
}
END
```

The CLI displays:

- Tokens from lexical analysis.
- The dataclass AST.
- The compilation result or the first diagnostic.

## Launch the GUI

From the repository root:

```bash
python gui.py
```

On Windows, double-click:

```text
launch_python_gui.bat
```

The GUI provides:

- Source editor.
- Compile and clear buttons.
- Valid `for`, `while`, and `do-while` sample buttons.
- Lexical token table.
- Expandable AST tree.
- Semantic analysis output.
- Compiler result/status display.

## Test the project

Run all Python tests:

```bash
python -m unittest discover -s tests -p "test_python_compiler.py" -v
```

The tests cover:

1. Valid `for` loop.
2. Valid `while` loop.
3. Valid `do-while` loop.
4. Syntax error caused by a missing semicolon.
5. Undeclared variable.
6. Duplicate declaration.
7. Nested loops.

Expected result:

```text
Ran 7 tests
OK
```

## Supported examples

### Valid `for` loop

```c
for (int i = 0; i < 10; i++) {
    i++;
}
```

### Valid `while` loop

```c
int i = 0;

while (i < 10) {
    i++;
}
```

### Valid `do-while` loop

```c
int i = 0;

do {
    i++;
} while (i < 10);
```

### Syntax error

```c
for (int i = 0 i < 10; i++) {
    i++;
}
```

Expected diagnostic:

```text
Expected SEMICOLON, but found 'i'
```

### Semantic error

```c
while (x < 10) {
    x++;
}
```

Expected diagnostic:

```text
Variable 'x' is not declared
```

## Limitations

The Python implementation intentionally does not support complete C. It currently excludes functions, arrays, pointers, floating-point types, `break`, `continue`, conditional statements, prefix updates, and runtime execution.

## Troubleshooting

### Python was not found

Install Python from the official Python website and enable Tcl/Tk during installation. On Windows, try:

```cmd
py -3 gui.py
```

### Tkinter was not found

Reinstall Python with Tcl/Tk support enabled. Tkinter is normally included in the Windows installer.

### The GUI does not start from WSL

Run the Windows launcher from Command Prompt or PowerShell instead:

```cmd
cd C:\Users\LENOVO\LoopStatementCompiler
py -3 gui.py
```

### Path format in WSL

If running the CLI in WSL, use:

```bash
cd /mnt/c/Users/LENOVO/LoopStatementCompiler
python3 main.py
```

Do not pass `C:\Users\...` paths directly to Linux Bash.

## GitHub workflow

```bash
git clone https://github.com/Phiraien/LoopStatementCompiler.git
cd LoopStatementCompiler
python -m unittest discover -s tests -p "test_python_compiler.py" -v
```

Create a branch before making changes:

```bash
git switch -c member1-lexer
git add .
git commit -m "describe the change"
git push -u origin member1-lexer
```

Do not commit generated files, secrets, local virtual environments, or personal configuration.
