import os

from anytree import Node
from anytree.exporter import UniqueDotExporter


def set_edge(node, child):
    return 'color=red' if child.best else ''

def save_tree(root: Node):
    UniqueDotExporter(root, edgeattrfunc=set_edge).to_picture("trace.pdf")
    os.system('open trace.pdf')