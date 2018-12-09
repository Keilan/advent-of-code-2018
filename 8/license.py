import sys


class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def __str__(self):
        return 'Node with {} children and metadata {}'.format(len(self.children), self.metadata)


def build_tree(tree, info):
    """
    Recursively builds a tree.
    """
    # Remove information for the current node
    num_children, num_metadata = info[:2]
    info = info[2:]

    # Create children (recursively)
    children = []
    for _ in range(num_children):
        child, info, tree = build_tree(tree, info)
        children.append(child)

    # Remove metadata
    metadata = info[:num_metadata]
    info = info[num_metadata:]

    node = Node(children, metadata)
    tree.append(node)
    return node, info, tree


def get_value(node):
    """
    Get the value of a node.
    """
    if len(node.children) == 0:
        return sum(node.metadata)
    else:
        total = 0
        for index in node.metadata:
            try:
                total += get_value(node.children[index-1])
            except IndexError:
                pass
        return total


def print_node(node, indent):
    """
    A helper function to visualize the nodes.
    """
    print(' ' * indent, str(node), ': Children are:')
    for c in node.children:
        print_node(c, indent + 2)


def license():
    license = sys.stdin.readline().split()
    license = [int(x) for x in license]

    # Build the tree
    tree = []
    root, _, tree = build_tree(tree, license)

    # Sum Metadata
    total_metadata = sum([sum(node.metadata) for node in tree])
    print('Sum of metadata is {}'.format(total_metadata))

    # Get Node Value
    root_value = get_value(root)
    print('The value of the root node is {}'.format(root_value))

license()
