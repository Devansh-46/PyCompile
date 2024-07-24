from node import Node

class IRGenerator:
    def generate(self, ast):
        return self.visit(ast)

    def visit(self, node):
        method_name = f'visit_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{node.type} method')

    def visit_program(self, node):
        ir_nodes = []
        for child in node.children:
            ir_nodes.append(self.visit(child))
        return ir_nodes

    def visit_block(self, node):
        ir_nodes = []
        for child in node.children:
            ir_nodes.append(self.visit(child))
        return IRNode('block', None, ir_nodes)

    def visit_assignment(self, node):
        identifier = node.value
        expression_ir = self.visit(node.children[0])
        return IRNode('assignment', identifier, [expression_ir])

    def visit_if(self, node):
        condition_ir = self.visit(node.children[0])
        then_ir = self.visit(node.children[1])
        else_ir = self.visit(node.children[2]) if len(node.children) > 2 else None
        return IRNode('if', None, [condition_ir, then_ir, else_ir])

    def visit_while(self, node):
        condition_ir = self.visit(node.children[0])
        body_ir = self.visit(node.children[1])
        return IRNode('while', None, [condition_ir, body_ir])

    def visit_print(self, node):
        expression_ir = self.visit(node.children[0])
        return IRNode('print', None, [expression_ir])

    def visit_function_def(self, node):
        func_name = node.value
        parameters_ir = self.visit(node.children[0])
        body_ir = self.visit(node.children[1])
        return IRNode('function_def', func_name, [parameters_ir, body_ir])

    def visit_function_call(self, node):
        func_name = node.value
        arguments_ir = [self.visit(arg) for arg in node.children]
        return IRNode('function_call', func_name, arguments_ir)

    def visit_binary_expression(self, node):
        left_ir = self.visit(node.children[0])
        right_ir = self.visit(node.children[1])
        return IRNode('binary_expression', node.value, [left_ir, right_ir])

    def visit_number(self, node):
        return IRNode('number', node.value)

    def visit_identifier(self, node):
        return IRNode('identifier', node.value)

# IRNode class
class IRNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f'IRNode(type={self.type}, value={self.value}, children={self.children})'
