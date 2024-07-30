class NodeWrapper:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f'NodeWrapper(type={self.type}, value={self.value}, children={self.children})'

def wrap_node(node):
    if isinstance(node, tuple):
        return NodeWrapper('tuple', None, [wrap_node(child) for child in node])
    elif isinstance(node, NodeWrapper):
        return node
    elif isinstance(node, str):
        return NodeWrapper('string', node)
    elif isinstance(node, (int, float)):
        return NodeWrapper('number', node)
    else:
        return NodeWrapper(type=type(node).__name__, value=node)

class IRNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f'IRNode(type={self.type}, value={self.value}, children={self.children})'

class IRGenerator:
    def generate(self, ast):
        wrapped_ast = wrap_node(ast)
        return self.visit(wrapped_ast)

    def visit(self, node):
        # Handle specific node types
        if node.type == 'tuple':
            return self.visit_tuple(node)
        elif node.type == 'string':
            return self.visit_string(node)
        elif node.type == 'number':
            return self.visit_number(node)
        
        # Handle other node types dynamically
        method_name = f'visit_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{node.type} method')

    def visit_tuple(self, node):
        return IRNode('tuple', None, [self.visit(child) for child in node.children])

    def visit_string(self, node):
        return IRNode('string', node.value)

    def visit_number(self, node):
        return IRNode('number', node.value)

    def visit_program(self, node):
        ir_nodes = [self.visit(child) for child in node.children]
        return IRNode('program', None, ir_nodes)

    def visit_block(self, node):
        ir_nodes = [self.visit(child) for child in node.children]
        return IRNode('block', None, ir_nodes)

    def visit_assignment(self, node):
        if len(node.children) < 1:
            raise ValueError("Assignment node is missing expression.")
        identifier = node.value
        expression_ir = self.visit(node.children[0])
        return IRNode('assignment', identifier, [expression_ir])

    def visit_if(self, node):
        if len(node.children) < 2:
            raise ValueError("If node is missing condition or then body.")
        condition_ir = self.visit(node.children[0])
        then_ir = self.visit(node.children[1])
        else_ir = self.visit(node.children[2]) if len(node.children) > 2 else None
        return IRNode('if', None, [condition_ir, then_ir, else_ir])

    def visit_while(self, node):
        if len(node.children) < 2:
            raise ValueError("While node is missing condition or body.")
        condition_ir = self.visit(node.children[0])
        body_ir = self.visit(node.children[1])
        return IRNode('while', None, [condition_ir, body_ir])

    def visit_print(self, node):
        if len(node.children) < 1:
            raise ValueError("Print node is missing expression.")
        expression_ir = self.visit(node.children[0])
        return IRNode('print', None, [expression_ir])

    def visit_function_def(self, node):
        if len(node.children) < 2:
            raise ValueError("Function definition node is missing parameters or body.")
        func_name = node.value
        parameters_ir = self.visit(node.children[0])
        body_ir = self.visit(node.children[1])
        return IRNode('function_def', func_name, [parameters_ir, body_ir])

    def visit_function_call(self, node):
        if len(node.children) < 1:
            raise ValueError("Function call node is missing arguments.")
        func_name = node.value
        arguments_ir = [self.visit(arg) for arg in node.children]
        return IRNode('function_call', func_name, arguments_ir)

    def visit_binary_expression(self, node):
        if len(node.children) < 2:
            raise ValueError("Binary expression node is missing operands.")
        left_ir = self.visit(node.children[0])
        right_ir = self.visit(node.children[1])
        return IRNode('binary_expression', node.value, [left_ir, right_ir])

    def visit_identifier(self, node):
        return IRNode('identifier', node.value)

    def visit_boolean(self, node):
        return IRNode('boolean', node.value)

    def visit_unary_expression(self, node):
        if len(node.children) < 1:
            raise ValueError("Unary expression node is missing operand.")
        operand_ir = self.visit(node.children[0])
        return IRNode('unary_expression', node.value, [operand_ir])

    def visit_comparison(self, node):
        if len(node.children) < 2:
            raise ValueError("Comparison node is missing operands.")
        left_ir = self.visit(node.children[0])
        right_ir = self.visit(node.children[1])
        return IRNode('comparison', node.value, [left_ir, right_ir])

    def visit_logical_expression(self, node):
        if len(node.children) < 2:
            raise ValueError("Logical expression node is missing operands.")
        left_ir = self.visit(node.children[0])
        right_ir = self.visit(node.children[1])
        return IRNode('logical_expression', node.value, [left_ir, right_ir])

    def visit_return(self, node):
        if len(node.children) < 1:
            raise ValueError("Return node is missing return value.")
        return_value_ir = self.visit(node.children[0])
        return IRNode('return', None, [return_value_ir])

    def visit_parameter_list(self, node):
        return [self.visit(child) for child in node.children]

    def visit_parameter(self, node):
        return IRNode('parameter', node.value)

    def visit_else(self, node):
        return self.visit(node.children[0])

    def visit_elif(self, node):
        return self.visit(node.children[0])

    def visit_elif_list(self, node):
        return [self.visit(child) for child in node.children]

    def visit_else_if(self, node):
        if len(node.children) < 2:
            raise ValueError("Else if node is missing condition or body.")
        condition_ir = self.visit(node.children[0])
        body_ir = self.visit(node.children[1])
        return IRNode('else_if', None, [condition_ir, body_ir])

    def visit_else_if_list(self, node):
        return [self.visit(child) for child in node.children]

    def visit_list(self, node):
        return [self.visit(child) for child in node.children]

    def visit_index(self, node):
        if len(node.children) < 1:
            raise ValueError("Index node is missing index.")
        index_ir = self.visit(node.children[0])
        return IRNode('index', None, [index_ir])
    
    def visit_index_assignment(self, node):
        if len(node.children) < 2:
            raise ValueError("Index assignment node is missing index or expression.")
        index_ir = self.visit(node.children[0])
        expression_ir = self.visit(node.children[1])
        return IRNode('index_assignment', None, [index_ir, expression_ir])
    
    def visit_list_assignment(self, node):
        if len(node.children) < 2:
            raise ValueError("List assignment node is missing index or expression.")
        index_ir = self.visit(node.children[0])
        expression_ir = self.visit(node.children[1])
        return IRNode('list_assignment', None, [index_ir, expression_ir])
    
    def visit_list_access(self, node):
        if len(node.children) < 1:
            raise ValueError("List access node is missing index.")
        index_ir = self.visit(node.children[0])
        return IRNode('list_access', None, [index_ir])
    
    def visit_list_slice(self, node):
        if len(node.children) < 2:
            raise ValueError("List slice node is missing start or end.")
        start_ir = self.visit(node.children[0])
        end_ir = self.visit(node.children[1])
        return IRNode('list_slice', None, [start_ir, end_ir])
    
    def visit_list_slice_full(self, node):
        if len(node.children) < 1:
            raise ValueError("List slice full node is missing step.")
        step_ir = self.visit(node.children[0])
        return IRNode('list_slice_full', None, [step_ir])
    
    def visit_list_slice_step(self, node):
        if len(node.children) < 1:
            raise ValueError("List slice step node is missing step.")
        step_ir = self.visit(node.children[0])
        return IRNode('list_slice_step', None, [step_ir])
