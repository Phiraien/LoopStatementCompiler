# Compiler Architecture

```text
source.c
   |
   v
Flex lexer (lexer.l) ---- invalid-character diagnostics
   |
   v
Bison parser (parser.y) -- syntax diagnostics
   |
   v
AST (ast.c / ast.h)
   |
   v
Semantic analyzer (semantic.c / semantic.h)
   |
   v
CLI report (main.c)
```

## Lexical analysis

Flex recognizes keywords, identifiers, integer literals, operators, delimiters, comments, and whitespace. `yylineno` supplies source-line information. Unknown characters are returned to Bison and become syntax errors at the current line.

## Syntax analysis

Bison validates the loop-oriented grammar and constructs an AST directly from parser actions. A parse failure prevents semantic analysis from running, so a malformed program is not mislabeled as a semantic failure.

## AST representation

Every AST node contains a kind, source line, and optional `next` pointer for statement lists. Loop nodes own their initialization, condition, update, and body nodes. `ast_free` recursively releases the complete tree.

## Semantic analysis

The analyzer creates lexical scopes for blocks and `for` statements. It reports duplicate declarations in the current scope, undeclared identifier uses, and assignments to undeclared identifiers. The current type domain is integer-only, so basic type validation is represented by the grammar and AST design rather than a separate type lattice.

## Ownership rules

Parser-created identifier strings are copied into AST nodes and then released by AST constructors. The AST owns all child nodes after construction. The caller owns the root and must call `ast_free` exactly once.

## Deliberate limitations

This is a front end, not a complete compiler: it has no code generation, optimization, runtime execution, function declarations, arrays, pointers, floating-point types, or control-flow statements outside the requested loop forms.
