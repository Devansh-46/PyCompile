from node import Node
from mytoken import Token


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_position = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.parse_statement())
        return Node('program', None, statements)

    def is_at_end(self):
        return self.current_position >= len(self.tokens) or self.tokens[self.current_position].type == 'EOF'

    def consume(self, expected_type=None):
        if self.is_at_end():
            raise ValueError(f"Unexpected end of input, expected {expected_type}")
        token = self.tokens[self.current_position]
        if expected_type and token.type != expected_type:
            raise ValueError(f"Expected token type {expected_type}, but got {token.type}")
        self.current_position += 1
        return token

    def current_token(self):
        if self.is_at_end():
            return Token('EOF', 'EOF')
        return self.tokens[self.current_position]

    def peek_token(self):
        if self.current_position + 1 >= len(self.tokens):
            return Token('EOF', 'EOF')
        return self.tokens[self.current_position + 1]

    def parse_statement(self):
        token = self.current_token()
        if token.type == 'IDENTIFIER' and self.peek_token().type == 'ASSIGN':
            return self.parse_assignment()
        elif token.type == 'IF':
            return self.parse_if()
        elif token.type == 'WHILE':
            return self.parse_while()
        elif token.type == 'PRINT':
            return self.parse_print()
        elif token.type == 'DEF':
            return self.parse_function_def()
        elif token.type == 'IDENTIFIER' and self.peek_token().type == 'LPAREN':
            return self.parse_function_call()
        else:
            return self.parse_expression_as_statement()

    def parse_expression_as_statement(self):
        expr = self.parse_expression()
        if self.current_token().type != 'END':
            self.tokens.insert(self.current_position, Token('END', 'END'))
        self.consume('END')
        return Node('expression_statement', None, [expr])

    def parse_assignment(self):
        identifier = self.consume('IDENTIFIER').value
        self.consume('ASSIGN')
        expr = self.parse_expression()
        if self.current_token().type != 'END':
            self.tokens.insert(self.current_position, Token('END', 'END'))
        self.consume('END')
        return Node('assignment', identifier, [expr])

    def parse_if(self):
        self.consume('IF')
        condition = self.parse_expression()
        self.consume('COLON')
        then_branch = self.parse_statement()
        if self.current_token().type == 'ELSE':
            self.consume('ELSE')
            else_branch = self.parse_statement()
            return Node('if', None, [condition, then_branch, else_branch])
        else:
            return Node('if', None, [condition, then_branch])

    def parse_while(self):
        self.consume('WHILE')
        condition = self.parse_expression()
        self.consume('COLON')
        body = self.parse_statement()
        return Node('while', None, [condition, body])

    def parse_print(self):
        self.consume('PRINT')
        expr = self.parse_expression()
        if self.current_token().type != 'END':
            self.tokens.insert(self.current_position, Token('END', 'END'))
        self.consume('END')
        return Node('print', None, [expr])

    def parse_function_def(self):
        self.consume('DEF')
        func_name = self.consume('IDENTIFIER').value
        self.consume('LPAREN')
        params = []
        if self.current_token().type != 'RPAREN':
            params.append(self.consume('IDENTIFIER').value)
            while self.current_token().type == 'COMMA':
                self.consume('COMMA')
                params.append(self.consume('IDENTIFIER').value)
        self.consume('RPAREN')
        self.consume('COLON')
        body = []
        while self.current_token().type != 'END':
            body.append(self.parse_statement())
        self.consume('END')
        return Node('function_def', func_name, [Node('parameters', value=params), Node('body', children=body)])

    def parse_function_call(self):
        func_name = self.consume('IDENTIFIER').value
        self.consume('LPAREN')
        args = []
        if self.current_token().type != 'RPAREN':
            args.append(self.parse_expression())
            while self.current_token().type == 'COMMA':
                self.consume('COMMA')
                args.append(self.parse_expression())
        self.consume('RPAREN')
        return Node('function_call', func_name, args)

    def parse_expression(self):
        return self.parse_binary_expression()

    def parse_binary_expression(self):
        left = self.parse_term()
        while self.current_token().type in ('PLUS', 'MINUS'):
            op = self.consume().type
            right = self.parse_term()
            left = Node('binary_expression', op, [left, right])
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token().type in ('MUL', 'DIV'):
            op = self.consume().type
            right = self.parse_factor()
            left = Node('binary_expression', op, [left, right])
        return left

    def parse_factor(self):
        token = self.current_token()
        if token.type == 'NUMBER':
            self.consume('NUMBER')
            return Node('number', token.value)
        elif token.type == 'IDENTIFIER':
            if self.peek_token().type == 'LPAREN':
                return self.parse_function_call()
            else:
                self.consume('IDENTIFIER')
                return Node('identifier', token.value)
        elif token.type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        else:
            raise ValueError(f"Unexpected token: {token}")
