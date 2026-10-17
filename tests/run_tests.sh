#!/bin/sh
set -u
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
missing=""
for tool in flex bison cc make; do
  if ! command -v "$tool" >/dev/null 2>&1; then missing="$missing $tool"; fi
done
if [ -n "$missing" ]; then
  printf 'SKIP: missing required tool(s):%s\n' "$missing" >&2
  printf 'Install Flex, Bison, a C compiler, and make, then rerun this script.\n' >&2
  exit 2
fi
cd "$root" || exit 2
rm -f loopcc parser.tab.c parser.tab.h lex.yy.c *.o
make all
pass=0; fail=0
run_expect(){ label=$1; expected=$2; file=$3; if ./loopcc "$file" >/dev/null 2>&1; then status=0; else status=$?; fi; if [ "$status" -eq "$expected" ]; then printf 'PASS %s\n' "$label"; pass=$((pass+1)); else printf 'FAIL %s (expected %s, got %s)\n' "$label" "$expected" "$status"; fail=$((fail+1)); fi; }
run_expect valid-for 0 tests/valid_for.c
run_expect valid-while 0 tests/valid_while.c
run_expect valid-do-while 0 tests/valid_do_while.c
run_expect invalid-syntax 1 tests/invalid_syntax.c
run_expect invalid-semantic 1 tests/invalid_semantic.c
run_expect valid-basic 0 tests/valid/basic.c
run_expect valid-nested 0 tests/valid/nested.c
run_expect invalid-undeclared 1 tests/invalid/undeclared.c
run_expect invalid-redeclaration 1 tests/invalid/redeclaration.c
printf 'Summary: %s passed, %s failed.\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
