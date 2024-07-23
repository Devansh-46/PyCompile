class AssemblyGenerator:
    def __init__(self):
        self.assembly_code = []
        self.label_counter = 0

    def generate(self, instructions):
        for instruction in instructions:
            method_name = 'generate_' + instruction.split()[0]
            method = getattr(self, method_name, self.generic_generate)
            method(instruction)

    def generic_generate(self, instruction):
        self.assembly_code.append(f'// {instruction}')

    def generate_PUSH(self, instruction):
        _, value = instruction.split()
        self.assembly_code.append(f'    PUSH {value}')

    def generate_STORE(self, instruction):
        _, var_name = instruction.split()
        self.assembly_code.append(f'    STORE {var_name}')

    def generate_LOAD(self, instruction):
        _, var_name = instruction.split()
        self.assembly_code.append(f'    LOAD {var_name}')

    def generate_CMP_GT(self, instruction):
        self.assembly_code.append('    CMP_GT')

    def generate_JMP_IF_FALSE(self, instruction):
        _, label = instruction.split()
        self.assembly_code.append(f'    JMP_IF_FALSE {label}')

    def generate_JMP(self, instruction):
        _, label = instruction.split()
        self.assembly_code.append(f'    JMP {label}')

    def generate_PRINT(self, instruction):
        self.assembly_code.append('    PRINT')

    def generate_ADD(self, instruction):
        self.assembly_code.append('    ADD')

    def generate_HALTS(self, instruction):
        self.assembly_code.append('    HALT')

    def generate_IF(self, instruction):
        self.assembly_code.append('IF:')
        self.label_counter += 1
        label = f'ELSE_{self.label_counter}'
        self.assembly_code.append(f'    JMP_IF_FALSE {label}')
        self.label_counter += 1
        self.assembly_code.append(f'{label}:')
        
    def generate_WHILE(self, instruction):
        self.assembly_code.append('WHILE:')
        self.label_counter += 1
        label = f'ENDWHILE_{self.label_counter}'
        self.assembly_code.append(f'    JMP_IF_FALSE {label}')
        self.label_counter += 1
        self.assembly_code.append(f'{label}:')

    def get_assembly_code(self):
        return self.assembly_code

# Example usage
instructions = [
    'PUSH 10',
    'STORE x',
    'LOAD x',
    'PUSH 5',
    'CMP_GT',
    'JMP_IF_FALSE ELSE',
    'LOAD x',
    'PRINT',
    'JMP ENDIF',
    'ELSE:',
    'PUSH 0',
    'PRINT',
    'ENDIF:',
    'PUSH 1',
    'STORE y',
    'WHILE:',
    'LOAD y',
    'PUSH 10',
    'CMP_LT',
    'JMP_IF_FALSE ENDWHILE',
    'LOAD y',
    'PRINT',
    'LOAD y',
    'PUSH 1',
    'ADD',
    'STORE y',
    'JMP WHILE',
    'ENDWHILE:',
    'HALT'
]

assembly_generator = AssemblyGenerator()
assembly_generator.generate(instructions)
assembly_code = assembly_generator.get_assembly_code()

print("Assembly Code Generation completed successfully.")
print("Generated Assembly Code:")
for line in assembly_code:
    print(line)
