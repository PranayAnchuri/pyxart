from operator import itruediv
from src.pyxart.group.art_receiver import process_group_message, update_group_message
from src.pyxart.group.tree import get_leaves
from src.pyxart.client import Client
from src.pyxart.server import Server
from src.pyxart.group import create_group, create_copath
from collections import namedtuple
import pickle


User = namedtuple("User", "name iden_key_pub pre_key_pub")

names = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "Gavin", "Homer"]
clients = [Client(names[i]) for i in range(8)]
users = []
group_name = "DemoGroup"


def update_client(client):
    client.update_keys()
    cl.iden_key_pub = cl.get_iden_key_pub()
    cl.pre_key_pub = cl.get_pre_key_pub()
    users.append(User(cl.name, cl.get_iden_key_pub(), cl.get_pre_key_pub()))


srv = Server()
for cl in clients:
    srv.register(cl, cl.get_iden_key_pub(), cl.get_pre_key_pub())
    # for compatibility with grpc
    cl.iden_key_pub = cl.get_iden_key_pub()
    cl.pre_key_pub = cl.get_pre_key_pub()
    users.append(User(cl.name, cl.get_iden_key_pub(), cl.get_pre_key_pub()))

setup_message, secret, creator_key = create_group(
    clients[1:], names[0], clients[0].get_iden_key_priv()
)
clients[0].add_creator_key(group_name, creator_key)

leaf_nodes = get_leaves(setup_message.tree)

for client, node in zip(clients[1:], leaf_nodes[1:]):
    path = [_ for _ in create_copath(node)]
    recon = process_group_message(
        group_name, pickle.dumps(setup_message), client, users
    )
    assert recon == secret
print("done1")

update_client(clients[1])
updated_tree_secret, updated_tree_state = update_group_message(
    group_name, pickle.dumps(setup_message), clients[1], users
)

for client, node in zip(clients[2:], leaf_nodes[2:]):
    path = [_ for _ in create_copath(node)]
    # recon = process_group_message(client, srv, setup_message.initiator, setup_message.setup_key, path)
    recon = update_group_message(group_name, updated_tree_state, client, users)
    # recon = process_group_message(
    # group_name, pickle.dumps(setup_message), client, users
    # )
    # assert recon == updated_tree_secret
print("done")
