#include "ast.h"
#include "semantic.h"
#include <stdio.h>
#include <string.h>
extern int yyparse(void); extern FILE *yyin; extern AstNode *ast_root; extern int yylineno;
static void usage(const char*p){fprintf(stderr,"usage: %s [-t|-j] [source.c]\n",p);}
int main(int argc,char**argv){int tree=0,json=0;const char*path=NULL;for(int i=1;i<argc;i++){if(!strcmp(argv[i],"-t"))tree=1;else if(!strcmp(argv[i],"-j"))json=1;else if(argv[i][0]=='-'){usage(argv[0]);return 2;}else if(path){usage(argv[0]);return 2;}else path=argv[i];}if(path){yyin=fopen(path,"r");if(!yyin){perror(path);return 2;}}if(yyparse()!=0){if(path)fclose(yyin);ast_free(ast_root);return 1;}int bad=semantic_check(ast_root,stderr);if(!bad){if(json)ast_json_print(ast_root,stdout);else{puts("parse and semantic analysis succeeded");if(tree)ast_print(ast_root,stdout,0);}}ast_free(ast_root);if(path)fclose(yyin);return bad?1:0;}
