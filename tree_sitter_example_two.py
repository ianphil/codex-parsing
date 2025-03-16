from tree_sitter import Language, Parser
import tree_sitter_python as tspython

# Initialize the Python language
PY_LANGUAGE = Language(tspython.language())

# Create a parser and set the language
parser = Parser(PY_LANGUAGE)

# Define the source code
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

# Parse the source code
tree = parser.parse(source_code.encode('utf8'))

# Define the query to find the 'greet' function
query = PY_LANGUAGE.query("""
(function_definition
  name: (identifier) @function.name
  (#eq? @function.name "greet")) @function.def
""")

# Execute the query
matches = query.matches(tree.root_node)

if matches:
    # Debugging: Print the match structure
    print("Matches found:", matches)
    
    # Take the first match
    match = matches[0]
    captures = match[1]  # Dictionary of captures
    
    # Get the function_definition node (first item in the list)
    greet_node = captures['function.def'][0]  # Access the first Node
    
    # Extract the code
    greet_code = source_code[greet_node.start_byte:greet_node.end_byte]
    print("Extracted 'greet' function code using query:")
    print(greet_code)
else:
    print("Function 'greet' not found!")