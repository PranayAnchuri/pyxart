import sys
sys.path.append('./src/pyxart')
from group.art_receiver import process_group_message
from group.tree import get_leaves, to_networkx
from client import Client
from server import Server
from group import create_group, create_copath, plot


names = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "Gavin", "Homer"]
clients = [Client(names[i]) for i in range(8)]

srv = Server()
for cl in clients:
    srv.register(cl)

setup_message, secret = create_group(clients, srv)
leaf_nodes = get_leaves(setup_message.tree)
nx_tree = to_networkx(setup_message.tree)
#nx.nx_agraph.write_dot(G,'test.dot')
plot(nx_tree, f'Proof tree generated by {names[0]}', 'proof_tree')
participants = setup_message.participants

for client, node in zip(clients[1:], leaf_nodes[1:]):
    path = [_ for _ in create_copath(node)]
    recon = process_group_message(client, srv, setup_message.initiator, setup_message.setup_key, path)
    assert recon == secret
print("done")