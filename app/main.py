import sys

class Token:
    def __init__(self, type_, lexeme, literal, line):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.match("IF"):
            return self.if_statement()
        # Additional statement types can be added here
        raise Exception("Expected statement.")

    def if_statement(self):
        self.consume("LEFT_PAREN", "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume("RIGHT_PAREN", "Expect ')' after condition.")
        self.consume("LEFT_BRACE", "Expect '{' before statement.")
        
        then_branch = []
        while not self.check("RIGHT_BRACE") and not self.is_at_end():
            then_branch.append(self.statement())

        self.consume("RIGHT_BRACE", "Expect '}' after block.")
        
        else_branch = None
        if self.match("ELSE"):
            self.consume("LEFT_BRACE", "Expect '{' after 'else'.")
            else_branch = []
            while not self.check("RIGHT_BRACE") and not self.is_at_end():
                else_branch.append(self.statement())
            self.consume("RIGHT_BRACE", "Expect '}' after else block.")

        return {
            "type": "if",
            "condition": condition,
            "then": then_branch,
            "else": else_branch
        }

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.addition()
        while self.match("BANG_EQUAL", "EQUAL_EQUAL"):
            operator = self.previous()
            right = self.addition()
            expr = f"({operator.lexeme} {expr} {right})"
        return expr

    def addition(self):
        expr = self.multiplication()
        while self.match("PLUS", "MINUS"):
            operator = self.previous()
            right = self.multiplication()
            expr = f"({operator.lexeme} {expr} {right})"
        return expr

    def multiplication(self):
        expr = self.unary()
        while self.match("STAR", "SLASH"):
            operator = self.previous()
            right = self.unary()
            expr = f"({operator.lexeme} {expr} {right})"
        return expr

    def unary(self):
        if self.match("BANG", "MINUS"):
            operator = self.previous()
            right = self.unary()
            return f"({operator.lexeme} {right})"
        return self.primary()

    def primary(self):
        if self.match("NUMBER", "STRING"):
            return self.previous().literal
        if self.match("TRUE"):
            return "true"
        if self.match("FALSE"):
            return "false"
        if self.match("NIL"):
            return "nil"
        if self.match("IDENTIFIER"):
            return self.previous().lexeme
        raise Exception("Expected expression.")

    def match(self, *types):
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False

    def check(self, type_):
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == "EOF"

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

def tokenize(file_contents):
    line = 1
    tokens = []
    length = len(file_contents)
    i = 0
    while i < length:
        c = file_contents[i]
        if c == "\n":
            line += 1
        elif c in {" ", "\r", "\t"}:
            pass
        elif c == "(":
            tokens.append(Token("LEFT_PAREN", "(", "null", line))
        elif c == ")":
            tokens.append(Token("RIGHT_PAREN", ")", "null", line))
        elif c == "{":
            tokens.append(Token("LEFT_BRACE", "{", "null", line))
        elif c == "}":
            tokens.append(Token("RIGHT_BRACE", "}", "null", line))
        elif c == ",":
            tokens.append(Token("COMMA", ",", "null", line))
        elif c == ";":
            tokens.append(Token("SEMICOLON", ";", "null", line))
        elif c == ".":
            tokens.append(Token("DOT", ".", "null", line))
        elif c == "-":
            tokens.append(Token("MINUS", "-", "null", line))
        elif c == "+":
            tokens.append(Token("PLUS", "+", "null", line))
        elif c == "*":
            tokens.append(Token("STAR", "*", "null", line))
        elif c == "=":
            if i + 1 < length and file_contents[i + 1] == "=":
                i += 1
                tokens.append(Token("EQUAL_EQUAL", "==", "null", line))
            else:
                tokens.append(Token("EQUAL", "=", "null", line))
        elif c == "!":
            if i + 1 < length and file_contents[i + 1] == "=":
                i += 1
                tokens.append(Token("BANG_EQUAL", "!=", "null", line))
            else:
                tokens.append(Token("BANG", "!", "null", line))
        elif c == "<":
            if i + 1 < length and file_contents[i + 1] == "=":
                i += 1
                tokens.append(Token("LESS_EQUAL", "<=", "null", line))
            else:
                tokens.append(Token("LESS", "<", "null", line))
        elif c == ">":
            if i + 1 < length and file_contents[i + 1] == "=":
                i += 1
                tokens.append(Token("GREATER_EQUAL", ">=", "null", line))
            else:
                tokens.append(Token("GREATER", ">", "null", line))
        elif c == "/":
            if i + 1 < length and file_contents[i + 1] == "/":
                i += 1
                while i < length and file_contents[i] != "\n":
                    i += 1
            else:
                tokens.append(Token("SLASH", "/", "null", line))
        elif c == '"':
            word = ""
            i += 1
            while i < length and file_contents[i] != '"':
                if file_contents[i] == "\n":  # Handle new lines in strings
                    line += 1
                word += file_contents[i]
                i += 1
            
            if i == length:  # End of file reached without a closing quote
                print(f"[line {line}] Error: Unterminated string.", file=sys.stderr)
                tokens.append(Token("EOF", "", "null", line))
                sys.exit(65)
            
            i += 1  # Skip the closing quote
            tokens.append(Token("STRING", f'"{word}"', word, line))
        elif c.isdigit() or (c == '.' and (i + 1 < length and file_contents[i + 1].isdigit())):
            number = c
            if c == '.':
                while i + 1 < length and file_contents[i + 1].isdigit():
                    i += 1
                    number += file_contents[i]
            else:
                while i + 1 < length and file_contents[i + 1].isdigit():
                    i += 1
                    number += file_contents[i]
                if i + 1 < length and file_contents[i + 1] == '.':
                    i += 1
                    number += '.'
                    while i + 1 < length and file_contents[i + 1].isdigit():
                        i += 1
                        number += file_contents[i]
            tokens.append(Token("NUMBER", number, float(number), line))
        elif c.isalpha() or c == "_":
            word = c
            while i + 1 < length and (file_contents[i + 1].isalnum() or file_contents[i + 1] == "_"):
                i += 1
                word += file_contents[i]
            keywords = {
                "and": "AND",
                "class": "CLASS",
                "else": "ELSE",
                "false": "FALSE",
                "for": "FOR",
                "fun": "FUN",
                "if": "IF",
                "nil": "NIL",
                "or": "OR",
                "print": "PRINT",
                "return": "RETURN",
                "super": "SUPER",
                "this": "THIS",
                "true": "TRUE",
                "var": "VAR",
                "while": "WHILE",
            }
            if word in keywords:
                tokens.append(Token(keywords[word], word, "null", line))
            else:
                tokens.append(Token("IDENTIFIER", word, "null", line))
        else:
            print(f"[line {line}] Error: Unexpected character: '{c}'", file=sys.stderr)
            tokens.append(Token("EOF", "", "null", line))
            sys.exit(65)
        i += 1
    tokens.append(Token("EOF", "", "null", line))
    return tokens

def main():
    print(sys.argv)
    if len(sys.argv) < 2:
        print("Usage: lox.py <script>")
        sys.exit(64)

    with open(sys.argv[1], 'r') as file:
        file_contents = file.read()
    
    tokens = tokenize(file_contents)
    parser = Parser(tokens)
    statements = parser.parse()
    
    for stmt in statements:
        print(stmt)

if __name__ == "__main__":
    main()