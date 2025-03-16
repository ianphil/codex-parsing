from tree_sitter import Language, Parser
import tree_sitter_python as tspython

PY_LANGUAGE = Language(tspython.language())

parser = Parser(PY_LANGUAGE)

tree = parser.parse(
    bytes(
        """
def foo(thing: str):
    if bar:
        baz()

def baz():
    pass
""",
        "utf8"
    )
)

# Print the tree structure
def print_tree(node, indent=0):
    print(" " * indent + node.type)
    for child in node.children:
        print_tree(child, indent + 2)

print_tree(tree.root_node)
