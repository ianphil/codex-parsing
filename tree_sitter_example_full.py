from tree_sitter import Language, Parser
import tree_sitter_python as tspython

# Initialize the Python language
PY_LANGUAGE = Language(tspython.language())

# Create a parser and set the language
parser = Parser(PY_LANGUAGE)

source_code = '''
def main():
    print("Hello from codex-parsing!")

def greet():
    print("Hello from codex-parsing!")

def farewell():
    print("Goodbye from codex-parsing!")

if __name__ == "__main__":
    main()
'''

tree = parser.parse(source_code.encode('utf8'))

def find_function_node(node, function_name):
    if node.type == 'function_definition':
        # Check the function name (first child is usually the 'def' keyword, second is the identifier)
        name_node = node.children[1]
        if name_node.type == 'identifier' and source_code[name_node.start_byte:name_node.end_byte] == function_name:
            return node
    # Recursively search children
    for child in node.children:
        result = find_function_node(child, function_name)
        if result:
            return result
    return None

# Find the 'greet' function
root_node = tree.root_node
greet_node = find_function_node(root_node, 'greet')

if greet_node:
    greet_code = source_code[greet_node.start_byte:greet_node.end_byte]
    print("Extracted 'greet' function code:")
    print(greet_code)
else:
    print("Function 'greet' not found!")
