from ast_nodes import *


class SemanticAnalyzer:
    def __init__(self):
        self.scopes = [{}]

    def declare(self, name, initialized):
        scope = self.scopes[-1]
        if name in scope:
            raise ValueError(f"Variable '{name}' already declared")
        scope[name] = initialized

    def find_scope(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope
        raise ValueError(f"Variable '{name}' is not declared")

    def check_expression(self, node):
        if isinstance(node, Number):
            return
        if isinstance(node, Variable):
            scope = self.find_scope(node.name)
            if not scope[node.name]:
                raise ValueError(f"Variable '{node.name}' used before initialization")
        elif isinstance(node, BinaryOp):
            self.check_expression(node.left)
            self.check_expression(node.right)

    def analyze(self, node):
        if isinstance(node, Block):
            self.scopes.append({})
            try:
                for statement in node.statements:
                    self.analyze(statement)
            finally:
                self.scopes.pop()
        elif isinstance(node, Declaration):
            if node.value is not None:
                self.check_expression(node.value)
            self.declare(node.name, node.value is not None)
        elif isinstance(node, Assignment):
            scope = self.find_scope(node.name)
            self.check_expression(node.value)
            scope[node.name] = True
        elif isinstance(node, Update):
            scope = self.find_scope(node.name)
            if not scope[node.name]:
                raise ValueError(f"Variable '{node.name}' used before initialization")
        elif isinstance(node, ForLoop):
            self.scopes.append({})
            try:
                self.analyze(node.initialization)
                self.check_expression(node.condition)
                self.analyze(node.update)
                self.analyze(node.body)
            finally:
                self.scopes.pop()
        elif isinstance(node, WhileLoop):
            self.check_expression(node.condition)
            self.analyze(node.body)
        elif isinstance(node, DoWhileLoop):
            self.analyze(node.body)
            self.check_expression(node.condition)
