from turtle import pu
from itertools import tee
import pyxart.keys as keys
from nacl.bindings.crypto_scalarmult import crypto_scalarmult
from collections import namedtuple
from .tree import ProofNode, nleft, get_sibling, SecretNode, PublicNode, Node
from .utils import keyexchange, get_pub, dh, reduce_path, create_leaf_node
from collections import namedtuple


GroupSetupMessage = namedtuple('GroupSetupMessage','initiator participants setup_key tree')

def compute_parent(left, right):
    return dh(left.priv, right.pub)

def compute_tree_secret(secrets):
    if len(secrets) == 1:
        return secrets[0]
    num_nodes_in_left = nleft(len(secrets))
    left = compute_tree_secret(secrets[:num_nodes_in_left])
    right = compute_tree_secret(secrets[num_nodes_in_left:])
    # compute parent node
    parent = compute_parent(left, right)
    parent.left = left
    parent.right = right
    left.parent = (parent, True)
    right.parent = (parent, False)
    return parent

def create_proof_node(node):
    return ProofNode(node.pub)


def create_group(members, creator_name, creator_priv_key):
    secrets = []
    setup_key = keys.KeyPairCurve25519.generate()
    creator_leaf_key = keys.KeyPairCurve25519.generate()
    secrets.append(create_leaf_node(priv=creator_leaf_key.priv, name=f"Group creator's initiation key"))
    for participant in members:
        leaf_key = keyexchange(setup_key.priv, creator_priv_key, participant.iden_key_pub, participant.pre_key_pub)
        secrets.append(create_leaf_node(priv=leaf_key, name=f"Shared key between ({creator_name}, {participant.name})"))
    tree = compute_tree_secret(secrets)
    return create_setup_message(tree, members, setup_key, creator_name), tree.priv, creator_leaf_key.priv

def create_copath(leaf_node):
    """
    Return public keys on the copath for index^{th} leaf
    """
    while not leaf_node.is_root():
        yield create_proof_node(get_sibling(leaf_node))
        leaf_node, _ = leaf_node.parent

def create_proof_tree(tree: Node) -> ProofNode:
    if tree is None:
        return tree
    proof_root = ProofNode(tree.pub, tree.name)
    proof_root.left = create_proof_tree(tree.left)
    proof_root.right = create_proof_tree(tree.right)
    if proof_root.left is not None:
        proof_root.left.parent = (proof_root, True)
    if proof_root.right is not None:
        proof_root.right.parent = (proof_root, False)
    return proof_root

def create_setup_message(tree, members, setup_key, creator_name):
    return GroupSetupMessage(creator_name, [creator_name] + [p.name for p in members], setup_key.pub, create_proof_tree(tree))