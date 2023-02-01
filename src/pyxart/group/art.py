from turtle import pu
from ..keys import KeyPairCurve25519
from nacl.bindings.crypto_scalarmult import crypto_scalarmult
from collections import namedtuple
from .tree import (
    ProofNode,
    nleft,
    get_sibling,
    Node,
    get_leaves,
    highest_power_of_2,
)
from .utils import keyexchange, get_pub, dh, reduce_path, create_leaf_node
from collections import namedtuple


GroupSetupMessage = namedtuple(
    "GroupSetupMessage", "initiator participants setup_key tree"
)


def compute_parent(left, right):
    """Create a parent node from left and right child nodes

    Args:
        left (Node): left sibling
        right (Node): right sibling

    Returns:
        Node: Parent node
    """
    return dh(left.priv, right.pub)


def create_level(left, right):
    """Create a new level in the tree by creating a parent of two nodes

    Args:
        left (Node): left root
        right (Nodfe): right root

    Returns:
        Node: Parent node in the next higher level
    """
    parent = compute_parent(left, right)
    parent.left = left
    parent.right = right
    left.parent = (parent, True)
    right.parent = (parent, False)
    return parent


def compute_tree_secret(secrets):
    """Recursively calculate the tree secret from leaf node secrets

    Args:
        secrets (list): list of leaf secrets

    Returns:
        Node: Root node with secrets
    """
    if len(secrets) == 1:
        return secrets[0]
    num_nodes_in_left = nleft(len(secrets))
    left = compute_tree_secret(secrets[:num_nodes_in_left])
    right = compute_tree_secret(secrets[num_nodes_in_left:])
    return create_level(left, right)


def create_proof_node(node):
    """Create proof node object from tree node

    The proof node objects contain only the public keys

    Args:
        node (Node): Tree node

    Returns:
        ProofNode: Proof node object containing the public key
    """
    return ProofNode(node.pub)


def create_group(members, creator_name, creator_priv_key):
    """Create an encrypted group with given members

    Creator uses members public keys to create initial leaf secrets for the
    members
    Leaf secrets are then composed into a tree in a bottom up fashion


    Args:
        members (list): Members in the group
        creator_name (str): Group creator
        creator_priv_key (bytes): Creators private key for the group

    Returns:
        tuple: (setup message, root secret, creators leaf key)
    """
    secrets = []
    setup_key = KeyPairCurve25519.generate()
    creator_leaf_key = KeyPairCurve25519.generate()
    secrets.append(
        create_leaf_node(
            priv=creator_leaf_key.priv, name=f"Group creator's initiation key"
        )
    )
    for participant in members:
        leaf_key = keyexchange(
            setup_key.priv,
            creator_priv_key,
            participant.iden_key_pub,
            participant.pre_key_pub,
        )
        secrets.append(
            create_leaf_node(
                priv=leaf_key,
                name=f"Shared key between ({creator_name}, {participant.name})",
            )
        )
    tree = compute_tree_secret(secrets)
    return (
        create_setup_message(
            tree,
            [creator_name] + [x.name for x in members],
            setup_key.pub,
            creator_name,
        ),
        tree.priv,
        creator_leaf_key.priv,
    )


def create_copath(leaf_node):
    """
    Return public keys on the copath for index^{th} leaf
    """
    while not leaf_node.is_root():
        # yield create_proof_node(get_sibling(leaf_node))
        yield get_sibling(leaf_node)
        leaf_node, _ = leaf_node.parent


def update_copath(leaf_node, updates):
    """
    Return public keys on the copath for index^{th} leaf
    """
    while not leaf_node.is_root():
        sibling = get_sibling(leaf_node)
        sibling.pub = updates.pop(0)
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
    """Creates a setup message for other members to reconstruct the root secret

    Args:
        tree (Node): current tree
        members (list): list of group members
        setup_key (bytes): Group setup key
        creator_name (str): Group creators name

    Returns:
        GroupSetupMessage: padded setup message
    """
    return GroupSetupMessage(creator_name, members, setup_key, create_proof_tree(tree))


def add_to_tree(tree, leaf):
    """Add new member to tree

    Args:
        tree (Node): current tree
        leaf (bytes): leaf secret

    Returns:
        Node: Updated root node
    """
    leaves = get_leaves(tree)
    nl = len(leaves)
    hp2 = highest_power_of_2(nl)
    if hp2 == nl:
        # create a new node and join
        leaf = Node(data=[leaf])
        return create_level(tree, leaf)
    else:
        tree.right = add_to_tree(tree.right, leaf)
        tree.data = tree.left.data + tree.right.data
        return tree
