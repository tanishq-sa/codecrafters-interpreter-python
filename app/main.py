import sys
from enum import Enum

IS_ERROR_IN_CODE = False

class TokenType(Enum):
    EOF = 0

    # Literals
    IDENTIFIER = 1
    STRING = 2
    NUMBER = 3

    # Single-character tokens
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"

    # One or two character tokens
    BANG = 15
    BANG_EQUAL = 16
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = 19
    GREATER_EQUAL = 20
    LESS = 21
    LESS_EQUAL = 22

    # Keywords
    AND = 23
    CLASS = 24
    ELSE = 25
    FALSE = 26
    FUN = 27
    FOR = 28
    IF = 29
    NIL = 30
    OR = 31
    PRINT = 32
    RETURN = 33
    SUPER = 34
    THIS = 35
    TRUE = 36
    VAR = 37
    WHILE = 38

KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE
}

class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        if self.literal is not None:
            return f"{self.type.name} {self.lexeme} {self.literal}"
        else:
            return f"{self.type.name} {self.lexeme} null"

    def __repr__(self):
        return self.__str__()

class Scanner:

    def __init__(self, source):
        self.start = 0
        self.current = 0
        self.tokens = []
        self.source = source
        self.had_error = False
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.add_token(TokenType.EOF)

        return self.tokens

    def scan_token(self):
        c = self.advance()
        if c in [" ", "\r", "\t"]:
            pass
        elif c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "\n":
            self.line += 1
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            elif self.match("*"):
                while self.peek() != "*" and self.peek(1) != "/" and not self.is_at_end():
                    self.advance()
                self.advance()
                self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == "!":
            if self.match("="):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif c == "=":
            if self.match("="):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif c == "<":
            if self.match("="):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif c == ">":
            if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif c == '"':
            self.string()
        else:
            if self.is_digit(c):
                self.number()
            elif self.is_alpha(c):
                self.identifier()
            else:
                self.had_error = True
                sys.stderr.write(f"[line {self.line}] Error: Unexpected character: {c}\n")

    # def error(self, line, message):
    #     pass

    def is_digit(self, c):
        return c >= "0" and c <= "9"

    def is_alpha(self, c):
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek(1)):
            self.advance()

        while self.is_digit(self.peek()):
            self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def identifier(self):
        while self.is_alpha(self.peek()) or self.is_digit(self.peek()):
            self.advance()

        text = self.source[self.start : self.current]
        keyword_type = KEYWORDS.get(text)

        if keyword_type == None:
            self.add_token(TokenType.IDENTIFIER)
        else:
            self.add_token(keyword_type)

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.had_error = True
            sys.stderr.write(f"[line {self.line}] Error: Unterminated string.\n")
            return

        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self, offset=0):
        if self.current + offset >= len(self.source):
            return "\0"
        return self.source[self.current + offset]

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type, literal=None):
        text = ""
        if token_type != TokenType.EOF:
            text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, 0))

    def is_at_end(self):
        return self.current >= len(self.source)
    
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

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
    tokens = []
    scanner = None
    if file_contents:
        scanner = Scanner(file_contents)
        tokens = scanner.scan_tokens()
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner

    for token in tokens:
        print(token)

    if scanner and scanner.had_error:
        return 65

if __name__ == "__main__":
    sys.exit(main())