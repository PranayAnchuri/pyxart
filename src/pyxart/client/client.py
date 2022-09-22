from ..keys import KeyPairCurve25519
import os
import shelve
import atexit


class Client:

    def __init__(self, name) -> None:
        self.name = name
        self.shelf = shelve.open(f'{name}', writeback=True)
        self.props = ['iden_key', 'pre_key', 'group_keys', 'group_creator_keys']
        if 'iden_key' not in self.shelf:
            self.shelf['iden_key'] = KeyPairCurve25519.generate()
        if 'pre_key' not in self.shelf:
            self.shelf['pre_key'] = KeyPairCurve25519.generate()
        if 'group_keys' not in self.shelf:
            self.shelf['group_keys'] = {}
        if 'group_creator_keys' not in self.shelf:
            self.shelf['group_creator_keys'] = {}
        atexit.register(self.cleanup)
    
    def __repr__(self) -> str:
        return f"Client{self.name}"
    
    def __str__(self) -> str:
        return f"Client name is {self.name}"
    
    def update_keys(self):
            self.shelf['iden_key'] = KeyPairCurve25519.generate()
            self.shelf['pre_key'] = KeyPairCurve25519.generate()

    def cleanup(self):
        print("Running cleanup")
        self.shelf.close()
    
    def add_creator_key(self, group_name, creator_key):
        self.shelf["group_creator_keys"][group_name] = creator_key
    
    def get_creator_key(self, group_name):
        return self.shelf["group_creator_keys"][group_name]

    def add_to_cache(self, group_name, group_secret):
        self.shelf["group_keys"][group_name] = group_secret
    
    def in_cache(self, group_name):
        return group_name in self.shelf["group_keys"]
    
    def get_key(self, group_name):
        return self.shelf["group_keys"][group_name]
    
    def get_iden_key_pub(self):
        return self.shelf["iden_key"].pub

    def get_iden_key_priv(self):
        return self.shelf["iden_key"].priv

    def get_pre_key_pub(self):
        return self.shelf["pre_key"].pub

    def get_pre_key_priv(self):
        return self.shelf["pre_key"].priv