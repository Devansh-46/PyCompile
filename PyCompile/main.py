import os
import time
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from ir_generator import IRGenerator
from code_generator import CodeGenerator
from assembly_generator import AssemblyGenerator
from vm import VM

def main():
    print("Starting compilation process...")

    source_file = 'source.py'

    # Check if the source file exists
    if not os.path.exists(source_file):
        print(f"Source file '{source_file}' does not exist. Creating one...")
        with open(source_file, 'w') as file:
            code = input("Please enter the source code:\n")
            file.write(code)
        print(f"Source file '{source_file}' created.")

    # Read source code from the file
    with open(source_file, 'r') as file:
        source_code = file.read()
    print("Source code read successfully.")

    try:
        # Step 1: Lexical Analysis
        print("Starting lexical analysis...")
        start_time = time.time()
        lexer = Lexer()
        lexer.build()
        tokens = lexer.tokenize(source_code)
        end_time = time.time()
        print(f"Lexical analysis completed in {end_time - start_time:.4f} seconds. Tokens generated:")
        for token in tokens:
            print(token)
        
        # Step 2: Parsing
        print("Starting parsing...")
        start_time = time.time()
        parser = Parser()
        ast = parser.parse(source_code)
        end_time = time.time()
        print(f"Parsing completed in {end_time - start_time:.4f} seconds. AST generated:")
        print(ast)

        # Step 3: Semantic Analysis
        print("Starting semantic analysis...")
        start_time = time.time()
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast)
        end_time = time.time()
        print(f"Semantic analysis completed in {end_time - start_time:.4f} seconds.")

        # Step 4: Intermediate Representation Generation
        print("Starting IR generation...")
        start_time = time.time()
        ir_generator = IRGenerator()
        ir = ir_generator.generate(ast)
        end_time = time.time()
        print(f"IR generation completed in {end_time - start_time:.4f} seconds. IR generated:")
        print(ir)

        # Print the AST for debugging purposes
        print("AST:")
        print(ast)

        # Step 5: Code Generation
        print("Starting code generation...")
        start_time = time.time()
        code_generator = CodeGenerator()
        machine_code = code_generator.generate(ir)
        end_time = time.time()
        print(f"Code generation completed in {end_time - start_time:.4f} seconds. Machine code generated:")
        print(machine_code)

        # Step 6: Assembly Generation
        print("Starting assembly generation...")
        start_time = time.time()
        assembly_generator = AssemblyGenerator()
        assembly_code = assembly_generator.generate(ir)
        end_time = time.time()
        print(f"Assembly generation completed in {end_time - start_time:.4f} seconds. Assembly code generated:")
        print(assembly_code)

        # Step 7: Virtual Machine Execution
        print("Starting virtual machine execution...")
        start_time = time.time()
        vm = VM()
        vm.load(assembly_code)
        vm.run()
        end_time = time.time()
        print(f"Virtual machine execution completed in {end_time - start_time:.4f} seconds.")
            

    # except LexerError as e:
    #     print(f"Lexer error: {e}")
    except SyntaxError as e:
        print(f"Parser error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
