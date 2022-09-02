from .utils import keyexchange, reduce_path, create_leaf_node

# functions on the receiver end

def process_group_message(client, server, initiator_name, setup_key_pub, copath):
    # construct shared secret
    initiator = server.getBundle(initiator_name)
    #leaf_key = keyexchange(setup_key.priv, creator.iden_key.priv, bundle.iden_key.pub, bundle.pre_key.pub)
    leaf_key = keyexchange(client.pre_key.priv, client.iden_key.priv, initiator.iden_key.pub, setup_key_pub)
    secret = create_leaf_node(leaf_key)
    recon = reduce_path(secret, copath)
    return recon.priv