import math
from pdb import set_trace

class Node:

    def __init__(self, priv=None, pub=None, name=None) -> None:
        self.parent = None
        self.left = None
        self.right = None
        self.priv = priv
        self.pub = pub
        self.name = name
    
    def set_parent(self, node):
        self.parent = node
    
    def is_root(self):
        return self.parent == None
    
    def is_leaf(self):
        return self.left == None and self.right == None

    def __repr__(self) -> str:
        return f"Pub {self.pub}"
    
    def __str__(self) -> str:
        return f"Pub {self.pub}"
    
class PublicNode(Node):

    def __init__(self, priv, pub) -> None:
        self.priv = priv
        self.pub = pub
        super(PublicNode,self).__init__()

class SecretNode(Node):

    def __init__(self, priv, pub) -> None:
        self.priv = priv
        self.pub = pub
        super(SecretNode,self).__init__()

class ProofNode(Node):
    def __init__(self, pub, name=None) -> None:
        super().__init__(None, pub, name)
    
    def __repr__(self) -> str:
        return f"Name {self.name}"
    
    def __str__(self) -> str:
        return f"Name{self.name}"

def nleft(x):
    return int(math.pow(2, math.ceil(math.log2(x))-1))

def get_sibling(node):
    if node.is_root():
        return None
    parent, is_left = node.parent
    return parent.right if is_left else parent.left

def get_leaves(node):
    if node.is_leaf():
        return [node]
    return get_leaves(node.left) + get_leaves(node.right)


def highest_power_of_2(n):
    p = int(math.log(n, 2));
    return int(pow(2, p));