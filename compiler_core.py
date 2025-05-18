from lark import Lark, Transformer
import textwrap
import networkx as nx
import matplotlib.pyplot as plt

def create_lexer():
    tokens = [
        'IDENTIFIER', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'LPAREN', 'RPAREN', 'HASH', 'ANGLE_OPEN', 'ANGLE_CLOSE',
        'STRING_LITERAL', 'LBRACE', 'RBRACE', 'SEMICOLON', 'ASSIGN', 'COMMA'
    ]

    grammar = r"""
        %ignore /\s+/      
        %ignore /\/\/.*/   

        HASH: "#"
        ANGLE_OPEN: "<"
        ANGLE_CLOSE: ">"
        STRING_LITERAL: /"[^"]*"/
        LBRACE: "{"
        RBRACE: "}"
        SEMICOLON: ";"
        ASSIGN: "="
        COMMA: ","

        IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
        NUMBER: /\d+(\.\d*)?/
        PLUS: "+"
        MINUS: "-"
        TIMES: "*"
        DIVIDE: "/"
        LPAREN: "("
        RPAREN: ")"

        start: token*
        token: IDENTIFIER
            | NUMBER
            | PLUS
            | MINUS
            | TIMES
            | DIVIDE
            | LPAREN
            | RPAREN
            | HASH
            | ANGLE_OPEN
            | ANGLE_CLOSE
            | STRING_LITERAL
            | LBRACE
            | RBRACE
            | SEMICOLON
            | ASSIGN
            | COMMA
    """

    return Lark(grammar)

def tokenize_file(filename):
    lexer = create_lexer()
    try:
        with open(filename, 'r') as file:
            source_code = file.read()

        tokens = []
        for token in lexer.lex(source_code):
            tokens.append((token.type, token.value))

        return tokens

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

filename = "abc.cpp"
tokens = tokenize_file(filename)

if tokens:
    print("Tokens found:")
    for token_type, value in tokens:
        print(f"Type: {token_type:12} Value: {value}")

class ASTNode:
    def __init__(self, node_type, value=None):
        self.type = node_type
        self.value = value
        self.children = []

class ParserTransformer(Transformer):
    def __init__(self):
        super().__init__()

    def statement(self, items):
        return items[0]

    def expression(self, items):
        if len(items) == 1:
            return items[0]

        result = items[0]
        for i in range(1, len(items)-1, 2):
            operator = items[i].value
            operand = items[i+1]

            ast_node = ASTNode("BinaryOp", operator)
            ast_node.children.append(result)
            ast_node.children.append(operand)
            result = ast_node

        return result

    def factor(self, items):
        item = items[0]
        if isinstance(item, str):
            return ASTNode("Number", int(item))
        elif isinstance(item, ASTNode):
            return item
        else:
            return ASTNode("Identifier", item)

    def declaration(self, items):
        type_spec = items[0]
        identifier = items[1]

        if len(items) == 2:
            return ASTNode("Declaration", {"type": type_spec, "name": identifier})
        else:
            return ASTNode("Assignment", {
                "type": type_spec,
                "name": identifier,
                "value": items[3]
            })

    def compound_statement(self, items):
        return ASTNode("CompoundStatement", children=[item for item in items if item])

def tokenize_and_parse(filename):
    parser = create_lexer()
    try:
        with open(filename, 'r') as file:
            source_code = file.read()

        tree = parser.parse(source_code)
        transformer = ParserTransformer()
        ast = transformer.transform(tree)
        return ast

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

ast = tokenize_and_parse(filename)

def print_ast(node, indent=""):
    if hasattr(node, 'data'):
        print(f"{indent}{node.data}", end="")
        if node.children:
            print()
            for child in node.children:
                print_ast(child, indent + " ")
        else:
            print()
    else:
        print(f"{indent}{node.type}", end="")
        if hasattr(node, 'value'):
            print(f": {node.value}")
        else:
            print()
        for child in getattr(node, 'children', []):
            print_ast(child, indent + "  ")

if ast:
    print("\nAbstract Syntax Tree:")
    print_ast(ast)

def print_ast_as_tree(node, prefix="", is_last=True):
    if hasattr(node, 'data'):
        connector = "└── " if is_last else "├── "
        print(prefix + connector + node.data)
        children_prefix = prefix + ("    " if is_last else "│   ")

        for i, child in enumerate(node.children):
            is_child_last = i == len(node.children) - 1
            print_ast_as_tree(child, children_prefix, is_child_last)

    elif hasattr(node, 'type'):
        connector = "└── " if is_last else "├── "
        print(prefix + connector + node.type)

        if hasattr(node, 'value') and node.value is not None:
            value_connector = "└── " if not hasattr(node, 'children') else "├── "
            value_prefix = prefix + ("    " if is_last else "│   ")
            print(value_prefix + value_connector + str(node.value))

        if hasattr(node, 'children'):
            children_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(node.children):
                is_child_last = i == len(node.children) - 1
                print_ast_as_tree(child, children_prefix, is_child_last)

if ast:
    print("Abstract Syntax Tree:")
    print_ast_as_tree(ast)

def ast_to_graph(node, graph, parent=None, counter=[0], leaf_nodes=set()):
    node_id = counter[0]
    label = node.type if hasattr(node, 'type') else str(node.data)
    if hasattr(node, 'value') and node.value is not None:
        label += f": {node.value}"

    wrapped_label = textwrap.fill(label, width=16)
    graph.add_node(node_id, label=wrapped_label)

    is_leaf = not getattr(node, 'children', [])
    if is_leaf:
        leaf_nodes.add(node_id)

    if parent is not None:
        graph.add_edge(parent, node_id)

    counter[0] += 1
    for child in getattr(node, 'children', []):
        ast_to_graph(child, graph, node_id, counter, leaf_nodes)

# ✅ The missing part — plot_ast function
def plot_ast(ast):
    G = nx.DiGraph()
    leaf_nodes = set()
    ast_to_graph(ast, G, leaf_nodes=leaf_nodes)

    # Use hierarchy (tree-like) layout
    def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.successors(root))
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                    vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                    pos=pos, parent=root)
        return pos

    if len(G.nodes) == 0:
        raise ValueError("AST graph is empty. Cannot draw AST.")
    root_node = list(G.nodes)[0]
    pos = hierarchy_pos(G, root=root_node)

    labels = nx.get_node_attributes(G, 'label')

    plt.figure(figsize=(14, 10))
    nx.draw(G, pos, with_labels=False, arrows=True, node_size=1800, node_color="lightblue", font_size=10)
    nx.draw_networkx_labels(G, pos, labels, font_size=9)

    plt.title("Abstract Syntax Tree (Tree Layout)")
    plt.axis('off')
    plt.savefig("ast_tree.png")
    plt.show()


# Call to generate image
if ast:
    plot_ast(ast)
