import sys

error_code = 0

def scan(file_contents):
    global error_code
    length = len(file_contents)

    i = 0
    while i < length:
        syntas = file_contents[i]

        match syntas:
            case "/":
                if i < length - 1 and file_contents[i + 1] == "/":
                    i += 1
                    while i < length and file_contents[i] != "\n":
                        i += 1
                else:
                    print("SLASH / null")
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
            case "!":
                if i < length - 1 and file_contents[i + 1] == "=":
                    print("BANG_EQUAL != null")
                    i += 1
                else:
                    print("BANG ! null")
            case "=":
                if i < length - 1 and file_contents[i + 1] == "=":
                    print("EQUAL_EQUAL == null")
                    i += 1 
                else:
                    print("EQUAL = null")
            case "<":
                if i < length - 1 and file_contents[i + 1] == "=":
                    print("LESS_EQUAL <= null")
                    i += 1
                else:
                    print("LESS < null")
            case ">":
                if i < length - 1 and file_contents[i + 1] == "=":
                    print("GREATER_EQUAL >= null")
                    i += 1
                else:
            case "\t":
                print("TAB \\t null")
            case " ":
                pass
            case _:
                error_code = 65
                line_number = file_contents.count("\n", 0, i) + 1
                print(
                    f"[line {line_number}] Error: Unexpected character: {syntas}",
                    file=sys.stderr,
                )

        i += 1

def main():
    # Debug print statement
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

    # Process file contents if not empty
    if file_contents:
        scan(file_contents)
        print("EOF  null")
        exit(error_code)
    else:
        print("EOF  null")
        exit(0)

if __name__ == "__main__":
    main()