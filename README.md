# LoopStatementCompiler

A Compiler Design mini project implementing a loop statement compiler front end using C, Flex, and Bison.

## Overview

This repository recognizes and validates a documented, integer-only subset of C containing:

- `for`, `while`, and `do-while` loops
- integer declarations and assignments
- arithmetic and comparison expressions
- nested blocks and nested loops
- line and block comments
- AST construction and printing
- lexical-scope semantic checks
- syntax, lexical, and semantic diagnostics

This is a front end for demonstration and viva purposes. It does **not** generate machine code or claim to implement complete ISO C.

## Requirements

- GCC or another C11 compiler
- Flex
- Bison
- GNU Make
- POSIX shell for `tests/run_tests.sh`

### Ubuntu/Linux installation

```sh
sudo apt update
sudo apt install build-essential flex bison make
```

### Windows

Use MSYS2/MinGW, WSL, or another environment that provides the commands above. In MSYS2 UCRT64, install the packages with:

```sh
pacman -S --needed flex bison make mingw-w64-ucrt-x86_64-gcc
```

## Build and run

```sh
make clean
make
./loopcc -t tests/valid_for.c
```

The compiler reads stdin when no source path is supplied:

```sh
./loopcc < tests/valid_while.c
```

Exit codes are 0 for success, 1 for syntax/semantic failure, and 2 for command-line or prerequisite errors.

## Tests

Run the complete suite:

```sh
make test
# or
sh tests/run_tests.sh
```

The suite covers the three requested valid loop examples, syntax failure, semantic failure, and additional nested/scope cases. A successful run reports `Summary: 9 passed, 0 failed.` The repository must be tested in an environment with the required toolchain; otherwise the script reports the missing tools and exits with status 2 rather than inventing results.

Run the headless GUI/compiler bridge checks with:

```sh
make gui-test
```

These tests validate JSON AST output, invalid syntax handling, and empty-source behavior without requiring a display.

## Project structure

```text
lexer.l                 Flex lexer
parser.y                Bison grammar and parser actions
ast.h, ast.c            AST definitions, construction, printing, cleanup
semantic.h, semantic.c  Symbol table, scopes, semantic diagnostics
main.c                  CLI, parser/semantic integration
Makefile                Generation, compilation, check, test, clean targets
tests/                  Valid/invalid source programs and test runner
.github/                Pull-request and issue templates
screenshots/            Instructions for adding verified screenshots
```

Generated parser/lexer C files, object files, executables, editor settings, and crash dumps are ignored by Git.

## Language limitations

The supported subset intentionally excludes functions, arrays, pointers, floating-point values, types other than `int`, comma operators, `break`, `continue`, `if`, code generation, optimization, and runtime evaluation. See `docs/cfg_and_grammar.md` for the grammar and `docs/architecture.md` for the pipeline.

## AST tree output

Use `-t` to print a branching tree with readable node names:

```sh
./loopcc -t tests/valid_for.c
```

Example shape:

```text
Program
└── Block
    ├── Declaration: i
    │   └── Integer: 0
    └── For Loop
        ├── Initialization
        │   └── Assignment: i
        │       └── Integer: 0
        ├── Condition
        │   └── Binary Expression: <
        │       ├── Identifier: i
        │       └── Integer: 3
        ├── Update
        │   └── Assignment: i
        │       └── Binary Expression: +
        └── Body
            └── Block
```

The printer includes `for`, `while`, and `do-while` loop labels, condition/initialization/update/body branches, nested blocks, binary and unary expressions, identifiers, and integer literals.

The compiler also exposes a structured AST mode for tools such as the desktop GUI:

```sh
./loopcc -j tests/valid_for.c
```

`-j` emits JSON only after successful parsing and semantic analysis. Diagnostics remain on stderr. The text mode remains available through `-t`.

## Desktop GUI

The repository includes a dependency-free Tkinter dark IDE GUI. It edits and saves source files, invokes the existing C compiler, displays real diagnostics, runs the test suite, and renders the actual AST JSON in an expandable Treeview. It does not reimplement the compiler in Python.

Build the C compiler and launch the GUI:

```sh
make
python -m gui.app
```

On Windows, double-click `launch_gui.bat`. See [`gui/README.md`](gui/README.md) for MSYS2, Tkinter, structured AST, and troubleshooting instructions.

## Six-member work division

1. Member 1 — `lexer.l`: lexical analysis.
2. Member 2 — `parser.y`: CFG, grammar transformations, and syntax analysis.
3. Member 3 — `ast.h`, `ast.c`: AST implementation.
4. Member 4 — `semantic.h`, `semantic.c`: semantic analysis.
5. Member 5 — `main.c`, `Makefile`: integration and build system.
6. Member 6 — `tests/`, `README.md`: testing, documentation, and automation.

Every member should also make reviewable contributions to the report, presentation, and Git history. `docs/individual_contributions.md` is a work-plan template and must be updated with verified names and commits only.

## Collaboration workflow

Keep `main` stable. Each member should:

```sh
git clone https://github.com/Phiraien/LoopStatementCompiler.git
cd LoopStatementCompiler
git switch -c member1-lexer   # choose the assigned branch name
git add <files>
git commit -m "feat: describe the change"
git push -u origin member1-lexer
```

Recommended branches include `member1-lexer`, `member2-parser`, `member3-ast`, `member4-semantic`, `member5-integration`, and `member6-tests-docs`. Open a pull request into `main`, describe the test command and result, request review, and merge only after review. Do not commit credentials, generated artifacts, personal configuration, or unverified screenshots. Do not invite collaborators until their GitHub usernames and authorization are confirmed.

## Documentation

- `docs/interfaces.md` — shared tokens, functions, ownership, and parser contracts.
- `docs/cfg_and_grammar.md` — CFG and grammar transformations.
- `docs/architecture.md` — compiler pipeline and design.
- `docs/project_report.md` — report draft with placeholders for verified team data.
- `docs/viva_questions.md` — likely viva questions and concise answers.
- `docs/individual_contributions.md` — six-member work plan.
- `presentation/presentation_outline.md` — slide-by-slide outline.
