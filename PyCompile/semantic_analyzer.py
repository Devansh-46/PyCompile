from node import Node

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        if node.type == 'program':
            for child in node.children:
                self.analyze(child)
        elif node.type == 'function_def':
            self.symbol_table[node.value] = node
        elif node.type == 'function_call':
            if node.value not in self.symbol_table:
                raise ValueError(f"Undefined function: {node.value}")

    def generic_analyze(self, node):
        for child in node.children:
            self.analyze(child)

    def analyze_PROGRAM(self, node):
        self.generic_analyze(node)

    def analyze_ASSIGN(self, node):
        var_name = node.children[0].value
        expr_node = node.children[1]
        self.analyze(expr_node)
        self.symbol_table[var_name] = expr_node.type

    def analyze_ID(self, node):
        var_name = node.value
        if var_name not in self.symbol_table:
            raise ValueError(f"Undeclared variable: {var_name}")

    def analyze_NUMBER(self, node):
        pass  # Numbers are always valid

    def analyze_BIN_OP(self, node):
        left_node = node.children[0]
        right_node = node.children[1]
        self.analyze(left_node)
        self.analyze(right_node)

    def analyze_CMP(self, node):
        left_node = node.children[0]
        right_node = node.children[1]
        self.analyze(left_node)
        self.analyze(right_node)

    def analyze_IF(self, node):
        condition_node = node.children[0]
        self.analyze(condition_node)
        self.generic_analyze(node.children[1])  # if body
        if len(node.children) > 2:
            self.generic_analyze(node.children[2])  # else body

    def analyze_WHILE(self, node):
        condition_node = node.children[0]
        self.analyze(condition_node)
        self.generic_analyze(node.children[1])  # while body

    def analyze_PRINT(self, node):
        expr_node = node.children[0]
        self.analyze(expr_node)


# Example usage
syntax_tree = Node('PROGRAM', [
    Node('ASSIGN', children=[Node('ID', 'x'), Node('NUMBER', 10)]),
    Node('IF', children=[
        Node('CMP', '>', children=[Node('ID', 'x'), Node('NUMBER', 5)]),
        Node('BLOCK', children=[Node('PRINT', children=[Node('ID', 'x')])]),
        Node('BLOCK', children=[Node('PRINT', children=[Node('NUMBER', 0)])])
    ]),
    Node('ASSIGN', children=[Node('ID', 'y'), Node('NUMBER', 1)]),
    Node('WHILE', children=[
        Node('CMP', '<', children=[Node('ID', 'y'), Node('NUMBER', 10)]),
        Node('BLOCK', children=[
            Node('PRINT', children=[Node('ID', 'y')]),
            Node('ASSIGN', children=[Node('ID', 'y'), Node('BIN_OP', '+', children=[Node('ID', 'y'), Node('NUMBER', 1)])])
        ])
    ])
])

analyzer = SemanticAnalyzer()
analyzer.analyze(syntax_tree)
print("Semantic analysis completed successfully.")
print("Symbol Table:", analyzer.symbol_table)
