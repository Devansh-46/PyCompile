class VM:
    def __init__(self):
        self.bytecode = []
        self.pc = 0
        self.stack = []
        self.variables = {}

    def compile_to_bytecode(self, ast):
        self.bytecode = self._compile_node(ast)
        return self.bytecode

    def _compile_node(self, node):
        if node.type == 'program':
            bytecode = []
            for child in node.children:
                bytecode.extend(self._compile_node(child))
            return bytecode
        elif node.type == 'assignment':
            bytecode = self._compile_node(node.children[0])
            bytecode.append(f'STORE {node.value}')
            return bytecode
        elif node.type == 'identifier':
            return [f'LOAD {node.value}']
        elif node.type == 'number':
            return [f'PUSH {node.value}']
        elif node.type == 'binary_expression':
            left_bytecode = self._compile_node(node.children[0])
            right_bytecode = self._compile_node(node.children[1])
            op_bytecode = [f'{node.value}']
            return left_bytecode + right_bytecode + op_bytecode
        elif node.type == 'if':
            condition_bytecode = self._compile_node(node.children[0])
            then_bytecode = self._compile_node(node.children[1])
            else_bytecode = self._compile_node(node.children[2]) if len(node.children) > 2 else []
            return condition_bytecode + [f'JMP_IF_FALSE {len(then_bytecode) + 1}'] + then_bytecode + [f'JMP {len(else_bytecode)}'] + else_bytecode
        elif node.type == 'while':
            condition_bytecode = self._compile_node(node.children[0])
            body_bytecode = self._compile_node(node.children[1])
            return condition_bytecode + [f'JMP_IF_FALSE {len(body_bytecode) + 1}'] + body_bytecode + ['JMP -' + str(len(condition_bytecode) + len(body_bytecode) + 1)]
        elif node.type == 'print':
            bytecode = self._compile_node(node.children[0])
            bytecode.append('PRINT')
            return bytecode
        elif node.type == 'function_def':
            func_bytecode = []
            for stmt in node.children[1].children:
                func_bytecode.extend(self._compile_node(stmt))
            return [f'FUNC {node.value}'] + func_bytecode + ['ENDFUNC']
        elif node.type == 'function_call':
            arg_bytecode = []
            for arg in node.children:
                arg_bytecode.extend(self._compile_node(arg))
            return arg_bytecode + [f'CALL {node.value}']
        elif node.type == 'expression_statement':
            return self._compile_node(node.children[0])
        else:
            raise ValueError(f"Unknown AST node type: {node.type}")

    def run(self, bytecode):
        self.bytecode = bytecode
        self.pc = 0
        while self.pc < len(self.bytecode):
            instruction = self.bytecode[self.pc].split()
            opcode = instruction[0]
            if opcode == 'PUSH':
                self.stack.append(int(instruction[1]))
            elif opcode == 'LOAD':
                self.stack.append(self.variables[instruction[1]])
            elif opcode == 'STORE':
                self.variables[instruction[1]] = self.stack.pop()
            elif opcode == 'ADD':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            elif opcode == 'SUB':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
            elif opcode == 'MUL':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
            elif opcode == 'DIV':
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a / b)
            elif opcode == 'PRINT':
                print(self.stack.pop())
            elif opcode == 'JMP_IF_FALSE':
                if not self.stack.pop():
                    self.pc += int(instruction[1])
            elif opcode == 'JMP':
                self.pc += int(instruction[1])
            self.pc += 1
        return self.variables
