import sys

def main():
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

    line = 1
    error = False
    length = len(file_contents)
    i = 0

    while i < length:
        c = file_contents[i]
        
        if c == "\n":
            line += 1
        elif c == " " or c == "\r" or c == "\t":
            pass
        elif c == "(":
            print("LEFT_PAREN ( null")
        elif c == ")":
            print("RIGHT_PAREN ) null")
        elif c == "{":
            print("LEFT_BRACE { null")
        elif c == "}":
            print("RIGHT_BRACE } null")
        elif c == ",":
            print("COMMA , null")
        elif c == ";":
            print("SEMICOLON ; null")
        elif c == ".":
            print("DOT . null")
        elif c == "-":
            print("MINUS - null")
        elif c == "+":
            print("PLUS + null")
        elif c == "*":
            print("STAR * null")
        elif c == "=":
            if i + 1 < length and file_contents[i + 1] == "=":
                i += 1
                print("EQUAL_EQUAL == null")
            else:
                print("EQUAL = null")
        elif c == "!":
            if i + 1 < length and file_contents[i + 1] == "=":
                i += 1
                print("BANG_EQUAL != null")
            else:
                print("BANG ! null")
        elif c == "<":
            if i + 1 < length and file_contents[i + 1] == "=":
                i += 1
                print("LESS_EQUAL <= null")
            else:
                print("LESS < null")
        elif c == ">":
            if i + 1 < length and file_contents[i + 1] == "=":
                i += 1
                print("GREATER_EQUAL >= null")
            else:
                print("GREATER > null")
        elif c == "/":
            if i + 1 < length and file_contents[i + 1] == "/":
                i += 1
                while i < length and file_contents[i] != "\n":
                    i += 1
                    line += 1
            else:
                print("SLASH / null")
        else:
            print(f"[line {line}] Error: Unexpected character: {c}", file=sys.stderr)
            error = True

        i += 1

    print("EOF  null")

    if error:
        exit(65)
    else:
        exit(0)

if __name__ == "__main__":
    main()