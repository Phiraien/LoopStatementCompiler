# Viva Questions and Short Answers

1. **What is the role of the lexer?** It converts characters into tokens and reports invalid characters.
2. **What is the role of the parser?** It checks whether the token sequence follows the grammar and builds the AST.
3. **Why use an AST?** It removes unnecessary punctuation details while preserving program structure for later analysis.
4. **What is the difference between syntax and semantic errors?** Syntax errors violate the grammar; semantic errors use syntactically valid constructs incorrectly, such as an undeclared variable.
5. **Why is the language subset documented?** Full C is much larger; a precise subset makes behavior testable and honest.
6. **How are nested scopes represented?** The semantic analyzer pushes a scope for blocks and searches the current scope followed by its parents.
7. **What does a `for` node contain?** Initialization, condition, update, and body children.
8. **Why are precedence declarations needed?** They resolve how expressions such as `a + b * c` are grouped.
9. **How are duplicate declarations detected?** The analyzer checks only the current scope before inserting a symbol.
10. **How are undeclared identifiers detected?** Identifier uses and assignment targets are looked up through the scope chain.
11. **Why should semantic analysis not run after a parse failure?** The AST may be incomplete, so semantic diagnostics would be misleading.
12. **Does this project generate machine code?** No. It is a compiler front end only.
13. **How is memory managed?** AST constructors own nodes, and `ast_free` recursively releases the tree after analysis.
14. **What happens if the toolchain is unavailable?** The repository reports the missing prerequisites instead of claiming unverified build results.
15. **How could the project be extended?** Add richer types, control-flow statements, intermediate representation, optimization, and code generation.
