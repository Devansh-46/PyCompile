import ply.lex as lex

class Lexer:
    tokens = (
        'NUMBER', 'IDENTIFIER', 'ASSIGN', 'PLUS', 'MINUS', 'MUL', 'DIV',
        'LPAREN', 'RPAREN', 'COLON', 'COMMA', 'LBRACE', 'RBRACE', 'END',
        'EQ', 'LT', 'GT', 'LE', 'GE', 'NE', 'AND', 'OR', 'NOT', 'STRING', 'DEF', 
        'IF', 'PRINT', 'ELSE', 'WHILE'
    )
    # Reserved words
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'print': 'PRINT',
        'def': 'DEF',
    }
    # Regular expression rules for simple tokens
    t_ASSIGN = r'='
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_COLON = r':'
    t_COMMA = r','
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_EQ = r'=='
    t_LT = r'<'
    t_GT = r'>'
    t_LE = r'<='
    t_GE = r'>='
    t_NE = r'!='
    t_AND = r'and'
    t_OR = r'or'
    t_NOT = r'not'
    t_STRING = r'\"(?:[^\"\\]|\\.)*\"'

    # Ignored characters (spaces and tabs)
    t_ignore = ' \t'





    # Define a rule to handle identifiers and reserved words
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
        return t

    # Define a rule to handle numbers
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Define a rule to handle newlines
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Tokenize the input code
    def tokenize(self, code):
        self.lexer.input(code)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens
    

# if __name__ == "__main__":
#     Test the lexer
#     lexer = Lexer()
#     lexer.build()
#     input_code = '''
#     def my_function():
#         x = 10
#         if x > 5:
#             print(x)
#         else:
#             print(0)
#     '''
#     tokens = lexer.tokenize(input_code)
#     for token in tokens:
#         print(token)
