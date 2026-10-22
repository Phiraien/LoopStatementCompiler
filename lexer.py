import re

TOKEN_SPEC = [
    ("COMMENT",   r"//[^\n]*|/\*[\s\S]*?\*/"),
    ("FOR",       r"\bfor\b"),
    ("WHILE",     r"\bwhile\b"),
    ("DO",        r"\bdo\b"),
    ("INT",       r"\bint\b"),
    ("NUMBER",    r"\d+"),
    ("ID",        r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("INC",       r"\+\+"),
    ("DEC",       r"--"),
    ("EQ",        r"=="),
    ("NE",        r"!="),
    ("LE",        r"<="),
    ("GE",        r">="),
    ("ASSIGN",    r"="),
    ("LT",        r"<"),
    ("GT",        r">"),
    ("PLUS",      r"\+"),
    ("MINUS",     r"-"),
    ("MUL",       r"\*"),
    ("DIV",       r"/"),
    ("LPAREN",    r"\("),
    ("RPAREN",    r"\)"),
    ("LBRACE",    r"\{"),
    ("RBRACE",    r"\}"),
    ("SEMICOLON", r";"),
    ("SKIP",      r"[ \t\r\n]+"),
    ("MISMATCH",  r"."),
]

TOKEN_REGEX = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))


def tokenize(code):
    """Return (token_type, value) pairs and raise on invalid characters."""
    tokens = []
    line = 1
    position = 0

    for match in TOKEN_REGEX.finditer(code):
        if match.start() != position:
            raise SyntaxError(f"Invalid character near line {line}")
        position = match.end()
        token_type = match.lastgroup
        value = match.group()
        line += value.count("\n")

        if token_type in ("SKIP", "COMMENT"):
            continue
        if token_type == "MISMATCH":
            raise SyntaxError(f"Invalid character: {value}")
        tokens.append((token_type, value))

    if position != len(code):
        raise SyntaxError(f"Invalid character near line {line}")
    tokens.append(("EOF", ""))
    return tokens
