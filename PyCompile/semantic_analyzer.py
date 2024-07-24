from node import Node

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, ast):
        self.visit(ast)
        return ast

    def visit(self, node):
        method_name = f'visit_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_program(self, node):
        self.generic_visit(node)

    def visit_function_def(self, node):
        func_name = node.value
        if func_name in self.symbol_table:
            raise ValueError(f"Function '{func_name}' already defined")
        self.symbol_table[func_name] = node
        self.generic_visit(node)

    def visit_assignment(self, node):
        identifier = node.value
        self.symbol_table[identifier] = node
        self.generic_visit(node)

    def visit_identifier(self, node):
        if node.value not in self.symbol_table:
            raise ValueError(f"Undefined identifier '{node.value}'")


# Example usage
# syntax_tree = Node('PROGRAM', [
#     Node('ASSIGN', children=[Node('ID', 'x'), Node('NUMBER', 10)]),
#     Node('IF', children=[
#         Node('CMP', '>', children=[Node('ID', 'x'), Node('NUMBER', 5)]),
#         Node('BLOCK', children=[Node('PRINT', children=[Node('ID', 'x')])]),
#         Node('BLOCK', children=[Node('PRINT', children=[Node('NUMBER', 0)])])
#     ]),
#     Node('ASSIGN', children=[Node('ID', 'y'), Node('NUMBER', 1)]),
#     Node('WHILE', children=[
#         Node('CMP', '<', children=[Node('ID', 'y'), Node('NUMBER', 10)]),
#         Node('BLOCK', children=[
#             Node('PRINT', children=[Node('ID', 'y')]),
#             Node('ASSIGN', children=[Node('ID', 'y'), Node('BIN_OP', '+', children=[Node('ID', 'y'), Node('NUMBER', 1)])])
#         ])
#     ])
# ])

# analyzer = SemanticAnalyzer()
# analyzer.analyze(syntax_tree)
# print("Semantic analysis completed successfully.")
# print("Symbol Table:", analyzer.symbol_table)
