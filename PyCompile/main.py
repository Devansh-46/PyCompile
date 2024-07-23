import sys
from lexer import tokenize
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from ir_generator import IRGenerator
from code_generator import CodeGenerator
from assembly_generator import AssemblyGenerator
from vm import VM

def main():
    """
    Main entry point.

    Reads source code from command-line input, tokenizes it, parses it into an AST,
    compiles the AST into bytecode, and runs the bytecode in a virtual machine.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_file>")
        return

    source_file = sys.argv[1]

    try:
        with open(source_file, 'r') as file:
            source_code = file.read()

        # Lexical Analysis
        tokens = tokenize()
        print("Tokens:", tokens)

        # Syntax Analysis
        parser = Parser(tokens)
        ast = parser.parse()
        print("AST:", ast)

        # Semantic Analysis
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast)
        symbol_table = semantic_analyzer.symbol_table
        print("Symbol Table:", symbol_table)

        # Intermediate Representation (IR) Generation
        ir_generator = IRGenerator()
        ir_tree = ir_generator.generate_ir(ast, symbol_table)
        print("IR Tree:", ir_tree)

        # Code Generation
        code_generator = CodeGenerator()
        instructions = code_generator.generate_code(ir_tree, symbol_table)
        print("Generated Instructions:")
        for instruction in instructions:
            print(instruction)

        # Assembly Code Generation
        assembly_generator = AssemblyGenerator()
        assembly_code = assembly_generator.generate_assembly(instructions)
        print("Generated Assembly Code:")
        for line in assembly_code:
            print(line)

        # Virtual Machine Execution
        vm = VM()
        bytecode = vm.compile_to_bytecode(ast)
        print("Bytecode:", bytecode)
        execution_result = vm.run(bytecode)
        print("Execution Output:", execution_result)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()