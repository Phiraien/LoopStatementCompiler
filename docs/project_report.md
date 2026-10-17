# Loop Statement Compiler — Project Report Draft

> Replace bracketed placeholders with verified project information. Do not add invented names, screenshots, dates, or test results.

## Title page

- **Project:** Loop Statement Compiler — Compiler Front-End Development
- **Institution:** [institution]
- **Course:** [course]
- **Team members:** [verified names and identifiers]
- **Faculty guide:** [verified name]
- **Submission date:** [verified date]

## Abstract

This project implements a small compiler front end for a documented integer-only C subset containing `for`, `while`, and `do-while` loops. The front end demonstrates lexical analysis with Flex, syntax analysis with Bison, AST construction, lexical-scope semantic checks, diagnostics, and automated tests. It does not generate machine code.

## 1. Introduction

Loop statements combine initialization, conditions, updates, and nested statement bodies, making them useful for demonstrating the major front-end stages of a compiler. The project focuses on an intentionally limited language so the implementation remains understandable during a college demonstration and viva.

## 2. Objectives

- Recognize the selected loop constructs.
- Separate lexical, syntax, AST, and semantic stages.
- Report syntax and semantic errors with line numbers.
- Provide reproducible build and test commands.
- Document interfaces so six members can work in parallel.

## 3. Scope and limitations

The supported subset includes integer declarations, assignments, arithmetic and comparison expressions, nested blocks, comments, and the three requested loops. It excludes functions, arrays, pointers, non-integer types, code generation, and full ISO C behavior.

## 4. System architecture

Describe the pipeline from `lexer.l` to `parser.y`, AST construction, `semantic.c`, and `main.c`. Insert an approved architecture diagram or screenshot here if the team creates one.

## 5. Grammar and CFG

Summarize the grammar in `docs/cfg_and_grammar.md`, including list handling, expression precedence, and optional `for` components.

## 6. Implementation

### 6.1 Lexer

Explain keyword recognition, identifiers, integer literals, comments, operators, delimiters, whitespace, and line tracking.

### 6.2 Parser

Explain Bison productions, precedence declarations, parser actions, and syntax-error handling.

### 6.3 AST

Explain node kinds, child ownership, printing, and recursive cleanup.

### 6.4 Semantic analysis

Explain scopes, duplicate declarations, undeclared uses, and assignment checks.

## 7. Testing and results

Record only commands actually run and their observed results. Include the environment and tool versions. Do not copy expected results into this section until they have been verified.

| Case | Purpose | Observed result |
|---|---|---|
| `tests/valid_for.c` | Valid `for` loop | [record verified result] |
| `tests/valid_while.c` | Valid `while` loop | [record verified result] |
| `tests/valid_do_while.c` | Valid `do-while` loop | [record verified result] |
| `tests/invalid_syntax.c` | Syntax failure | [record verified result] |
| `tests/invalid_semantic.c` | Semantic failure | [record verified result] |

## 8. Team contributions

Use `docs/individual_contributions.md` and replace the work-plan placeholders with verified names, commits, and review links.

## 9. Demonstration plan

Demonstrate one valid input, print its AST, show a syntax error, show an undeclared-variable error, and explain how the lexer/parser/semantic stages isolate responsibilities.

## 10. Conclusion and future work

The project demonstrates a complete educational compiler-front-end pipeline for loop statements. Future work may add `break`, `continue`, functions, richer types, three-address code, and code generation.

## References

- Flex and Bison documentation used by the team.
- Course lecture notes and approved compiler-design references.
