import sys
import re
from enum import Enum

exit_code: int = 0

class TOKEN_TYPE(Enum):
    NONE = -2
    EOF = -1
    STRING = 0
    NUMBER = 1
    IDENTIFIER = 2
    LEFT_PAREN = 3
    RIGHT_PAREN = 4
    LEFT_BRACE = 5
    RIGHT_BRACE = 6
    COMMA = 7
    DOT = 8
    MINUS = 9
    PLUS = 10
    SEMICOLON = 11
    STAR = 12
    SLASH = 13
    EQUAL_EQUAL = 14
    EQUAL = 15
    BANG_EQUAL = 16
    BANG = 17
    LESS_EQUAL = 18
    LESS = 19
    GREATER_EQUAL = 20
    GREATER = 21
    AND = 22
    OR = 23
    IF = 24
    ELSE = 25
    FOR = 26
    WHILE = 27
    TRUE = 28
    FALSE = 29
    CLASS = 30
    SUPER = 31
    THIS = 32
    VAR = 33
    FUN = 34
    RETURN = 35
    PRINT = 36
    NIL = 37

    def __str__(self):
        return self.name

class Token:
    def __init__(self, type: TOKEN_TYPE, name: str, value):
        self.type = type
        self.name = name
        self.value = value

    def __str__(self):
        return f"{str(self.type)} {self.name} {self.value}"

    def __repr__(self):
        return str(self)

