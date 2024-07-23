from mytoken import Token


def tokenize(input):
    tokens = []
    i = 0
    while i < len(input):
        if input[i].isspace():
            i += 1
        elif input[i].isdigit():
            num = input[i]
            i += 1
            while i < len(input) and input[i].isdigit():
                num += input[i]
                i += 1
            tokens.append(Token('NUMBER', num))
        elif input[i].isalpha():
            id = input[i]
            i += 1
            while i < len(input) and (input[i].isalpha() or input[i].isdigit() or input[i] == '_'):
                id += input[i]
            if id in ('if', 'then', 'else', 'while', 'do', 'print', 'def'):
                tokens.append(Token(id.upper(), id))
            else:
                tokens.append(Token('IDENTIFIER', id))
        elif input[i] == '=':
            if i + 1 < len(input) and input[i + 1] == '=':
                tokens.append(Token('EQUALS', '=='))
                i += 2
            else:
                tokens.append(Token('ASSIGN', '='))
                i += 1
        elif input[i] == '+':
            tokens.append(Token('PLUS', '+'))
            i += 1
        elif input[i] == '-':
            tokens.append(Token('MINUS', '-'))
            i += 1
        elif input[i] == '*':
            tokens.append(Token('MUL', '*'))
            i += 1
        elif input[i] == '/':
            tokens.append(Token('DIV', '/'))
            i += 1
        elif input[i] == '(':
            tokens.append(Token('LPAREN', '('))
            i += 1
        elif input[i] == ')':
            tokens.append(Token('RPAREN', ')'))
            i += 1
        elif input[i] == '{':
            tokens.append(Token('LBRACE', '{'))
            i += 1
        elif input[i] == '}':
            tokens.append(Token('RBRACE', '}'))
            i += 1
        elif input[i] == ',':
            tokens.append(Token('COMMA', ','))
            i += 1
        elif input[i] == ';':
            tokens.append(Token('SEMICOLON', ';'))
            i += 1
        else:
            raise ValueError(f"Unknown character: {input[i]}")
    return tokens

