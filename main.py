from lexer import tokenize
from parser import Parser
from semantic import SemanticAnalyzer


def compile_code(code):
    result = {"success": False, "tokens": [], "ast": None, "message": ""}
    try:
        tokens = tokenize(code)
        result["tokens"] = tokens
        ast = Parser(tokens).parse()
        result["ast"] = ast
        SemanticAnalyzer().analyze(ast)
        result["success"] = True
        result["message"] = "Compilation Successful! No lexical, syntax or semantic errors."
    except (SyntaxError, ValueError) as error:
        result["message"] = str(error)
    return result


if __name__ == "__main__":
    print("================================")
    print("     LOOP STATEMENT COMPILER")
    print("================================")
    print("Enter your program.")
    print("Type END on a new line to compile.\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    result = compile_code("\n".join(lines))
    print("\n------ TOKENS ------")
    for token in result["tokens"]:
        print(token)
    print("\n------ AST ------")
    print(result["ast"])
    print("\n------ RESULT ------")
    print(result["message"])
