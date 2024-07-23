from ir_generator import IRNode


class CodeGenerator:
    def __init__(self):
        self.instructions = []
        self.label_count = 0
        self.function_table = {}

    def generate(self, node):
        if node.type == 'PROGRAM':
            for child in node.children:
                self.generate(child)
        elif node.type == 'FUNCTION_DEF':
            self.function_table[node.value] = len(self.instructions)
            self.instructions.append(f'{node.value}:')
            for stmt in node.children[1].children:
                self.generate(stmt)
            self.instructions.append('RETURN')
        elif node.type == 'FUNCTION_CALL':
            for arg in node.children:
                self.generate(arg)
            self.instructions.append(f'CALL {node.value}')

    def generic_generate(self, ir_node):
        for child in ir_node.children:
            self.generate(child)

    def generate_PROGRAM(self, ir_node):
        self.generic_generate(ir_node)
        self.instructions.append('HALT')

    def generate_ASSIGN(self, ir_node):
        var_name = ir_node.value
        expr_node = ir_node.children[0]
        self.generate(expr_node)
        self.instructions.append(f'STORE {var_name}')

    def generate_ID(self, ir_node):
        var_name = ir_node.value
        self.instructions.append(f'LOAD {var_name}')

    def generate_NUMBER(self, ir_node):
        number = ir_node.value
        self.instructions.append(f'PUSH {number}')

    def generate_BIN_OP(self, ir_node):
        op = ir_node.value
        left_node = ir_node.children[0]
        right_node = ir_node.children[1]
        self.generate(left_node)
        self.generate(right_node)
        if op == '+':
            self.instructions.append('ADD')
        elif op == '-':
            self.instructions.append('SUB')
        elif op == '*':
            self.instructions.append('MUL')
        elif op == '/':
            self.instructions.append('DIV')

    def generate_CMP(self, ir_node):
        cmp = ir_node.value
        left_node = ir_node.children[0]
        right_node = ir_node.children[1]
        self.generate(left_node)
        self.generate(right_node)
        if cmp == '>':
            self.instructions.append('CMP_GT')
        elif cmp == '<':
            self.instructions.append('CMP_LT')
        elif cmp == '==':
            self.instructions.append('CMP_EQ')
        elif cmp == '!=':
            self.instructions.append('CMP_NE')

    def generate_IF(self, ir_node):
        condition_node = ir_node.children[0]
        if_body = ir_node.children[1]
        else_body = ir_node.children[2] if len(ir_node.children) > 2 else None

        self.generate(condition_node)
        self.instructions.append('JMP_IF_FALSE ELSE')

        self.generate(if_body)
        if else_body:
            self.instructions.append('JMP ENDIF')
            self.instructions.append('ELSE:')
            self.generate(else_body)

        self.instructions.append('ENDIF:')

    def generate_WHILE(self, ir_node):
        condition_node = ir_node.children[0]
        while_body = ir_node.children[1]

        self.instructions.append('WHILE:')
        self.generate(condition_node)
        self.instructions.append('JMP_IF_FALSE ENDWHILE')
        self.generate(while_body)
        self.instructions.append('JMP WHILE')
        self.instructions.append('ENDWHILE:')

    def generate_PRINT(self, ir_node):
        expr_node = ir_node.children[0]
        self.generate(expr_node)
        self.instructions.append('PRINT')

    def get_instructions(self):
        return self.instructions
    
    def new_label(self):
        label = f'LABEL{self.label_count}'
        self.label_count += 1
        return label

# Example usage
ir_tree = IRNode('PROGRAM', children=[
    IRNode('ASSIGN', value='x', children=[IRNode('NUMBER', value=10)]),
    IRNode('IF', children=[
        IRNode('CMP', value='>', children=[IRNode('ID', value='x'), IRNode('NUMBER', value=5)]),
        IRNode('BLOCK', children=[IRNode('PRINT', children=[IRNode('ID', value='x')])]),
        IRNode('BLOCK', children=[IRNode('PRINT', children=[IRNode('NUMBER', value=0)])])
    ]),
    IRNode('ASSIGN', value='y', children=[IRNode('NUMBER', value=1)]),
    IRNode('WHILE', children=[
        IRNode('CMP', value='<', children=[IRNode('ID', value='y'), IRNode('NUMBER', value=10)]),
        IRNode('BLOCK', children=[
            IRNode('PRINT', children=[IRNode('ID', value='y')]),
            IRNode('ASSIGN', value='y', children=[IRNode('BIN_OP', value='+', children=[IRNode('ID', value='y'), IRNode('NUMBER', value=1)])])
        ])
    ])
])

code_generator = CodeGenerator()
code_generator.generate(ir_tree)
instructions = code_generator.get_instructions()

print("Code Generation completed successfully.")
print("Generated Instructions:")
for instruction in instructions:
    print(instruction)
