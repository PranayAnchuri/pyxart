import pytest
from src.pyxart.client import Client
from src.pyxart.group.art_receiver import process_group_message, update_group_message
from src.pyxart.group.tree import get_leaves
from src.pyxart.client import Client
from src.pyxart.server import Server
from src.pyxart.group import create_group, create_copath
from collections import namedtuple
import pickle
import uuid

User = namedtuple("User", "name iden_key_pub pre_key_pub")


@pytest.fixture
def groupname():
    return uuid.uuid4()


@pytest.fixture
def names():
    return ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "Gavin", "Homer"]


@pytest.fixture
def clients(names):
    return [Client(names[i]) for i in range(len(names))]


@pytest.fixture
def server():
    return Server()


@pytest.fixture
def users(clients, server):
    u = []
    for cl in clients:
        server.register(cl, cl.get_iden_key_pub(), cl.get_pre_key_pub())
        # for compatibility with grpc
        cl.iden_key_pub = cl.get_iden_key_pub()
        cl.pre_key_pub = cl.get_pre_key_pub()
        u.append(User(cl.name, cl.get_iden_key_pub(), cl.get_pre_key_pub()))
    return u


@pytest.fixture
def group_setup(users, clients, names):
    setup_message, secret, creator_key = create_group(
        clients[1:], names[0], clients[0].get_iden_key_priv()
    )
    return setup_message, secret, creator_key


def test_create(users, clients, groupname, group_setup):
    """Check that the creator and members compute the same shared secret"""

    setup_message, secret, creator_key = group_setup
    clients[0].add_creator_key(groupname, creator_key)

    leaf_nodes = get_leaves(setup_message.tree)

    for client, node in zip(clients[1:], leaf_nodes[1:]):
        path = [_ for _ in create_copath(node)]
        recon = process_group_message(
            groupname, pickle.dumps(setup_message), client, users
        )
        assert recon == secret


def update_client(client):
    client.update_keys()


@pytest.fixture
def update(users, clients, groupname, group_setup):
    update_client(clients[1])
    setup_message, secret, creator_key = group_setup
    updated_tree_secret, updated_tree_state = update_group_message(
        groupname, pickle.dumps(setup_message), clients[1], users
    )
    return updated_tree_secret, updated_tree_state


def test_update(update, clients, groupname, users):
    updated_tree_secret, updated_tree_state = update
    leaf_nodes = get_leaves(pickle.loads(updated_tree_state).tree)
    for client, node in zip(clients[2:], leaf_nodes[2:]):
        path = [_ for _ in create_copath(node)]
        # recon = process_group_message(client, srv, setup_message.initiator, setup_message.setup_key, path)
        recon = update_group_message(groupname, updated_tree_state, client, users)
        assert recon[0] == updated_tree_secret
