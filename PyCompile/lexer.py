# lexer.py

from mytoken import Token

class Lexer:
    def __init__(self, input_code):
        self.input_code = input_code
        self.tokens = []
        self.current_position = 0

    def tokenize(self):
        while self.current_position < len(self.input_code):
            current_char = self.input_code[self.current_position]

            if current_char.isspace():
                self.current_position += 1
            elif current_char.isdigit():
                self.tokens.append(self.tokenize_number())
            elif current_char.isalpha() or current_char == '_':
                self.tokens.append(self.tokenize_identifier())
            else:
                try:
                    self.tokens.append(self.tokenize_symbol())
                except RuntimeError as e:
                    raise LexerError(f"Unexpected character: {e}")

        self.tokens.append(Token('EOF', 'EOF'))
        return self.tokens

    def tokenize_number(self):
        start_position = self.current_position
        while self.current_position < len(self.input_code) and self.input_code[self.current_position].isdigit():
            self.current_position += 1
        return Token('NUMBER', self.input_code[start_position:self.current_position])

    def tokenize_identifier(self):
        start_position = self.current_position
        while self.current_position < len(self.input_code) and (self.input_code[self.current_position].isalnum() or self.input_code[self.current_position] == '_'):
            self.current_position += 1
        value = self.input_code[start_position:self.current_position]
        if value in ('if', 'else', 'while', 'print', 'def'):
            return Token(value.upper(), value)
        return Token('IDENTIFIER', value)

    def tokenize_symbol(self):
        current_char = self.input_code[self.current_position]
        self.current_position += 1
        if current_char == '=':
            if self.current_position < len(self.input_code) and self.input_code[self.current_position] == '=':
                self.current_position += 1
                return Token('EQ', '==')
            return Token('ASSIGN', '=')
        elif current_char == '+':
            return Token('PLUS', '+')
        elif current_char == '-':
            return Token('MINUS', '-')
        elif current_char == '*':
            return Token('MUL', '*')
        elif current_char == '/':
            return Token('DIV', '/')
        elif current_char == '(':
            return Token('LPAREN', '(')
        elif current_char == ')':
            return Token('RPAREN', ')')
        elif current_char == ':':
            return Token('COLON', ':')
        elif current_char == ',':
            return Token('COMMA', ',')
        elif current_char == '{':
            return Token('LBRACE', '{')
        elif current_char == '}':
            return Token('RBRACE', '}')
        elif current_char == '\n':
            return Token('END', 'END')
        else:
            raise RuntimeError(f"Unexpected character: {current_char} at position {self.current_position}")

class LexerError(Exception):
    def __init__(self, message, position=None):
        self.message = message
        self.position = position
        super().__init__(message)

    def __str__(self):
        if self.position is not None:
            return f"LexerError: {self.message} at position {self.position}"
        return f"LexerError: {self.message}"

    def __repr__(self):
        return self.__str__()

# if __name__ == "__main__":
#     input_code = """
#     x = 10
#     if x == 5:
#         print(x)
#     else:
#         print(0)
#     """
#     lexer = Lexer(input_code)
#     tokens = lexer.tokenize()
#     for token in tokens:
#         print(token)