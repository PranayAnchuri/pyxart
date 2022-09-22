from nacl.bindings.crypto_scalarmult import crypto_scalarmult
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from .tree import ProofNode, nleft, get_sibling, SecretNode, PublicNode, Node
from cryptography.hazmat.backends import default_backend
import libnacl

def keyexchange(s1, s2, o1, o2):
    return crypto_scalarmult(s1, o2)

def reduce_path(secret, path):
    intermediate = []
    for node in path:
        secret = dh(secret.priv, node.pub)
        intermediate.append(ProofNode(secret.pub))
    return secret, intermediate

def update_pub_on_path(secret, path):
    for node in path:
        secret = dh(secret.priv, node.pub)
        node.parent[0].pub = secret.pub
    return secret.priv


def kdf(secret_key_material):
    """
    :param secret_key_material: A bytes-like object encoding the secret key material.
    :returns: A bytes-like object encoding the shared secret key.
    """

    salt = b"\x00"
    input_key_material = secret_key_material
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=None, backend=default_backend())
    return hkdf.derive(input_key_material)

def get_pub(priv):
    return libnacl.crypto_scalarmult_base(priv)

def dh(priv, pub):
    shared_secret = crypto_scalarmult(priv, pub)
    parent_priv = kdf(shared_secret)
    parent_pub = get_pub(parent_priv)
    return Node(parent_priv, parent_pub)

def create_leaf_node(priv, name=None):
    return Node(priv, get_pub(priv), name)