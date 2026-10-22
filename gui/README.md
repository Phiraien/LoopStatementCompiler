# Desktop GUI

The GUI is a dependency-free Tkinter desktop application that uses the existing `loopcc` C executable. It does not reimplement the lexer, parser, AST, or semantic analyzer in Python.

## Launch

Build the compiler first from the repository root:

```sh
make
```

Then launch:

```sh
python -m gui.app
```

On Windows, double-click `launch_gui.bat` from the repository root. Python 3 with Tkinter is required; Tkinter is included with the standard Windows Python installer when the Tcl/Tk option is selected.

## Features

- Dark IDE-style source editor with line numbers and basic syntax highlighting.
- New, open, save, save-as, sample programs, and unsaved-change protection.
- Background compilation using `subprocess.run` and argument lists.
- Real compiler exit codes and diagnostics in Output and Errors tabs.
- Interactive AST Treeview populated from the compiler's `-j` JSON output.
- Test runner for `tests/run_tests.sh` using Bash from MSYS2 or PATH.
- Click/double-click compiler error lines to move the editor cursor.

## Structured AST mode

The command-line compiler keeps its existing text tree mode:

```sh
./loopcc -t tests/valid_for.c
```

The GUI uses the new machine-readable mode:

```sh
./loopcc -j tests/valid_for.c
```

The JSON is emitted only after successful parsing and semantic analysis. Diagnostics remain on stderr, so they cannot corrupt the JSON document.

## Troubleshooting

- **Compiler unavailable:** run `make` in MSYS2 UCRT64 or WSL and confirm that `loopcc.exe`/`loopcc` exists in the repository root.
- **Bash not found for Run Tests:** launch from MSYS2 UCRT64, add Bash to PATH, or set the `MSYS2_BASH` environment variable. The GUI prefers `C:\msys64\usr\bin\bash.exe` over WSL Bash so Windows paths are converted correctly.
- **Tkinter unavailable:** reinstall Python with Tcl/Tk support or use a standard Python distribution for Windows.
- **No AST after failure:** this is intentional; the GUI never displays an incomplete or fabricated tree.
