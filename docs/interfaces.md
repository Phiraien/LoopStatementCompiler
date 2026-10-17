# Module interfaces

## Lexer (`lexer.l`)

- Input: `yyin` (`FILE *`), defaulting to stdin.
- Output: Bison token values through `yylex`, including `NUMBER` (`yylval.intval`) and `IDENT` (`yylval.str`).
- Ownership: identifier strings are heap-allocated by the lexer and consumed by AST constructors.
- Diagnostics: `yylineno` is maintained by Flex.

## Parser (`parser.y`)

- Entry point: `int yyparse(void)`.
- Output: global `AstNode *ast_root`; null or incomplete when parsing fails.
- Error callback: `yyerror(const char *)` writes a line-numbered diagnostic to stderr.
- The parser owns temporary semantic values until AST constructors copy/free them.

## AST (`ast.h` / `ast.c`)

- Constructors create heap-owned nodes and duplicate identifier names.
- `ast_append` links statement lists using `next`.
- `ast_print` emits a stable, indented debug representation.
- `ast_free` recursively releases a complete tree/list.
- AST nodes preserve the source line at which their construct begins.

## Semantic checker (`semantic.h` / `semantic.c`)

`int semantic_check(const AstNode *root, FILE *diagnostics)` returns 0 when no errors are found and 1 otherwise. It checks duplicate declarations in the current scope, use before declaration, and assignment to undeclared names. Blocks and `for` statements create scopes.

## CLI (`main.c`)

`loopcc [-t] [source.c]` reads stdin or a named source file, parses it, runs semantic checks, and returns 0 on success, 1 for syntax/semantic failure, and 2 for command-line or file-open errors. `-t` prints the AST after successful analysis.

## Build contract

The Makefile invokes `bison -d` to produce `parser.tab.c/.h`, `flex` to produce `lex.yy.c`, then compiles and links the C modules. Generated files and binaries are ignored by Git.