class Lexer:
    def __init__(self, program: str):
        self.program: str = program
        self.size: int = len(self.program)
        self.i: int = 0
        if self.size >= 1:
            self.c: str = self.program[self.i]
        self.line: int = 1

    def advance(self):
        self.i += 1
        if self.i < self.size:
            self.c = self.program[self.i]

    def advance_with(self, token: Token) -> Token:
        self.advance()
        return token

    def skip_whitespace(self):
        while self.i < self.size and self.c.isspace():
            if self.c in [" ", "\r", "\t"]:
                self.advance()
            elif self.c == "\n":
                self.advance()
                self.line += 1

    def peek(self) -> Token:
        i = self.i
        c = self.c
        self.advance()
        next: Token
        self.skip_whitespace()

        if self.i >= self.size:
            next = Token(TOKEN_TYPE.EOF, "", "null")
        elif self.c == "(":
            next = self.advance_with(Token(TOKEN_TYPE.LEFT_PAREN, "(", "null"))
        elif self.c == ")":
            next = self.advance_with(Token(TOKEN_TYPE.RIGHT_PAREN, ")", "null"))
        elif self.c == "{":
            next = self.advance_with(Token(TOKEN_TYPE.LEFT_BRACE, "{", "null"))
        elif self.c == "}":
            next = self.advance_with(Token(TOKEN_TYPE.RIGHT_BRACE, "}", "null"))
        elif self.c == ",":
            next = self.advance_with(Token(TOKEN_TYPE.COMMA, ",", "null"))
        elif self.c == ".":
            next = self.advance_with(Token(TOKEN_TYPE.DOT, ".", "null"))
        elif self.c == "-":
            next = self.advance_with(Token(TOKEN_TYPE.MINUS, "-", "null"))
        elif self.c == "+":
            next = self.advance_with(Token(TOKEN_TYPE.PLUS, "+", "null"))
        elif self.c == ";":
            next = self.advance_with(Token(TOKEN_TYPE.SEMICOLON, ";", "null"))
        elif self.c == "*":
            next = self.advance_with(Token(TOKEN_TYPE.STAR, "*", "null"))
        elif self.c == "/":
            if self.peek().type == TOKEN_TYPE.SLASH:
                while self.i < self.size and self.c != "\n":
                    self.advance()
                next = Token(TOKEN_TYPE.NONE, "", "")
            else:
                next = self.advance_with(Token(TOKEN_TYPE.SLASH, "/", "null"))
        elif self.c == "=":
            if self.peek().type == TOKEN_TYPE.EQUAL:
                self.advance()
                next = self.advance_with(Token(TOKEN_TYPE.EQUAL_EQUAL, "==", "null"))
            else:
                next = self.advance_with(Token(TOKEN_TYPE.EQUAL, "=", "null"))
        elif self.c == "!":
            if self.peek().type == TOKEN_TYPE.EQUAL:
                self.advance()
                next = self.advance_with(Token(TOKEN_TYPE.BANG_EQUAL, "!=", "null"))
            else:
                next = self.advance_with(Token(TOKEN_TYPE.BANG, "!", "null"))
        elif self.c == "<":
            if self.peek().type == TOKEN_TYPE.EQUAL:
                self.advance()
                next = self.advance_with(Token(TOKEN_TYPE.LESS_EQUAL, "<=", "null"))
            else:
                next = self.advance_with(Token(TOKEN_TYPE.LESS, "<", "null"))
        elif self.c == ">":
            if self.peek().type == TOKEN_TYPE.EQUAL:
                self.advance()
                next = self.advance_with(Token(TOKEN_TYPE.GREATER_EQUAL, ">=", "null"))
            else:
                next = self.advance_with(Token(TOKEN_TYPE.GREATER, ">", "null"))
        elif self.c == '"':
            next = self.next_string()
        elif self.c.isalpha() or self.c == "_":
            next = self.next_id()
        elif self.c.isdigit():
            next = self.next_number()
        else:
            next = self.advance_with(Token(TOKEN_TYPE.NONE, "", ""))
        
        self.i = i
        self.c = c
        return next

    def next_id(self) -> Token:
        identifier = ""
        while self.i < self.size and (self.c.isalnum() or self.c == "_"):
            identifier += self.c
            self.advance()
        
        return {
            "and": Token(TOKEN_TYPE.AND, identifier, "null"),
            "or": Token(TOKEN_TYPE.OR, identifier, "null"),
            "if": Token(TOKEN_TYPE.IF, identifier, "null"),
            "else": Token(TOKEN_TYPE.ELSE, identifier, "null"),
            "for": Token(TOKEN_TYPE.FOR, identifier, "null"),
            "while": Token(TOKEN_TYPE.WHILE, identifier, "null"),
            "true": Token(TOKEN_TYPE.TRUE, identifier, "null"),
            "false": Token(TOKEN_TYPE.FALSE, identifier, "null"),
            "class": Token(TOKEN_TYPE.CLASS, identifier, "null"),
            "super": Token(TOKEN_TYPE.SUPER, identifier, "null"),
            "this": Token(TOKEN_TYPE.THIS, identifier, "null"),
            "var": Token(TOKEN_TYPE.VAR, identifier, "null"),
            "fun": Token(TOKEN_TYPE.FUN, identifier, "null"),
            "return": Token(TOKEN_TYPE.RETURN, identifier, "null"),
            "print": Token(TOKEN_TYPE.PRINT, identifier, "null"),
            "nil": Token(TOKEN_TYPE.NIL, identifier, "null"),
        }.get(identifier, Token(TOKEN_TYPE.IDENTIFIER, identifier, "null"))

    def next_string(self) -> Token:
        global exit_code
        string_value = ""
        self.advance()
        while self.c != '"':
            string_value += self.c
            self.advance()
            if self.i >= self.size:
                print(f"[line {self.line}] Error: Unterminated string.", file=sys.stderr)
                exit_code = 65
                return self.advance_with(Token(TOKEN_TYPE.NONE, "", ""))
        return self.advance_with(Token(TOKEN_TYPE.STRING, f'"{string_value}"', string_value))

    def next_number(self) -> Token:
        dot = False
        number_string = ""
        while self.i < self.size:
            if self.c == ".":
                if dot:
                    break
                dot = True
            elif not self.c.isdigit():
                break
            number_string += self.c
            self.advance()
        
        value = float(number_string)
        return Token(TOKEN_TYPE.NUMBER, number_string, value)

    def next_token(self) -> Token:
        self.skip_whitespace()
        if self.i >= self.size:
            return Token(TOKEN_TYPE.EOF, "", "null")

        return self.peek()

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.current = 0

    def parse(self):
        return self.expression()

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()
        while self.match(TOKEN_TYPE.BANG_EQUAL, TOKEN_TYPE.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def match(self, *types) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def is_at_end(self) -> bool:
        return self.peek().type == TOKEN_TYPE.EOF

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def peek(self) -> Token:
        return self.tokens[self.current]

    def unary(self):
        if self.match(TOKEN_TYPE.MINUS, TOKEN_TYPE.BANG):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TOKEN_TYPE.NUMBER, TOKEN_TYPE.STRING, TOKEN_TYPE.FALSE, TOKEN_TYPE.TRUE, TOKEN_TYPE.NIL):
            return Literal(self.previous().value)
        elif self.match(TOKEN_TYPE.IDENTIFIER):
            return Variable(self.previous())
        elif self.match(TOKEN_TYPE.LEFT_PAREN):
            expr = self.expression()
            self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise Exception(message)

class ASTNode:
    pass

class Binary(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Unary(ASTNode):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

class Variable(ASTNode):
    def __init__(self, token):
        self.token = token

class Grouping(ASTNode):
    def __init__(self, expression):
        self.expression = expression

def main():
    with open(sys.argv[1]) as f:
        program = f.read()
        lex = Lexer(program)
        tokens = []
        while True:
            token = lex.next_token()
            if token.type == TOKEN_TYPE.EOF:
                break
            if token.type != TOKEN_TYPE.NONE:
                tokens.append(token)
                print(token)

    parser = Parser(tokens)
    try:
        expression = parser.parse()
        print("Parsed Expression:", expression)
    except Exception as e:
        print("Parsing Error:", e)

if __name__ == "__main__":
    main()