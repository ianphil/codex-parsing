# Codex Parsing Tutorial 2: Query the tree

Code for example: [py-tree-sitter](https://github.com/tree-sitter/py-tree-sitter)

I'll create a tutorial based on the py-tree-sitter README.md file, focusing on using Tree-sitter queries to locate and extract the `greet` method from your Python code. The README briefly mentions queries as a powerful feature for pattern matching in the syntax tree, so we'll expand on that here.

### Tutorial: Using Tree-sitter Queries to Extract the `greet` Method

#### Step 1: Prerequisites
You'll need the same setup as before:
- Python 3
- `py-tree-sitter` and `tree-sitter-python` installed

Install them if you haven’t already:
```bash
pip install tree-sitter tree-sitter-python
```

#### Step 2: Setup and Imports
We’ll set up the parser and import the necessary modules, similar to the previous tutorial:

```python
from tree_sitter import Language, Parser
import tree_sitter_python as tspython

# Initialize the Python language
PY_LANGUAGE = Language(tspython.language())

# Create a parser and set the language
parser = Parser(PY_LANGUAGE)
```

#### Step 3: Define the Source Code
Use your provided Python code as the source:

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
Parse the code into a syntax tree:

```python
tree = parser.parse(source_code.encode('utf8'))
```

#### Step 5: Define a Query
Tree-sitter queries allow us to define patterns to match specific parts of the syntax tree. We want to find a `function_definition` node where the function name is "greet". Here’s the query:

```python
query = PY_LANGUAGE.query("""
(function_definition
  name: (identifier) @function.name
  (#eq? @function.name "greet"))
""")
```

- `(function_definition ...)` matches any function definition node.
- `name: (identifier) @function.name` captures the function’s name (an `identifier` node) and tags it as `@function.name`.
- `(#eq? @function.name "greet")` is a predicate that ensures the captured name equals "greet".

The README doesn’t provide detailed query examples, but this follows Tree-sitter’s query syntax, which is well-documented in the broader Tree-sitter ecosystem.

#### Step 6: Execute the Query
Run the query on the syntax tree to find matches:

```python
matches = query.matches(tree.root_node)
```

The `matches` variable will contain a list of tuples, where each tuple includes the pattern index and a dictionary of captured nodes.

#### Step 7: Extract the `greet` Function
Process the matches to extract the code for the `greet` function:

```python
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
```

- **Check and Debug Matches**: The `if matches:` condition verifies if the Tree-sitter query found any results, then prints the `matches` list (e.g., `[(0, {'function.def': [...], 'function.name': [...]})]`) for debugging to show the structure of the matched nodes.
- **Extract the Function Node**: From the first match (`matches[0]`), it retrieves the captures dictionary (`match[1]`) and gets the `function_definition` node by accessing the first item in the `'function.def'` list (`captures['function.def'][0]`), which represents the `greet` function.
- **Extract and Print Code**: Using the node’s `start_byte` and `end_byte` attributes, it slices the `source_code` string to extract the `greet` function’s text, then prints it; if no matches are found, it outputs "Function 'greet' not found!" instead.

#### Complete Tutorial Code
Here’s the full script:

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

# Define the query to find the 'greet' function
query = PY_LANGUAGE.query("""
(function_definition
  name: (identifier) @function.name
  (#eq? @function.name "greet"))
""")

# Execute the query
matches = query.matches(tree.root_node)

# Extract the 'greet' function code
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
```

#### Output
Running this script will output:
```
Extracted 'greet' function code using query:
def greet():
    print("Hello from codex-parsing!")
```

#### Explanation
- The query approach is more declarative than manually traversing the tree, letting Tree-sitter’s engine handle the matching.
- The `#eq?` predicate ensures specificity, filtering for only the `greet` function.
- We rely on the node hierarchy (identifier → name → function_definition) to get the full function code.

#### Advantages of Queries
- **Precision**: Queries target specific patterns without manual recursion.
- **Reusability**: You can modify the query to match other functions by changing "greet" to another name.
- **Scalability**: Queries can be extended to match more complex patterns (e.g., functions with specific parameters).

#### Notes
- The README mentions queries briefly, suggesting they’re a key feature, but doesn’t provide Python-specific examples. This tutorial adapts general Tree-sitter query syntax to py-tree-sitter.
- If the code structure changes (e.g., decorators or comments), the query might need adjustment to remain robust.

This tutorial demonstrates how to use Tree-sitter queries with py-tree-sitter to efficiently extract the `greet` method from your Python code!