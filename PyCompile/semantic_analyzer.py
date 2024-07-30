class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.current_scope = "global"
        self.error = False
        self.error_message = ""
        self.current_function = None
        self.current_function_params = []
        self.current_function_return_type = None
        self.current_function_return_value = None
    
    def add_symbol(self, symbol, value, scope="global"):
        if scope == "global":
            self.symbol_table[symbol] = value
        else:
            if scope not in self.symbol_table:
                self.symbol_table[scope] = {}
            self.symbol_table[scope][symbol] = value
    
    def analyze(self, ast):
        self.visit(ast)

    def visit(self, node):
        if isinstance(node, tuple):
            node_type = node[0]
            if hasattr(self, f'visit_{node_type}'):
                method = getattr(self, f'visit_{node_type}')
                method(node)
            elif node_type in ('==', '!=', '<', '>', '<=', '>='):
                self.visit_comparison(node)
            else:
                raise Exception(f'No visit_{node_type} method')
        elif isinstance(node, list):
            for subnode in node:
                self.visit(subnode)
        elif isinstance(node, dict):
            for key, value in node.items():
                self.visit(value)
        else:
            # Handle other types of nodes if necessary
            pass

    def visit_program(self, node):
        _, statements = node
        self.visit(statements)

    def visit_assign(self, node):
        _, name, value = node
        self.visit(value)
        self.symbol_table[name] = value

    def visit_print(self, node):
        _, value = node
        self.visit(value)

    def visit_tuple(self, node):
        _, elements = node
        for element in elements:
            self.visit(element)

    def visit_string(self, node):
        # Strings are considered valid as-is in this context
        pass
  
    def visit_if(self, node):
        _, condition, then_body = node
        self.visit(condition)
        self.visit(then_body)

    def visit_else(self, node):
        _, else_body = node
        self.visit(else_body)

    def visit_if_else(self, node):
        _, condition, then_body, else_body = node
        self.visit(condition)
        self.visit(then_body)
        self.visit(else_body)

    def visit_while(self, node):
        _, condition, body = node
        self.visit(condition)
        self.visit(body)

    def visit_function(self, node):
        _, name, body = node
        self.symbol_table[name] = ('function', body)

    def visit_call(self, node):
        _, name, args = node
        if name not in self.symbol_table:
            raise ValueError(f"Undefined function '{name}'")
        _, body = self.symbol_table[name]
        if len(args) != len(body[1]):
            raise ValueError(f"Function '{name}' expects {len(body[1])} arguments, but got {len(args)}")
        for arg in args:
            self.visit(arg)

    def visit_bin_op(self, node):
        _, left, right = node
        self.visit(left)
        self.visit(right)

    def visit_cmp(self, node):
        _, left, right = node
        self.visit(left)
        self.visit(right)

    def visit_number(self, node):
        # Numbers are considered valid as-is in this context
        pass

    def visit_identifier(self, node):
        if node not in self.symbol_table:
            raise ValueError(f"Undefined identifier '{node}'")
        _, value = self.symbol_table[node]
        return value

    def visit_function_definition(self, node):
        _, name, params, return_type, body = node
        self.current_function = name
        self.current_function_params = params
        self.current_function_return_type = return_type
        self.visit(body)
    
    def visit_return(self, node):
        _, value = node
        self.current_function_return_value = value
        self.visit(value)
    
    def visit_function_call(self, node):
        _, name, args = node
        if name not in self.symbol_table:
            raise ValueError(f"Undefined function '{name}'")
        _, params, return_type, body = self.symbol_table[name]
        if len(args) != len(params):
            raise ValueError(f"Function '{name}' expects {len(params)} arguments, but got {len(args)}")
        for arg in args:
            self.visit(arg)
        if return_type != 'VOID':
            if self.current_function_return_value is None:
                raise ValueError(f"Function '{name}' must return a value of type '{return_type}'")
            if self.current_function_return_value[0] != return_type:
                raise ValueError(f"Function '{name}' must return a value of type '{return_type}', but got '{self.current_function_return_value[0]}'")
        self.current_function_return_value = None

    def visit_comparison(self, node):
        # Check if the node has the correct number of elements
        if len(node) < 3:
            raise ValueError(f"Comparison node is malformed: {node}")

        _, left, right = node if len(node) == 3 else (None, None, None)

        # Node should be in the form (op, left, right)
        op = node[0]
        self.visit(left)
        self.visit(right)
        if op not in ('==', '!=', '<', '>', '<=', '>='):
            raise ValueError(f"Unsupported comparison operator '{op}'")
        
    def generic_visit(self, node):
        if hasattr(node, 'children'):
            for child in node.children:
                self.visit(child)
        elif isinstance(node, dict):
            for key, value in node.items():
                self.visit(value)
