#ifndef LOOP_SEMANTIC_H
#define LOOP_SEMANTIC_H
#include "ast.h"
int semantic_check(const AstNode *root, FILE *diagnostics);
#endif
