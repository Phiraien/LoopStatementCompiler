# Presentation outline

1. Problem and goal: a focused loop-language front end.
2. Scope: the supported C subset and explicit non-goals.
3. Six-member division: lexer, parser, AST, semantics, CLI/build, QA/docs.
4. Pipeline: source → Flex tokens → Bison AST → semantic checks → diagnostics.
5. AST walkthrough using `tests/valid/nested.c`.
6. Error handling using undeclared identifiers and redeclarations.
7. Build/test workflow and honest prerequisite reporting.
8. Limitations and possible extensions: functions, richer types, code generation.
9. Demonstration checklist: `make`, `./loopcc -t ...`, `make test`.
