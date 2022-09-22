from ..client import Client
from collections import namedtuple, defaultdict
import pickle
import uuid

Bundle = namedtuple('Bundle', 'iden_key_pub pre_key_pub')
Group = namedtuple('Group', 'members creation_message nonce')


class Server:

    def __init__(self) -> None:
        self.clients = {}
        self.groups = {}
        self.messages = defaultdict(list)

    def register(self, name, iden_key_pub, pre_key_pub):
        self.clients[name] = Bundle(iden_key_pub, pre_key_pub)

    def get_bundle(self, client_name):
        return self.clients[client_name]
    
    def register_group(self, creation_message):
        grp = pickle.loads(creation_message)
        grp_key = str(uuid.uuid4())
        #self.groups.append(Group(grp.participants, creation_message))
        self.groups[grp_key] = Group(grp.participants, creation_message, 0)
        return grp_key, grp.participants

    def update_group(self, grp_key, creation_message):
        self.groups[grp_key] = Group(self.groups[grp_key].members, creation_message, self.groups[grp_key].nonce+1)
    
    def get_groups(self, client_name):
        """ Return creation messages for all groups a member is part of"""
        for grp_key, grp in self.groups.items():
            if client_name in grp.members:
                yield grp_key, grp.creation_message
    
    def store_message(self, group_key, message):
        if group_key in self.groups:
            self.messages[group_key].append(message)

    def get_messages(self, group_key):
        if group_key in self.groups:
            return self.messages[group_key]

