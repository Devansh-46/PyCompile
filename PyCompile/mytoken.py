# mytoken.py

class Token:
    def __init__(self, type, value, line=None, column=None):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}, {self.column})"

class TokenType:
    # Keywords
    DEF = 'DEF'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    RETURN = 'RETURN'
    # Operators
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    LT = 'LT'
    LE = 'LE'
    GT = 'GT'
    GE = 'GE'
    EQ = 'EQ'
    NE = 'NE'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    # Delimiters
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    COLON = 'COLON'
    COMMA = 'COMMA'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    END = 'END'
    # Others
    NUMBER = 'NUMBER'
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    EOF = 'EOF'
    # Assignment
    ASSIGN = 'ASSIGN'
    ADD_ASSIGN = 'ADD_ASSIGN'
    SUB_ASSIGN = 'SUB_ASSIGN'
    MUL_ASSIGN = 'MUL_ASSIGN'
    DIV_ASSIGN = 'DIV_ASSIGN'
    # Unary operators
    INCREMENT = 'INCREMENT'
    DECREMENT = 'DECREMENT'
    # Comparison operators
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    # Bitwise operators
    BITWISE_AND = 'BITWISE_AND'
    BITWISE_OR = 'BITWISE_OR'
    BITWISE_XOR = 'BITWISE_XOR'
    BITWISE_NOT = 'BITWISE_NOT'
    LEFT_SHIFT = 'LEFT_SHIFT'
    RIGHT_SHIFT = 'RIGHT_SHIFT'
    # Logical operators
    LOGICAL_AND = 'LOGICAL_AND'
    LOGICAL_OR = 'LOGICAL_OR'
    LOGICAL_NOT = 'LOGICAL_NOT'
    # Control flow
    BREAK = 'BREAK'
    CONTINUE = 'CONTINUE'
    # Data types
    INT = 'INT'
    FLOAT = 'FLOAT'
    CHAR = 'CHAR'
    BOOL = 'BOOL'
    VOID = 'VOID'
    # Comments
    COMMENT = 'COMMENT'
    # Error
    ERROR = 'ERROR'
    # Keywords
    keywords = {
        'def': DEF,
        'if': IF,
        'else': ELSE,
        'while': WHILE,
        'return': RETURN,
        'and': AND,
        'or': OR,
        'not': NOT,
        'break': BREAK,
        'continue': CONTINUE,
        'int': INT,
        'float': FLOAT,
        'char': CHAR,
        'bool': BOOL,
        'void': VOID,
    }
    # Operators
    operators = {
        '+': PLUS,
        '-': MINUS,
        '*': MUL,
        '/': DIV,
        '<': LT,
        '<=': LE,
        '>': GT,
        '>=': GE,
        '==': EQ,
        '!=': NE,
        '=': ASSIGN,
        '+=': ADD_ASSIGN,
        '-=': SUB_ASSIGN,
        '*=': MUL_ASSIGN,
        '/=': DIV_ASSIGN,
        '++': INCREMENT,
        '--': DECREMENT,
        '==': EQUAL,
        '!=': NOT_EQUAL,
        '&': BITWISE_AND,
        '|': BITWISE_OR,
        '^': BITWISE_XOR,
        '~': BITWISE_NOT,
        '<<': LEFT_SHIFT,
        '>>': RIGHT_SHIFT,
        '&&': LOGICAL_AND,
        '||': LOGICAL_OR,
        '!': LOGICAL_NOT,
    }
    # Delimiters
    delimiters = {
        '(': LPAREN,
        ')': RPAREN,
        ':': COLON,
        ',': COMMA,
        '{': LBRACE,
        '}': RBRACE,
        ';': END,
    }
    # Unary operators
    unary_operators = {
        '++': INCREMENT,
        '--': DECREMENT,
        '~': BITWISE_NOT,
        '!': LOGICAL_NOT,
    }
    # Comparison operators
    comparison_operators = {
        '==': EQUAL,
        '!=': NOT_EQUAL,
    }
    # Bitwise operators
    bitwise_operators = {
        '&': BITWISE_AND,
        '|': BITWISE_OR,
        '^': BITWISE_XOR,
        '~': BITWISE_NOT,
        '<<': LEFT_SHIFT,
        '>>': RIGHT_SHIFT,
    }
    # Logical operators
    logical_operators = {
        '&&': LOGICAL_AND,
        '||': LOGICAL_OR,
        '!': LOGICAL_NOT,
    }
    # Control flow
    control_flow = {
        'break': BREAK,
        'continue': CONTINUE,
    }
    # Data types
    data_types = {
        'int': INT,
        'float': FLOAT,
        'char': CHAR,
        'bool': BOOL,
        'void': VOID,
    }
    # Function calls
    function_calls = {
        'print': 'PRINT',
        }
    # Comments
    comments = {
        '//': COMMENT,
        '/*': COMMENT,
        '*/': COMMENT,
    }
    # Error
    errors = {
        'ERROR': ERROR,
    }
    # Combine all operators into one dictionary
    operators.update(unary_operators)
    operators.update(comparison_operators)
    operators.update(bitwise_operators)
    operators.update(logical_operators)
    operators.update(control_flow)
    operators.update(data_types)
    operators.update(function_calls)
    operators.update(comments)
    operators.update(errors)
    # All operators
    operators.update(delimiters)
    operators.update(keywords)
    # All tokens
    tokens = list(operators.values())
    # All operators
    operators = list(operators.keys())
