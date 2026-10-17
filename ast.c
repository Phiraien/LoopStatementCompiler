#include "ast.h"
#include <stdlib.h>
#include <string.h>

static AstNode *make(AstKind kind, int line) { AstNode *n = calloc(1, sizeof(*n)); if (!n) return NULL; n->kind=kind; n->line=line; return n; }
static char *copy_text(char *s) { size_t n; char *out; if (!s) return NULL; n=strlen(s)+1; out=malloc(n); if (out) memcpy(out,s,n); return out; }
AstNode *ast_block(AstNode *items,int l){AstNode*n=make(AST_BLOCK,l);if(n)n->data.block.items=items;return n;}
AstNode *ast_decl(char*n,AstNode*i,int l){AstNode*x=make(AST_DECL,l);if(x){x->data.decl.name=copy_text(n);x->data.decl.initializer=i;}free(n);return x;}
AstNode *ast_assign(char*n,AstNode*v,int l){AstNode*x=make(AST_ASSIGN,l);if(x){x->data.assign.name=copy_text(n);x->data.assign.value=v;}free(n);return x;}
AstNode *ast_expr_stmt(AstNode*e,int l){AstNode*n=make(AST_EXPR_STMT,l);if(n)n->data.expr_stmt.expr=e;return n;}
AstNode *ast_for(AstNode*i,AstNode*c,AstNode*u,AstNode*b,int l){AstNode*n=make(AST_FOR,l);if(n){n->data.for_loop.init=i;n->data.for_loop.condition=c;n->data.for_loop.update=u;n->data.for_loop.body=b;}return n;}
AstNode *ast_while(AstNode*c,AstNode*b,int l){AstNode*n=make(AST_WHILE,l);if(n){n->data.loop.condition=c;n->data.loop.body=b;}return n;}
AstNode *ast_do_while(AstNode*c,AstNode*b,int l){AstNode*n=make(AST_DO_WHILE,l);if(n){n->data.loop.condition=c;n->data.loop.body=b;}return n;}
AstNode *ast_int(int v,int l){AstNode*n=make(AST_INT,l);if(n)n->data.integer.value=v;return n;}
AstNode *ast_ident(char*n,int l){AstNode*x=make(AST_IDENT,l);if(x){x->data.ident.name=copy_text(n);}free(n);return x;}
AstNode *ast_binary(AstOp o,AstNode*a,AstNode*b,int l){AstNode*n=make(AST_BINARY,l);if(n){n->data.binary.op=o;n->data.binary.left=a;n->data.binary.right=b;}return n;}
AstNode *ast_unary(AstOp o,AstNode*a,int l){AstNode*n=make(AST_UNARY,l);if(n){n->data.unary.op=o;n->data.unary.operand=a;}return n;}
AstNode *ast_append(AstNode*l,AstNode*n){AstNode*p;if(!l)return n;for(p=l;p->next;p=p->next);p->next=n;return l;}
static void pad(FILE*f,int n){while(n-->0)fputs("  ",f);}
static const char *op_name(AstOp o){static const char*s[]={"+","-","*","/","%","<","<=",">",">=","==","!=","-","!"};return s[o];}
void ast_print(const AstNode*n,FILE*f,int d){for(;n;n=n->next){pad(f,d);switch(n->kind){case AST_BLOCK:fputs("block\n",f);ast_print(n->data.block.items,f,d+1);break;case AST_DECL:fprintf(f,"decl %s\n",n->data.decl.name);if(n->data.decl.initializer)ast_print(n->data.decl.initializer,f,d+1);break;case AST_ASSIGN:fprintf(f,"assign %s\n",n->data.assign.name);ast_print(n->data.assign.value,f,d+1);break;case AST_EXPR_STMT:fputs("expr-stmt\n",f);ast_print(n->data.expr_stmt.expr,f,d+1);break;case AST_FOR:fputs("for\n",f);ast_print(n->data.for_loop.init,f,d+1);ast_print(n->data.for_loop.condition,f,d+1);ast_print(n->data.for_loop.update,f,d+1);ast_print(n->data.for_loop.body,f,d+1);break;case AST_WHILE:fputs("while\n",f);ast_print(n->data.loop.condition,f,d+1);ast_print(n->data.loop.body,f,d+1);break;case AST_DO_WHILE:fputs("do-while\n",f);ast_print(n->data.loop.body,f,d+1);ast_print(n->data.loop.condition,f,d+1);break;case AST_INT:fprintf(f,"int %d\n",n->data.integer.value);break;case AST_IDENT:fprintf(f,"ident %s\n",n->data.ident.name);break;case AST_BINARY:fprintf(f,"binary %s\n",op_name(n->data.binary.op));ast_print(n->data.binary.left,f,d+1);ast_print(n->data.binary.right,f,d+1);break;case AST_UNARY:fprintf(f,"unary %s\n",op_name(n->data.unary.op));ast_print(n->data.unary.operand,f,d+1);break;}}}
void ast_free(AstNode*n){while(n){AstNode*x=n->next;switch(n->kind){case AST_BLOCK:ast_free(n->data.block.items);break;case AST_DECL:free(n->data.decl.name);ast_free(n->data.decl.initializer);break;case AST_ASSIGN:free(n->data.assign.name);ast_free(n->data.assign.value);break;case AST_EXPR_STMT:ast_free(n->data.expr_stmt.expr);break;case AST_FOR:ast_free(n->data.for_loop.init);ast_free(n->data.for_loop.condition);ast_free(n->data.for_loop.update);ast_free(n->data.for_loop.body);break;case AST_WHILE:case AST_DO_WHILE:ast_free(n->data.loop.condition);ast_free(n->data.loop.body);break;case AST_IDENT:free(n->data.ident.name);break;case AST_BINARY:ast_free(n->data.binary.left);ast_free(n->data.binary.right);break;case AST_UNARY:ast_free(n->data.unary.operand);break;default:break;}free(n);n=x;}}
