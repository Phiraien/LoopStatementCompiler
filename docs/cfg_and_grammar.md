# CFG and Grammar Transformations

## Supported language subset

A program is one outer block. The subset supports `int` declarations, assignments, integer expressions, and nested `for`, `while`, and `do-while` statements. It intentionally excludes functions, arrays, pointers, floating-point values, `break`, and `continue`.

## Context-free grammar

```text
program          -> block
block            -> '{' statements '}'
statements       -> ε | statements statement
statement        -> block | declaration | expression_statement
                  | for_statement | while_statement | do_statement
declaration      -> 'int' IDENT ';'
                  | 'int' IDENT '=' expression ';'
expression_statement -> ';' | assignment_expr ';'
for_statement    -> 'for' '(' for_init for_condition for_update ')' statement
for_init         -> ';' | declaration | assignment_expr ';'
for_condition    -> ';' | assignment_expr ';'
for_update       -> ε | assignment_expr
while_statement  -> 'while' '(' expression ')' statement
do_statement     -> 'do' statement 'while' '(' expression ')' ';'
assignment_expr  -> IDENT '=' expression | expression
expression       -> primary | expression operator expression
                  | '-' expression | '!' expression
primary          -> NUMBER | IDENT | '(' assignment_expr ')'
```

The Bison file adds precedence and associativity declarations to resolve arithmetic and comparison expressions. The grammar is intentionally smaller than ISO C so it remains suitable for a mini-project demonstration.

## Grammar transformations

1. **Left recursion for lists:** `statements` is left-recursive so Bison can append statements in source order without an artificial list production.
2. **Expression precedence:** one compact expression nonterminal is used with `%left` and `%right` declarations for `+`, `*`, comparisons, unary minus, and logical not.
3. **Optional loop components:** `for_init` and `for_condition` explicitly include the semicolon that terminates each component; `for_update` is nullable because the update expression may be omitted.
4. **Dangling-else avoidance:** `if` is not part of this subset, so the classic dangling-else ambiguity does not arise.

## Examples

```c
{
    int i = 0;
    for (; i < 3; i = i + 1) {
        while (i < 2) { i = i + 1; }
    }
}
```

The parser builds nodes for the declaration, loop condition, update assignment, and nested loop body. Semantic analysis then validates identifier declarations and uses.
