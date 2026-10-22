#ifndef LOOP_AST_H
#define LOOP_AST_H

#include <stdio.h>

typedef enum {
    AST_BLOCK, AST_DECL, AST_ASSIGN, AST_EXPR_STMT,
    AST_FOR, AST_WHILE, AST_DO_WHILE,
    AST_INT, AST_IDENT, AST_BINARY, AST_UNARY
} AstKind;

typedef enum { OP_ADD, OP_SUB, OP_MUL, OP_DIV, OP_MOD,
               OP_LT, OP_LE, OP_GT, OP_GE, OP_EQ, OP_NE,
               OP_NEG, OP_NOT } AstOp;

typedef struct AstNode AstNode;
struct AstNode {
    AstKind kind;
    int line;
    AstNode *next;
    union {
        struct { AstNode *items; } block;
        struct { char *name; AstNode *initializer; } decl;
        struct { char *name; AstNode *value; } assign;
        struct { AstNode *expr; } expr_stmt;
        struct { AstNode *init; AstNode *condition; AstNode *update; AstNode *body; } for_loop;
        struct { AstNode *condition; AstNode *body; } loop;
        struct { int value; } integer;
        struct { char *name; } ident;
        struct { AstOp op; AstNode *left; AstNode *right; } binary;
        struct { AstOp op; AstNode *operand; } unary;
    } data;
};

AstNode *ast_block(AstNode *items, int line);
AstNode *ast_decl(char *name, AstNode *initializer, int line);
AstNode *ast_assign(char *name, AstNode *value, int line);
AstNode *ast_expr_stmt(AstNode *expr, int line);
AstNode *ast_for(AstNode *init, AstNode *condition, AstNode *update, AstNode *body, int line);
AstNode *ast_while(AstNode *condition, AstNode *body, int line);
AstNode *ast_do_while(AstNode *condition, AstNode *body, int line);
AstNode *ast_int(int value, int line);
AstNode *ast_ident(char *name, int line);
AstNode *ast_binary(AstOp op, AstNode *left, AstNode *right, int line);
AstNode *ast_unary(AstOp op, AstNode *operand, int line);
AstNode *ast_append(AstNode *list, AstNode *node);
void ast_print(const AstNode *node, FILE *out, int indent);
void ast_json_print(const AstNode *node, FILE *out);
void ast_free(AstNode *node);

#endif
