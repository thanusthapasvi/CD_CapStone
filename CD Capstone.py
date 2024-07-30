class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_char = ''
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.source_code):
            self.current_char = self.source_code[self.pos]
        else:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isdigit():
                self.tokens.append(self.make_number())
            elif self.current_char in '+-*/();':
                self.tokens.append(Token(self.current_char))
                self.advance()
            else:
                self.error(f"Illegal character '{self.current_char}'")
                self.advance()
        return self.tokens

    def make_number(self):
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return Token('NUMBER', int(num_str))

    def error(self, message):
        print(f"Lexer error: {message}")

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'{self.type}:{self.value}' if self.value is not None else self.type

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()
        self.synchronizing_tokens = {';', ')', '}'}

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self):
        try:
            result = self.expr()
            if self.current_token is not None:
                self.error(f"Unexpected token '{self.current_token}'")
            return result
        except Exception as e:
            print(f"Parsing failed: {e}")

    def expr(self):
        result = self.term()
        while self.current_token is not None and self.current_token.type in ('+', '-'):
            token = self.current_token
            self.advance()
            if token.type == '+':
                result += self.term()
            elif token.type == '-':
                result -= self.term()
        return result

    def term(self):
        result = self.factor()
        while self.current_token is not None and self.current_token.type in ('*', '/'):
            token = self.current_token
            self.advance()
            if token.type == '*':
                result *= self.factor()
            elif token.type == '/':
                result /= self.factor()
        return result

    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.advance()
            return token.value
        elif token.type == '(':
            self.advance()
            result = self.expr()
            if self.current_token is None or self.current_token.type != ')':
                self.error("Expected ')'")
                self.recover()
            else:
                self.advance()
            return result
        else:
            self.error(f"Unexpected token '{token}'")
            self.recover()

    def error(self, message):
        print(f"Parser error: {message}")

    def recover(self):
        while self.current_token is not None and self.current_token.type not in self.synchronizing_tokens:
            self.advance()
        if self.current_token is not None:
            self.advance()

class Compiler:
    def __init__(self, source_code):
        self.source_code = source_code

    def compile(self):
        try:
            lexer = Lexer(self.source_code)
            tokens = lexer.generate_tokens()
            print(f"Tokens: {tokens}")
            parser = Parser(tokens)
            result = parser.parse()
            print(f"Compilation successful: {result}")
        except Exception as e:
            print(f"Compilation failed: {e}")

source_code = "3 + 5 * (10 - 4)"
compiler = Compiler(source_code)
compiler.compile()

source_code_with_error = "3 + 5 * (10 - 4;"
compiler = Compiler(source_code_with_error)
compiler.compile()
