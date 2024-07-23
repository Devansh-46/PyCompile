from node import Node
class IRNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        return f"IRNode(type={self.type}, value={self.value}, children={self.children})"

class IRGenerator:
    def generate(self, node):
        method_name = 'generate_' + node.type
        method = getattr(self, method_name, self.generic_generate)
        return method(node)

    def generic_generate(self, node):
        ir_node = IRNode(node.type)
        for child in node.children:
            ir_child = self.generate(child)
            ir_node.children.append(ir_child)
        return ir_node

    def generate_PROGRAM(self, node):
        return self.generic_generate(node)

    def generate_ASSIGN(self, node):
        var_name = node.children[0].value
        expr_node = self.generate(node.children[1])
        return IRNode('ASSIGN', value=var_name, children=[expr_node])

    def generate_ID(self, node):
        return IRNode('ID', value=node.value)

    def generate_NUMBER(self, node):
        return IRNode('NUMBER', value=node.value)

    def generate_BIN_OP(self, node):
        left_node = self.generate(node.children[0])
        right_node = self.generate(node.children[1])
        return IRNode('BIN_OP', value=node.value, children=[left_node, right_node])

    def generate_CMP(self, node):
        left_node = self.generate(node.children[0])
        right_node = self.generate(node.children[1])
        return IRNode('CMP', value=node.value, children=[left_node, right_node])

    def generate_IF(self, node):
        condition_node = self.generate(node.children[0])
        if_body = self.generate(node.children[1])
        if len(node.children) > 2:
            else_body = self.generate(node.children[2])
            return IRNode('IF', children=[condition_node, if_body, else_body])
        return IRNode('IF', children=[condition_node, if_body])

    def generate_WHILE(self, node):
        condition_node = self.generate(node.children[0])
        while_body = self.generate(node.children[1])
        return IRNode('WHILE', children=[condition_node, while_body])

    def generate_PRINT(self, node):
        expr_node = self.generate(node.children[0])
        return IRNode('PRINT', children=[expr_node])

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

ir_generator = IRGenerator()
ir_tree = ir_generator.generate(syntax_tree)
print("IR Generation completed successfully.")
print("IR Tree:", ir_tree)
