import ply.yacc as yacc
from lexer import Lexer
from node import Node

class IfElseNode(Node):
    def __init__(self, condition, then_body, else_body):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class Parser:
    tokens = Lexer.tokens

    precedence = (
        ('left', 'AND', 'OR'),
        ('left', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL', 'DIV'),
        ('right', 'UMINUS'),  # Unary minus operator
    )

    def __init__(self):
        self.lexer = Lexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self, debug=True, errorlog=yacc.NullLogger())

    def p_program(self, p):
        '''program : statement_list'''
        p[0] = ('program', p[1])

    def p_statement_list(self, p):
        '''statement_list : statement_list statement
                          | statement'''
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    def p_statement(self, p):
        '''statement : assignment_statement
                     | print_statement
                     | if_statement
                     | while_statement
                     | function_definition
                     | tuple_statement
                     | string_statement'''
        p[0] = p[1]

    def p_assignment_statement(self, p):
        '''assignment_statement : IDENTIFIER ASSIGN expression'''
        p[0] = ('assign', p[1], p[3])

    def p_print_statement(self, p):
        '''print_statement : PRINT LPAREN expression RPAREN'''
        p[0] = ('print', p[3])

    def p_tuple_statement(self, p):
        '''tuple_statement : LPAREN expression_list RPAREN'''
        p[0] = ('tuple', p[2])

    def p_string_statement(self, p):
        '''string_statement : STRING'''
        p[0] = ('string', p[1])

    def p_expression_list(self, p):
        '''expression_list : expression_list COMMA expression
                           | expression'''
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_if_statement(self, p):
        '''if_statement : IF expression COLON statement_list else_statement
                        | IF expression COLON statement_list'''
        if len(p) == 6:
            p[0] = ('if_else', p[2], p[4], p[5])
        else:
            p[0] = ('if', p[2], p[4])

    def p_else_statement(self, p):
        '''else_statement : ELSE COLON statement_list'''
        p[0] = ('else', p[3])

    def p_while_statement(self, p):
        '''while_statement : WHILE expression COLON statement_list'''
        p[0] = ('while', p[2], p[4])

    def p_function_definition(self, p):
        '''function_definition : DEF IDENTIFIER LPAREN RPAREN COLON statement_list'''
        p[0] = ('function', p[2], p[6])

    def p_expression(self, p):
        '''expression : term
                      | expression PLUS term
                      | expression MINUS term
                      | expression LT term
                      | expression LE term
                      | expression GT term
                      | expression GE term
                      | expression EQ term
                      | expression NE term'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[2], p[1], p[3])

    def p_term(self, p):
        '''term : factor
                | term MUL factor
                | term DIV factor'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[2], p[1], p[3])

    def p_factor(self, p):
        '''factor : NUMBER
                  | IDENTIFIER
                  | LPAREN expression RPAREN
                  | MINUS factor %prec UMINUS'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = ('uminus', p[2])

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}', line {p.lineno}, position {p.lexpos}")
        else:
            print("Syntax error at EOF")

    def parse(self, code):
        return self.parser.parse(code)

# def main():
#     parser = Parser()
#     input_code = '''
#     def my_function():
#         x = 10
#         if x > 5:
#             print(x)
#         else:
#             print(0)
#     '''
#     result = parser.parse(input_code)
#     print(result)

# if __name__ == '__main__':
#     main()
