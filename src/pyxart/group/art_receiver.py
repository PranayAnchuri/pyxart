from .utils import (
    keyexchange,
    reduce_path,
    create_leaf_node,
    update_pub_on_path,
)
from .tree import get_leaves
from .art import create_copath
import pickle
from ..client import Client


def process_group_message(group_name, group, client, users):
    """Create group secret from creation message and group metadata

    Args:
        group_name (str): Group name
        group (bytes): initiation message
        client (Client): client object
        users (list): list of users in the group

    Returns:
        bytes: Group secret
    """
    group = pickle.loads(group)
    leaf_nodes = get_leaves(group.tree)
    node = leaf_nodes[group.participants.index(client.name)]
    user_mapping = dict([(u.name, u) for u in users])
    path = [_ for _ in create_copath(node)]
    if group.initiator == client.name:
        # use creator key
        leaf_key = client.get_creator_key(group_name)
    else:
        leaf_key = keyexchange(
            client.get_pre_key_priv(),
            client.get_iden_key_priv(),
            user_mapping[group.initiator].iden_key_pub,
            group.setup_key,
        )
    secret = create_leaf_node(leaf_key)
    recon, _ = reduce_path(secret, path)
    return recon.priv


def update_group_message(group_name, group, client, users):
    """Create group's update message when user keys are updated

    Args:
        group_name (str): Group name
        group (bytes): serialized group state
        client (Client): client object performing the update
        users (list): list of users in the group

    Returns:
        tuple: tuple.1 = updated secret; tuple.2 = updated group state
    """
    group = pickle.loads(group)
    leaf_nodes = get_leaves(group.tree)
    node = leaf_nodes[group.participants.index(client.name)]
    user_mapping = dict([(u.name, u) for u in users])
    path = [_ for _ in create_copath(node)]
    if group.initiator == client.name:
        # use creator key
        leaf_key = client.get_creator_key(group_name)
    else:
        leaf_key = keyexchange(
            client.get_pre_key_priv(),
            client.get_iden_key_priv(),
            user_mapping[group.initiator].iden_key_pub,
            group.setup_key,
        )
    secret = create_leaf_node(leaf_key)
    # update public keys of parents of nodes on the copath
    updated_tree_secret = update_pub_on_path(secret, path)
    node.pub = secret.pub
    return updated_tree_secret, pickle.dumps(group)
