from ..client import Client
from collections import namedtuple, defaultdict
import pickle
import uuid

Bundle = namedtuple("Bundle", "iden_key_pub pre_key_pub")
Group = namedtuple("Group", "members creation_message nonce")


class Server:
    def __init__(self) -> None:
        self.clients = {}
        self.groups = {}
        self.messages = defaultdict(list)

    def register(self, name, iden_key_pub, pre_key_pub):
        """Registers users public keys

        Args:
            name (str): User name
            iden_key_pub (bytes): Identity public key
            pre_key_pub (bytes): User's pre key
        """
        self.clients[name] = Bundle(iden_key_pub, pre_key_pub)

    def get_bundle(self, client_name):
        """Get user's key bundle

        Args:
            client_name (str): username

        Returns:
            Bundle: User's key bundle
        """
        return self.clients[client_name]

    def register_group(self, creation_message):
        """Register a group chat

        Args:
            creation_message (bytes): Serialized creation message

        Returns:
            tuple: tuple.1 = group id, tuple.2 = group participants
        """
        grp = pickle.loads(creation_message)
        grp_key = str(uuid.uuid4())
        # self.groups.append(Group(grp.participants, creation_message))
        self.groups[grp_key] = Group(grp.participants, creation_message, 0)
        return grp_key, grp.participants

    def update_group(self, grp_key, creation_message):
        """Update group tree

        Args:
            grp_key (str): Group id
            creation_message (bytes): Updated group state
        """
        self.groups[grp_key] = Group(
            self.groups[grp_key].members,
            creation_message,
            self.groups[grp_key].nonce + 1,
        )

    def get_groups(self, client_name):
        """Return creation messages for all groups a member is part of"""
        for grp_key, grp in self.groups.items():
            if client_name in grp.members:
                yield grp_key, grp.creation_message

    def store_message(self, group_key, message):
        """Store an encrypted message in a group"""
        if group_key in self.groups:
            self.messages[group_key].append(message)

    def get_messages(self, group_key):
        """Retrieve encrypted payloads"""
        if group_key in self.groups:
            return self.messages[group_key]
