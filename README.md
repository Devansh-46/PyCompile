# PyCompile

![PyCompile](https://img.shields.io/badge/language-Python-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

PyCompile is a simple and intuitive compiler for a custom programming language. It takes source code as input, tokenizes it, parses it into a syntax tree, and performs semantic analysis. The project is designed to be educational, demonstrating how a compiler works from source code to execution.

## Features
- **Lexical Analysis**: Tokenizes the input source code.
- **Syntax Analysis**: Parses tokens into a syntax tree.
- **Semantic Analysis**: Checks for semantic errors.
- **Intermediate Representation**: Generates an intermediate representation of the code.
- **Code Generation**: Generates low-level code from the intermediate representation.
- **Assembly Generation**: Converts low-level code to assembly instructions.
- **Virtual Machine**: Executes the generated assembly instructions.
- **Command-Line Interface**: Simple interface to compile and execute source code files.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Classes and Methods](#classes-and-methods)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install and set up PyCompile, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Devansh-46/PyCompile.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd PyCompile
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use the compiler, run the `main.py` script with the path to your source code file as an argument:

```bash
python main.py <path_to_source_code>
```


## Examples

Create a file named `example.src` with the following content:

```python
def add(x, y) {
    x + y
}

z = add(5, 3);
print(z);
```

Run the compiler:

```bash
python main.py example.src
```

## Project Structure

```css
PyCompile/
├── main.py
├── lexer.py
├── parser.py
├── semantic_analyzer.py
├── ir_generator.py
├── code_generator.py
├── assembly_generator.py
├── vm.py
├── node.py
├── mytoken.py
└── tests/
    ├── test_lexer.py
    ├── test_parser.py
    ├── test_semantic_analyzer.py
    ├── test_ir_generator.py
    ├── test_code_generator.py
    ├── test_assembly_generator.py
    └── test_vm.py

```

- main.py: Entry point for the compiler. Handles reading input files and orchestrating the compilation process.
- lexer.py: Handles lexical analysis, converting source code into tokens.
- parser.py: Handles syntax analysis, converting tokens into a syntax tree.
- semantic_analyzer.py: Performs semantic checks on the syntax tree.
- ir_generator.py: Generates an intermediate representation of the code.
- code_generator.py: Generates low-level code from the intermediate representation.
- assembly_generator.py: Converts low-level code to assembly instructions.
- vm.py: A virtual machine to execute the generated assembly instructions.
- node.py: Defines the Node class used in the syntax tree.
- mytoken.py: Defines the Token class used in lexical analysis.
- tests/: Contains test cases for various components of the compiler.
