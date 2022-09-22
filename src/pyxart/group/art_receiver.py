from .utils import keyexchange, reduce_path, create_leaf_node, get_pub, update_pub_on_path
from .tree import get_leaves
from .art import create_copath, create_setup_message
import pickle
from ..client import Client

def _unpack(group, users):
    group_name = group.name.name
    art = group.creation_message.art
    setup_message = pickle.loads(art)
    user_mapping = dict([(u.name, u) for u in users])
    return group_name, setup_message.tree, setup_message.initiator, user_mapping[setup_message.initiator].iden_key_pub, setup_message.participants, setup_message.setup_key

def _path(tree, participants, client):
    leaf_nodes = get_leaves(tree)
    node = leaf_nodes[participants.index(client.name)]
    path = [_ for _ in create_copath(node)]
    return node, path

def _update_path(path, updates):
    for prev, current in zip(path, updates):
        prev.pub = current.pub

def _leaf_secret(group_name, client, initiator, initiator_pub, setup_key):
    if initiator == client.name:
        # use creator key
        leaf_key = client.get_creator_key(group_name)
    else:
        leaf_key = keyexchange(client.get_pre_key_priv(), client.get_iden_key_priv(), initiator_pub, setup_key)
    return leaf_key

def _recompute(leaf_key, path):
    secret = create_leaf_node(leaf_key)
    recon, intermediate = reduce_path(secret, path)
    return recon.priv, intermediate

def _process_group_message(group, client, users):
    '''Function to construct group secret based on creation message'''
    name, tree, initiator, initiator_pub, participants, setup_key = _unpack(group, users)
    _, path = _path(tree, participants, client)
    leaf = _leaf_secret(name, client, initiator, initiator_pub, setup_key)
    return _recompute(leaf, path)
    #group_name = group.name.name
    #art = group.creation_message.art
    #setup_message = pickle.loads(art)
    #leaf_nodes = get_leaves(setup_message.tree)
    #node = leaf_nodes[setup_message.participants.index(client.name)]
    #user_mapping = dict([(u.name, u) for u in users])
    #path = [_ for _ in create_copath(node)]
    #if setup_message.initiator == client.name:
        # use creator key
        #leaf_key = client.get_creator_key(group_name)
    #else:
        #leaf_key = keyexchange(client.get_pre_key_priv(), client.get_iden_key_priv(), user_mapping[setup_message.initiator].iden_key_pub, setup_message.setup_key)
    #secret = create_leaf_node(leaf_key)
    #recon, intermediate = reduce_path(secret, path)
    #return recon.priv, intermediate

def process_group_message(group_name, group, client, users):
    '''Function to construct group secret based on creation message'''
    group = pickle.loads(group)
    leaf_nodes = get_leaves(group.tree)
    node = leaf_nodes[group.participants.index(client.name)]
    user_mapping = dict([(u.name, u) for u in users])
    path = [_ for _ in create_copath(node)]
    if group.initiator == client.name:
        # use creator key
        leaf_key = client.get_creator_key(group_name)
    else:
        leaf_key = keyexchange(client.get_pre_key_priv(), client.get_iden_key_priv(), user_mapping[group.initiator].iden_key_pub, group.setup_key)
    secret = create_leaf_node(leaf_key)
    recon, intermediate = reduce_path(secret, path)
    return recon.priv

def update_group_message(group_name, group, client, users):
    group = pickle.loads(group)
    leaf_nodes = get_leaves(group.tree)
    node = leaf_nodes[group.participants.index(client.name)]
    user_mapping = dict([(u.name, u) for u in users])
    path = [_ for _ in create_copath(node)]
    if group.initiator == client.name:
        # use creator key
        leaf_key = client.get_creator_key(group_name)
    else:
        leaf_key = keyexchange(client.get_pre_key_priv(), client.get_iden_key_priv(), user_mapping[group.initiator].iden_key_pub, group.setup_key)
    secret = create_leaf_node(leaf_key)
    # update public keys of parents of nodes on the copath
    updated_tree_secret = update_pub_on_path(secret, path)
    node.pub = secret.pub
    return updated_tree_secret, pickle.dumps(group)

    '''
    name, tree, initiator, initiator_pub, participants, setup_key = _unpack(group, users)
    node, path = _path(tree, participants, client)
    leaf = _leaf_secret(name, client, initiator, initiator_pub, setup_key)
    secret, intermediate = _recompute(leaf, path)
    _update_path(path, intermediate)
    node.pub = get_pub(leaf)
    return secret, create_setup_message(tree, participants, setup_key, initiator)
    '''