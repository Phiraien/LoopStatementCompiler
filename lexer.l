%option noyywrap yylineno
%{
#include "parser.tab.h"
#include <stdlib.h>
#include <string.h>
static char *copy_lexeme(const char *s) { size_t n=strlen(s)+1; char *p=malloc(n); if(p) memcpy(p,s,n); return p; }
%}
%%
[ \t\r]+                 ;
"//"[^\n]*               ;
\/\*([^*]|\*+[^*/])*\*\/  ;
\n                       ;
"int"                    return INT;
"for"                    return FOR;
"while"                  return WHILE;
"do"                     return DO;
"=="                     return EQ;
"!="                     return NE;
"<="                     return LE;
">="                     return GE;
[0-9]+                   { yylval.intval=(int)strtol(yytext,NULL,10); return NUMBER; }
[a-zA-Z_][a-zA-Z0-9_]*  { yylval.str=copy_lexeme(yytext); return IDENT; }
.                        return yytext[0];
%%
