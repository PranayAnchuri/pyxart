from .utils import keyexchange, reduce_path, create_leaf_node
from .tree import get_leaves
from .art import create_copath
import pickle
from ..client import Client

def process_group_message(group, client, users):
    '''Function to construct group secret based on creation message'''
    group_name = group.name.name
    art = group.creation_message.art
    setup_message = pickle.loads(art)
    leaf_nodes = get_leaves(setup_message.tree)
    node = leaf_nodes[setup_message.participants.index(client.name)]
    user_mapping = dict([(u.name, u) for u in users])
    path = [_ for _ in create_copath(node)]
    if setup_message.initiator == client.name:
        # use creator key
        leaf_key = client.get_creator_key(group_name)
    else:
        leaf_key = keyexchange(client.get_pre_key_priv(), client.get_iden_key_priv(), user_mapping[setup_message.initiator].iden_key_pub, setup_message.setup_key)
    secret = create_leaf_node(leaf_key)
    recon = reduce_path(secret, path)
    print(secret, client.get_pre_key_priv(), client.get_iden_key_priv())
    return recon.priv