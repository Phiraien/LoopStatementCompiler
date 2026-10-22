from ast_nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def match(self, token_type):
        if self.current()[0] == token_type:
            value = self.current()[1]
            self.pos += 1
            return value
        raise SyntaxError(f"Expected {token_type}, but found {self.current()[1]!r}")

    def parse(self):
        statements = []
        while self.current()[0] != "EOF":
            statements.append(self.statement())
        return Block(statements)

    def statement(self):
        token = self.current()[0]
        if token == "FOR":
            return self.for_loop()
        if token == "WHILE":
            return self.while_loop()
        if token == "DO":
            return self.do_while_loop()
        if token == "INT":
            node = self.declaration()
            self.match("SEMICOLON")
            return node
        if token == "ID":
            node = self.assignment_or_update()
            self.match("SEMICOLON")
            return node
        if token == "LBRACE":
            return self.block()
        raise SyntaxError(f"Unexpected token: {self.current()[1]!r}")

    def block(self):
        self.match("LBRACE")
        statements = []
        while self.current()[0] not in ("RBRACE", "EOF"):
            statements.append(self.statement())
        self.match("RBRACE")
        return Block(statements)

    def declaration(self):
        self.match("INT")
        name = self.match("ID")
        value = None
        if self.current()[0] == "ASSIGN":
            self.match("ASSIGN")
            value = self.expression()
        return Declaration(name, value)

    def assignment_or_update(self):
        name = self.match("ID")
        if self.current()[0] in ("INC", "DEC"):
            operator = self.current()[1]
            self.pos += 1
            return Update(name, operator)
        self.match("ASSIGN")
        return Assignment(name, self.expression())

    def for_loop(self):
        self.match("FOR")
        self.match("LPAREN")
        initialization = self.declaration() if self.current()[0] == "INT" else self.assignment_or_update()
        self.match("SEMICOLON")
        condition = self.condition()
        self.match("SEMICOLON")
        update = self.assignment_or_update()
        self.match("RPAREN")
        return ForLoop(initialization, condition, update, self.block())

    def while_loop(self):
        self.match("WHILE")
        self.match("LPAREN")
        condition = self.condition()
        self.match("RPAREN")
        return WhileLoop(condition, self.block())

    def do_while_loop(self):
        self.match("DO")
        body = self.block()
        self.match("WHILE")
        self.match("LPAREN")
        condition = self.condition()
        self.match("RPAREN")
        self.match("SEMICOLON")
        return DoWhileLoop(body, condition)

    def condition(self):
        left = self.expression()
        operators = ("LT", "GT", "LE", "GE", "EQ", "NE")
        if self.current()[0] not in operators:
            raise SyntaxError("Expected comparison operator in condition")
        operator = self.current()[1]
        self.pos += 1
        return BinaryOp(left, operator, self.expression())

    def expression(self):
        left = self.term()
        while self.current()[0] in ("PLUS", "MINUS"):
            operator = self.current()[1]
            self.pos += 1
            left = BinaryOp(left, operator, self.term())
        return left

    def term(self):
        left = self.factor()
        while self.current()[0] in ("MUL", "DIV"):
            operator = self.current()[1]
            self.pos += 1
            left = BinaryOp(left, operator, self.factor())
        return left

    def factor(self):
        token_type, value = self.current()
        if token_type == "NUMBER":
            self.pos += 1
            return Number(int(value))
        if token_type == "ID":
            self.pos += 1
            return Variable(value)
        if token_type == "LPAREN":
            self.match("LPAREN")
            node = self.expression()
            self.match("RPAREN")
            return node
        raise SyntaxError(f"Invalid expression near {value!r}")
