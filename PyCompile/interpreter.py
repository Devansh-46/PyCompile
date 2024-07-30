class Interpreter:
    def __init__(self, instructions):
        self.instructions = instructions()
        self.stack = []
        self.memory = {}
        self.instruction_pointer = 0
        self.labels = self.find_labels()
        self.instruction_pointer = self.find_instruction_pointer()


    def find_labels(self):
        labels = {}
        for i, instruction in enumerate(self.instructions):
            if instruction.endswith(':'):
                labels[instruction[:-1]] = i
        return labels
    
    def find_instruction_pointer(self):
        for i, instruction in enumerate(self.instructions):
            if instruction.endswith(':'):
                continue
            else:
                return i
        

    def run(self):
        while self.instruction_pointer < len(self.instructions):
            instruction = self.instructions[self.instruction_pointer]
            self.execute(instruction)
            self.instruction_pointer += 1
        

    def execute(self, instruction):
        parts = instruction.strip().split()
        if not parts:
            return
        command = parts[0]

        if command == 'PUSH':
            self.stack.append(int(parts[1]))
        elif command == 'STORE':
            self.memory[parts[1]] = self.stack.pop()
        elif command == 'LOAD':
            self.stack.append(self.memory[parts[1]])
        elif command == 'CMP_GT':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(int(a > b))
        elif command == 'CMP_LT':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(int(a < b))
        elif command == 'JMP_IF_FALSE':
            if not self.stack.pop():
                self.instruction_pointer = self.labels[parts[1]] - 1
        elif command == 'JMP':
            self.instruction_pointer = self.labels[parts[1]] - 1
        elif command == 'PRINT':
            print(self.stack.pop())
        elif command == 'ADD':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a + b)
        elif command == 'HALT':
            exit(0)
        else:
            pass
    

# Example usage
# instructions = [
#     'PUSH 10',
#     'STORE x',
#     'LOAD x',
#     'PUSH 5',
#     'CMP_GT',
#     'JMP_IF_FALSE ELSE',
#     'LOAD x',
#     'PRINT',
#     'JMP ENDIF',
#     'ELSE:',
#     'PUSH 0',
#     'PRINT',
#     'ENDIF:',
#     'PUSH 1',
#     'STORE y',
#     'WHILE:',
#     'LOAD y',
#     'PUSH 10',
#     'CMP_LT',
#     'JMP_IF_FALSE ENDWHILE',
#     'LOAD y',
#     'PRINT',
#     'LOAD y',
#     'PUSH 1',
#     'ADD',
#     'STORE y',
#     'JMP WHILE',
#     'ENDWHILE:',
#     'HALT'
# ]

# interpreter = Interpreter(instructions)
# interpreter.run()
