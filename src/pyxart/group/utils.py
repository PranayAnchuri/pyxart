from nacl.bindings.crypto_scalarmult import crypto_scalarmult
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from .tree import ProofNode, Node
from cryptography.hazmat.backends import default_backend
import libnacl


def keyexchange(s1, s2, o1, o2):
    """Generate a shared secred secret

    Args:
        s1 (bytes): scalar 1
        s2 (bytes): scalar 2
        o1 (bytes): pubkey 1
        o2 (bytes): pubkey 2

    Returns:
        bytes: shared secret
    """
    return crypto_scalarmult(s1, o2)


def reduce_path(secret, path):
    """Reduce a given list of public key nodes using an initial secret

    reduce(priv, [pub1, pub2, pub3]) = dh(dh(dh(priv, pub1).priv, pub2), pub3)

    Args:
        secret (bytes): initial secret
        path (node): list of tree nodes with public keys

    Returns:
        tuple: tup1 = reduced secret and tup2 = intermediate secrets
    """
    intermediate = []
    for node in path:
        secret = dh(secret.priv, node.pub)
        intermediate.append(ProofNode(secret.pub))
    return secret, intermediate


def update_pub_on_path(secret, path):
    """Update public keys on the copath

    Args:
        secret (bytes): initial secret
        path (list): copath

    Returns:
        bytes: reduced secret
    """
    for node in path:
        secret = dh(secret.priv, node.pub)
        node.parent[0].pub = secret.pub
    return secret.priv


def kdf(secret_key_material):
    """Key derivation function

    Args:
        secret_key_material (bytes): encoding of secret material

    Returns:
        bytes: EC scalar
    """
    input_key_material = secret_key_material
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=None,
        backend=default_backend(),
    )
    return hkdf.derive(input_key_material)


def get_pub(priv):
    """Utility function to get public key from private

    Args:
        priv (bytes): EC scalar

    Returns:
        bytes: EC point obtained by multiplying scalar with group generator
    """
    return libnacl.crypto_scalarmult_base(priv)


def dh(priv, pub):
    """Performs a round of Diffie-Hellman and derives a keypair

    Args:
        priv (bytes): private key
        pub (bytes): public key of other

    Returns:
        Node: node containing a keypair derived from the shared secret
    """
    shared_secret = crypto_scalarmult(priv, pub)
    parent_priv = kdf(shared_secret)
    parent_pub = get_pub(parent_priv)
    return Node(parent_priv, parent_pub)


def create_leaf_node(priv, name=None):
    """Create a leaf node with given private key

    Args:
        priv (bytes): private key
        name (str, optional): Name for this node. Defaults to None.

    Returns:
        Node: node with private, public keys and optional name
    """
    return Node(priv, get_pub(priv), name)
