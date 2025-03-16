# Codex Parsing

Code for example: [py-tree-sitter](https://github.com/tree-sitter/py-tree-sitter)

I'll create a tutorial based on the py-tree-sitter README.md file to extract the `greet` method from your Python code using Tree-sitter. The README provides guidance on setting up and using the Python bindings for Tree-sitter, which we'll adapt for this task.

### Tutorial: Extracting the `greet` Method Using py-tree-sitter

#### Step 1: Prerequisites
To follow this tutorial, you'll need:
- Python 3 installed
- The `py-tree-sitter` package
- The `tree-sitter-python` language implementation

Install them using pip:
```bash
pip install tree-sitter tree-sitter-python
```

#### Step 2: Setup and Imports
First, we need to import the necessary modules and set up the Tree-sitter parser with the Python language. Here's the initial code:

```python
from tree_sitter import Language, Parser
import tree_sitter_python as tspython

# Initialize the Python language
PY_LANGUAGE = Language(tspython.language())

# Create a parser and set the language
parser = Parser(PY_LANGUAGE)
```

This code follows the README's example of setting up a parser with the Python language binding.

#### Step 3: Define the Source Code
We'll use your provided Python code as the source to parse. Let's define it as a string:

```python
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
```

#### Step 4: Parse the Source Code
Using the parser, we'll generate a syntax tree from the source code:

```python
tree = parser.parse(source_code.encode('utf8'))
```

The README mentions parsing accepts bytes, so we encode the string as UTF-8.

#### Step 5: Traverse the Syntax Tree
To find the `greet` function, we need to traverse the syntax tree and locate the function definition with the name "greet". We'll use a simple recursive function to explore the tree:

```python
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
```

#### Step 6: Extract the Code
Once we have the node for the `greet` function, we can extract its text from the source code using the node's byte range:

```python
if greet_node:
    greet_code = source_code[greet_node.start_byte:greet_node.end_byte]
    print("Extracted 'greet' function code:")
    print(greet_code)
else:
    print("Function 'greet' not found!")
```

#### Complete Tutorial Code
Here's the full script combining all steps:

```python
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

# Function to find a specific function node
def find_function_node(node, function_name):
    if node.type == 'function_definition':
        name_node = node.children[1]
        if name_node.type == 'identifier' and source_code[name_node.start_byte:name_node.end_byte] == function_name:
            return node
    for child in node.children:
        result = find_function_node(child, function_name)
        if result:
            return result
    return None

# Find and extract the 'greet' function
root_node = tree.root_node
greet_node = find_function_node(root_node, 'greet')

if greet_node:
    greet_code = source_code[greet_node.start_byte:greet_node.end_byte]
    print("Extracted 'greet' function code:")
    print(greet_code)
else:
    print("Function 'greet' not found!")
```

#### Output
Running this script will output:
```
Extracted 'greet' function code:
def greet():
    print("Hello from codex-parsing!")
```

#### Explanation
- The README guided us to use `Language` and `Parser` from `tree_sitter` and the Python-specific language binding from `tree_sitter_python`.
- We parsed the code into a syntax tree and traversed it to find the `function_definition` node named "greet".
- The byte positions (`start_byte` and `end_byte`) from the node allowed us to extract the exact text of the `greet` function.

#### Notes
- The README suggests exploring `examples/usage.py` for more examples, but this tutorial adapts the basic parsing approach to our specific need.
- This method assumes a simple structure; for more complex cases (e.g., nested functions), you might need to refine the traversal logic.

This tutorial leverages py-tree-sitter to successfully extract the `greet` method from your Python code!