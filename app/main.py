import sys
error_code = 0
def scan(file_contents):
    global error_code
    for syntas in file_contents:
        match syntas:
            case "(":
                print("LEFT_PAREN ( null")
            case ")":
                print("RIGHT_PAREN ) null")
            case "{":
                print("LEFT_BRACE { null")
            case "}":
                print("RIGHT_BRACE } null")
            case "*":
                print("STAR * null")
            case ".":
                print("DOT . null")
            case ",":
                print("COMMA , null")
            case "+":
                print("PLUS + null")
            case "-":
                print("MINUS - null")
            case ";":
                print("SEMICOLON ; null")
            case "/":
                print("SLASH / null")
            case "==":
                print("EQUAL_EQUAL == null")
            case "=":
                print("EQUAL = null")

            case _:
                error_code = 65
                line_number = (
                    file_contents.count("\n", 0, file_contents.find(syntas)) + 1
                )
                print(
                    f"[line {line_number}] Error: Unexpected character: {syntas}",
                    file=sys.stderr,
                )
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)
    command = sys.argv[1]
    filename = sys.argv[2]
    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)
    with open(filename) as file:
        file_contents = file.read()
    # Uncomment this block to pass the first stage
    if file_contents:
        scan(file_contents)
        print("EOF  null")
        exit(error_code)
    else:
        print(
            "EOF  null"
        )  # Placeholder, remove this line when implementing the scanner
if __name__ == "__main__":
    main()