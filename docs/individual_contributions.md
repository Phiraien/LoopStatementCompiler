# Individual Contributions

This allocation supports six members working independently. It is a work plan, not a record of completed contributions; the group should replace placeholders with actual names and links only after confirming them.

| Member | Primary files | Responsibility |
|---|---|---|
| Member 1 | `lexer.l` | Lexical rules, keywords, literals, comments, line tracking, invalid characters. |
| Member 2 | `parser.y`, `docs/cfg_and_grammar.md` | CFG, grammar transformations, precedence, syntax diagnostics, parser actions. |
| Member 3 | `ast.h`, `ast.c` | AST types, constructors, printing, ownership, memory cleanup. |
| Member 4 | `semantic.h`, `semantic.c` | Symbol table, scopes, declaration/use checks, semantic diagnostics. |
| Member 5 | `main.c`, `Makefile` | Integration, command-line behavior, build rules, cleanup. |
| Member 6 | `tests/`, `README.md`, documentation | Test cases, automation, expected behavior, project documentation. |

Every member should also contribute reviewable commits to the report, presentation, and GitHub history. Do not list student names or claim work until the group agrees on the actual contribution record.

## Recommended evidence

- One or more focused commits on the member's branch.
- A pull request describing the change and its tests.
- Review comments or approvals from another member.
- A short section in the final report describing the verified work.
