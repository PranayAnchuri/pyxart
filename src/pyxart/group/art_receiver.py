from .utils import keyexchange, reduce_path, create_leaf_node
from .tree import get_leaves
from .art import create_copath
import pickle

def process_group_message(creation_pickle, client, users):
    grp = pickle.loads(creation_pickle)
    leaf_nodes = get_leaves(grp.tree)
    node = leaf_nodes[grp.participants.index(client.name)]
    user_mapping = dict([(u.name, u) for u in users])
    path = [_ for _ in create_copath(node)]
    leaf_key = keyexchange(client.pre_key.priv, client.iden_key.priv, user_mapping[grp.initiator].iden_key_pub, grp.setup_key)
    secret = create_leaf_node(leaf_key)
    recon = reduce_path(secret, path)
    return recon.priv