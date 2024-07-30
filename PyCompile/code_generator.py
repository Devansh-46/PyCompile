from ir_generator import IRNode
class CodeGenerator:
    def __init__(self):
        self.instructions = []
        self.label_count = 0
        self.function_table = {}

    def generate(self, node):
        if node.type == 'PROGRAM':
            self.generate_PROGRAM(node)
        elif node.type == 'ASSIGN':
            self.generate_ASSIGN(node)
        elif node.type == 'ID':
            self.generate_ID(node)
        elif node.type == 'NUMBER':
            self.generate_NUMBER(node)
        elif node.type == 'BIN_OP':
            self.generate_BIN_OP(node)
        elif node.type == 'CMP':
            self.generate_CMP(node)
        elif node.type == 'IF':
            self.generate_IF(node)
        elif node.type == 'WHILE':
            self.generate_WHILE(node)
        elif node.type == 'PRINT':
            self.generate_PRINT(node)
        elif node.type == 'RETURN':
            self.generate_RETURN(node)
        elif node.type == 'FUNCTION_DEF':
            self.generate_FUNCTION_DEF(node)
        elif node.type == 'FUNCTION_CALL':
            self.generate_FUNCTION_CALL(node)
        elif node.type == 'BLOCK':
            self.generate_BLOCK(node)
        elif node.type == 'TUPLE':
            self.generate_TUPLE(node)
        elif node.type == 'GET_TUPLE':
            self.generate_GET_TUPLE(node)
        elif node.type == 'STRING':
            self.generate_STRING(node)
            
        # elif IRNode.type == 'TUPLE':
        #     self.generate_TUPLE(node)
        # elif IRNode.type == 'GET_TUPLE':
        #     self.generate_GET_TUPLE(node)
        # elif IRNode.type == 'STRING':
        #     self.generate_STRING(node)
        else:
            raise ValueError(f'Unknown node type: {node.type}')


    def generate_PROGRAM(self, node):
        for child in node.children:
            self.generate(child)
        self.instructions.append('HALT')

    def generate_ASSIGN(self, node):
        var_name = node.value
        expr_node = node.children[0]
        self.generate(expr_node)
        self.instructions.append(f'STORE {var_name}')

    def generate_ID(self, node):
        var_name = node.value
        self.instructions.append(f'LOAD {var_name}')

    def generate_NUMBER(self, node):
        number = node.value
        self.instructions.append(f'PUSH {number}')

    def generate_BIN_OP(self, node):
        op = node.value
        left_node = node.children[0]
        right_node = node.children[1]
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

    def generate_CMP(self, node):
        cmp = node.value
        left_node = node.children[0]
        right_node = node.children[1]
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

    def generate_IF(self, node):
        condition_node = node.children[0]
        if_body = node.children[1]
        else_body = node.children[2] if len(node.children) > 2 else None

        false_label = self.new_label()
        end_label = self.new_label()

        self.generate(condition_node)
        self.instructions.append(f'JMP_IF_FALSE {false_label}')

        self.generate(if_body)
        if else_body:
            self.instructions.append(f'JMP {end_label}')
            self.instructions.append(f'{false_label}:')
            self.generate(else_body)
        else:
            self.instructions.append(f'{false_label}:')

        self.instructions.append(f'{end_label}:')

    def generate_WHILE(self, node):
        condition_node = node.children[0]
        while_body = node.children[1]

        start_label = self.new_label()
        end_label = self.new_label()

        self.instructions.append(f'{start_label}:')
        self.generate(condition_node)
        self.instructions.append(f'JMP_IF_FALSE {end_label}')

        self.generate(while_body)
        self.instructions.append(f'JMP {start_label}')
        self.instructions.append(f'{end_label}:')

    def generate_PRINT(self, node):
        expr_node = node.children[0]
        self.generate(expr_node)
        self.instructions.append('PRINT')

    def generate_RETURN(self, node):
        expr_node = node.children[0]
        self.generate(expr_node)
        self.instructions.append('RETURN')

    def generate_FUNCTION_DEF(self, node):
        function_name = node.value
        self.function_table[function_name] = len(self.instructions)
        self.instructions.append(f'{function_name}:')
        for stmt in node.children[1].children:
            self.generate(stmt)
        self.instructions.append('RETURN')

    def generate_FUNCTION_CALL(self, node):
        function_name = node.value
        for arg in node.children:
            self.generate(arg)
        self.instructions.append(f'CALL {function_name}')

    def generate_BLOCK(self, node):
        for stmt in node.children:
            self.generate(stmt)

    def generate_TUPLE(self, node):
        # Generate code for tuple creation
        for child in node.children:
            self.generate(child)
        self.instructions.append('CREATE_TUPLE')

    def generate_GET_TUPLE(self, node):
        # Generate code to get an element from a tuple
        tuple_node = node.children[0]
        index_node = node.children[1]
        self.generate(tuple_node)
        self.generate(index_node)
        self.instructions.append('GET_TUPLE')

    def generate_STRING(self, node):
        # Generate code for string literals
        string_value = node.value
        self.instructions.append(f'PUSH_STRING "{string_value}"')

    def get_instructions(self):
        return self.instructions

    def new_label(self):
        label = f'LABEL{self.label_count}'
        self.label_count += 1
        return label
