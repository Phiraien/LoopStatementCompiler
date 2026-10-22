from dataclasses import dataclass


@dataclass
class Number:
    value: int


@dataclass
class Variable:
    name: str


@dataclass
class BinaryOp:
    left: object
    operator: str
    right: object


@dataclass
class Declaration:
    name: str
    value: object


@dataclass
class Assignment:
    name: str
    value: object


@dataclass
class Update:
    name: str
    operator: str


@dataclass
class Block:
    statements: list


@dataclass
class ForLoop:
    initialization: object
    condition: object
    update: object
    body: Block


@dataclass
class WhileLoop:
    condition: object
    body: Block


@dataclass
class DoWhileLoop:
    body: Block
    condition: object
