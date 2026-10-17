#include "ast.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static AstNode *make(AstKind kind, int line) {
    AstNode *node = calloc(1, sizeof(*node));
    if (node) {
        node->kind = kind;
        node->line = line;
    }
    return node;
}

static char *copy_text(char *text) {
    size_t size;
    char *copy;

    if (!text) return NULL;
    size = strlen(text) + 1;
    copy = malloc(size);
    if (copy) memcpy(copy, text, size);
    return copy;
}

AstNode *ast_block(AstNode *items, int line) {
    AstNode *node = make(AST_BLOCK, line);
    if (node) node->data.block.items = items;
    return node;
}

AstNode *ast_decl(char *name, AstNode *initializer, int line) {
    AstNode *node = make(AST_DECL, line);
    if (node) {
        node->data.decl.name = copy_text(name);
        node->data.decl.initializer = initializer;
    }
    free(name);
    return node;
}

AstNode *ast_assign(char *name, AstNode *value, int line) {
    AstNode *node = make(AST_ASSIGN, line);
    if (node) {
        node->data.assign.name = copy_text(name);
        node->data.assign.value = value;
    }
    free(name);
    return node;
}

AstNode *ast_expr_stmt(AstNode *expr, int line) {
    AstNode *node = make(AST_EXPR_STMT, line);
    if (node) node->data.expr_stmt.expr = expr;
    return node;
}

AstNode *ast_for(AstNode *init, AstNode *condition, AstNode *update,
                 AstNode *body, int line) {
    AstNode *node = make(AST_FOR, line);
    if (node) {
        node->data.for_loop.init = init;
        node->data.for_loop.condition = condition;
        node->data.for_loop.update = update;
        node->data.for_loop.body = body;
    }
    return node;
}

AstNode *ast_while(AstNode *condition, AstNode *body, int line) {
    AstNode *node = make(AST_WHILE, line);
    if (node) {
        node->data.loop.condition = condition;
        node->data.loop.body = body;
    }
    return node;
}

AstNode *ast_do_while(AstNode *condition, AstNode *body, int line) {
    AstNode *node = make(AST_DO_WHILE, line);
    if (node) {
        node->data.loop.condition = condition;
        node->data.loop.body = body;
    }
    return node;
}

AstNode *ast_int(int value, int line) {
    AstNode *node = make(AST_INT, line);
    if (node) node->data.integer.value = value;
    return node;
}

AstNode *ast_ident(char *name, int line) {
    AstNode *node = make(AST_IDENT, line);
    if (node) node->data.ident.name = copy_text(name);
    free(name);
    return node;
}

AstNode *ast_binary(AstOp op, AstNode *left, AstNode *right, int line) {
    AstNode *node = make(AST_BINARY, line);
    if (node) {
        node->data.binary.op = op;
        node->data.binary.left = left;
        node->data.binary.right = right;
    }
    return node;
}

AstNode *ast_unary(AstOp op, AstNode *operand, int line) {
    AstNode *node = make(AST_UNARY, line);
    if (node) {
        node->data.unary.op = op;
        node->data.unary.operand = operand;
    }
    return node;
}

AstNode *ast_append(AstNode *list, AstNode *node) {
    AstNode *current;

    if (!list) return node;
    current = list;
    while (current->next) current = current->next;
    current->next = node;
    return list;
}

static const char *op_name(AstOp op) {
    static const char *names[] = {
        "+", "-", "*", "/", "%", "<", "<=", ">", ">=", "==", "!=", "-", "!"
    };
    return names[op];
}

static void print_node(const AstNode *node, const char *prefix, int is_last,
                       FILE *out);

static void print_branch(FILE *out, const char *prefix, int is_last) {
    fputs(prefix, out);
    fputs(is_last ? "└── " : "├── ", out);
}

static void child_prefix(char *buffer, size_t size, const char *prefix,
                         int is_last) {
    snprintf(buffer, size, "%s%s", prefix, is_last ? "    " : "│   ");
}

static void print_list(const AstNode *node, const char *prefix, FILE *out) {
    while (node) {
        print_node(node, prefix, node->next == NULL, out);
        node = node->next;
    }
}

static void print_labeled_child(const char *label, const AstNode *child,
                                const char *prefix, int is_last, FILE *out) {
    char next_prefix[1024];

    print_branch(out, prefix, is_last);
    fprintf(out, "%s%s\n", label, child ? "" : ": (empty)");
    if (!child) return;
    child_prefix(next_prefix, sizeof(next_prefix), prefix, is_last);
    print_node(child, next_prefix, 1, out);
}

