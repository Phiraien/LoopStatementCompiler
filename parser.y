%{
#include "ast.h"
#include <stdio.h>
#include <stdlib.h>
AstNode *ast_root = NULL;
int yylex(void);
void yyerror(const char *message);
extern int yylineno;
%}
%code requires { #include "ast.h" }
%union { int intval; char *str; AstNode *node; }
%token INT FOR WHILE DO
%token <intval> NUMBER
%token <str> IDENT
%token EQ NE LE GE
%type <node> program block statements statement declaration expression_statement for_statement while_statement do_statement expression assignment_expr primary for_init for_condition for_update
%left EQ NE '<' '>' LE GE
%left '+' '-'
%left '*' '/' '%'
%precedence '!' UMINUS
%%
program: block { ast_root=$1; };
block: '{' statements '}' { $$=ast_block($2,@1.first_line); };
statements: %empty { $$=NULL; } | statements statement { $$=ast_append($1,$2); };
statement: block { $$=$1; } | declaration { $$=$1; } | expression_statement { $$=$1; } | for_statement { $$=$1; } | while_statement { $$=$1; } | do_statement { $$=$1; };
declaration: INT IDENT ';' { $$=ast_decl($2,NULL,@1.first_line); } | INT IDENT '=' expression ';' { $$=ast_decl($2,$4,@1.first_line); };
expression_statement: ';' { $$=ast_expr_stmt(NULL,@1.first_line); } | assignment_expr ';' { $$=ast_expr_stmt($1,@1.first_line); };
for_statement: FOR '(' for_init for_condition for_update ')' statement { $$=ast_for($3,$4?$4->data.expr_stmt.expr:NULL,$5,$7,@1.first_line); };
for_init: ';' { $$=NULL; } | declaration { $$=$1; } | assignment_expr ';' { $$=ast_expr_stmt($1,@1.first_line); };
for_condition: ';' { $$=ast_expr_stmt(NULL,@1.first_line); } | assignment_expr ';' { $$=ast_expr_stmt($1,@1.first_line); };
for_update: %empty { $$=NULL; } | assignment_expr { $$=$1; };
while_statement: WHILE '(' expression ')' statement { $$=ast_while($3,$5,@1.first_line); };
do_statement: DO statement WHILE '(' expression ')' ';' { $$=ast_do_while($5,$2,@1.first_line); };
assignment_expr: IDENT '=' expression { $$=ast_assign($1,$3,@1.first_line); } | expression { $$=$1; };
expression: primary { $$=$1; } | expression '+' expression { $$=ast_binary(OP_ADD,$1,$3,@2.first_line); } | expression '-' expression { $$=ast_binary(OP_SUB,$1,$3,@2.first_line); } | expression '*' expression { $$=ast_binary(OP_MUL,$1,$3,@2.first_line); } | expression '/' expression { $$=ast_binary(OP_DIV,$1,$3,@2.first_line); } | expression '%' expression { $$=ast_binary(OP_MOD,$1,$3,@2.first_line); } | expression '<' expression { $$=ast_binary(OP_LT,$1,$3,@2.first_line); } | expression '>' expression { $$=ast_binary(OP_GT,$1,$3,@2.first_line); } | expression LE expression { $$=ast_binary(OP_LE,$1,$3,@2.first_line); } | expression GE expression { $$=ast_binary(OP_GE,$1,$3,@2.first_line); } | expression EQ expression { $$=ast_binary(OP_EQ,$1,$3,@2.first_line); } | expression NE expression { $$=ast_binary(OP_NE,$1,$3,@2.first_line); } | '-' expression %prec UMINUS { $$=ast_unary(OP_NEG,$2,@1.first_line); } | '!' expression { $$=ast_unary(OP_NOT,$2,@1.first_line); };
primary: NUMBER { $$=ast_int($1,@1.first_line); } | IDENT { $$=ast_ident($1,@1.first_line); } | '(' assignment_expr ')' { $$=$2; };
%%
void yyerror(const char *message){fprintf(stderr,"line %d: %s\n",yylineno,message);}
