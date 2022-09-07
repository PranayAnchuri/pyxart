from pyxart.group.art_receiver import process_group_message
from pyxart.group.tree import get_leaves, to_networkx
from pyxart.client import Client
from pyxart.server import Server
from pyxart.group import create_group, create_copath


names = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "Gavin", "Homer"]
clients = [Client(names[i]) for i in range(8)]

srv = Server()
for cl in clients:
    srv.register(cl)

setup_message, secret = create_group(clients, srv)
leaf_nodes = get_leaves(setup_message.tree)
nx_tree = to_networkx(setup_message.tree)

for client, node in zip(clients[1:], leaf_nodes[1:]):
    path = [_ for _ in create_copath(node)]
    recon = process_group_message(client, srv, setup_message.initiator, setup_message.setup_key, path)
    assert recon == secret
print("done")