static void print_node(const AstNode *node, const char *prefix, int is_last,
                       FILE *out) {
    char next_prefix[1024];

    if (!node) return;
    print_branch(out, prefix, is_last);

    switch (node->kind) {
        case AST_BLOCK:
            fputs("Block\n", out);
            child_prefix(next_prefix, sizeof(next_prefix), prefix, is_last);
            print_list(node->data.block.items, next_prefix, out);
            break;

        case AST_DECL:
            fprintf(out, "Declaration: %s\n", node->data.decl.name);
            if (node->data.decl.initializer) {
                child_prefix(next_prefix, sizeof(next_prefix), prefix, is_last);
                print_node(node->data.decl.initializer, next_prefix, 1, out);
            }
            break;

        case AST_ASSIGN:
            fprintf(out, "Assignment: %s\n", node->data.assign.name);
            child_prefix(next_prefix, sizeof(next_prefix), prefix, is_last);
            print_node(node->data.assign.value, next_prefix, 1, out);
            break;

        case AST_EXPR_STMT:
            fputs("Expression Statement\n", out);
            if (node->data.expr_stmt.expr) {
                child_prefix(next_prefix, sizeof(next_prefix), prefix, is_last);
                print_node(node->data.expr_stmt.expr, next_prefix, 1, out);
            }
            break;

        case AST_FOR:
            fputs("For Loop\n", out);
            child_prefix(next_prefix, sizeof(next_prefix), prefix, is_last);
            print_labeled_child("Initialization", node->data.for_loop.init,
                                next_prefix, 0, out);
            print_labeled_child("Condition", node->data.for_loop.condition,
                                next_prefix, 0, out);
            print_labeled_child("Update", node->data.for_loop.update,
                                next_prefix, 0, out);
            print_labeled_child("Body", node->data.for_loop.body,
                                next_prefix, 1, out);
            break;

        case AST_WHILE:
            fputs("While Loop\n", out);
            child_prefix(next_prefix, sizeof(next_prefix), prefix, is_last);
            print_labeled_child("Condition", node->data.loop.condition,
                                next_prefix, 0, out);
            print_labeled_child("Body", node->data.loop.body,
                                next_prefix, 1, out);
            break;

        case AST_DO_WHILE:
            fputs("Do-While Loop\n", out);
            child_prefix(next_prefix, sizeof(next_prefix), prefix, is_last);
            print_labeled_child("Body", node->data.loop.body,
                                next_prefix, 0, out);
            print_labeled_child("Condition", node->data.loop.condition,
                                next_prefix, 1, out);
            break;

        case AST_BINARY:
            fprintf(out, "Binary Expression: %s\n", op_name(node->data.binary.op));
            child_prefix(next_prefix, sizeof(next_prefix), prefix, is_last);
            print_node(node->data.binary.left, next_prefix, 0, out);
            print_node(node->data.binary.right, next_prefix, 1, out);
            break;

        case AST_UNARY:
            fprintf(out, "Unary Expression: %s\n", op_name(node->data.unary.op));
            child_prefix(next_prefix, sizeof(next_prefix), prefix, is_last);
            print_node(node->data.unary.operand, next_prefix, 1, out);
            break;

        case AST_IDENT:
            fprintf(out, "Identifier: %s\n", node->data.ident.name);
            break;

        case AST_INT:
            fprintf(out, "Integer: %d\n", node->data.integer.value);
            break;
    }
}

void ast_print(const AstNode *node, FILE *out, int indent) {
    (void)indent;
    fputs("Program\n", out);
    if (node) print_node(node, "", 1, out);
}

void ast_free(AstNode *node) {
    while (node) {
        AstNode *next = node->next;

        switch (node->kind) {
            case AST_BLOCK:
                ast_free(node->data.block.items);
                break;
            case AST_DECL:
                free(node->data.decl.name);
                ast_free(node->data.decl.initializer);
                break;
            case AST_ASSIGN:
                free(node->data.assign.name);
                ast_free(node->data.assign.value);
                break;
            case AST_EXPR_STMT:
                ast_free(node->data.expr_stmt.expr);
                break;
            case AST_FOR:
                ast_free(node->data.for_loop.init);
                ast_free(node->data.for_loop.condition);
                ast_free(node->data.for_loop.update);
                ast_free(node->data.for_loop.body);
                break;
            case AST_WHILE:
            case AST_DO_WHILE:
                ast_free(node->data.loop.condition);
                ast_free(node->data.loop.body);
                break;
            case AST_IDENT:
                free(node->data.ident.name);
                break;
            case AST_BINARY:
                ast_free(node->data.binary.left);
                ast_free(node->data.binary.right);
                break;
            case AST_UNARY:
                ast_free(node->data.unary.operand);
                break;
            case AST_INT:
                break;
        }
        free(node);
        node = next;
    }
}
