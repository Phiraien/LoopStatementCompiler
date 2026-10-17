CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -pedantic -O2
TARGET = loopcc
GENERATED = parser.tab.c parser.tab.h lex.yy.c
OBJS = parser.tab.o lex.yy.o ast.o semantic.o main.o

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

parser.tab.c parser.tab.h: parser.y ast.h
	bison -d -Wall -o parser.tab.c parser.y

lex.yy.c: lexer.l parser.tab.h
	flex -o $@ lexer.l

%.o: %.c ast.h semantic.h
	$(CC) $(CFLAGS) -c $< -o $@

check: all
	./loopcc tests/valid_for.c
	./loopcc tests/valid_while.c
	./loopcc tests/valid_do_while.c
	! ./loopcc tests/invalid_syntax.c
	! ./loopcc tests/invalid_semantic.c
	./loopcc tests/valid/basic.c
	./loopcc tests/valid/nested.c
	! ./loopcc tests/invalid/undeclared.c
	! ./loopcc tests/invalid/redeclaration.c

test:
	sh tests/run_tests.sh

clean:
	rm -f $(TARGET) $(OBJS) $(GENERATED)

.PHONY: all check test clean
