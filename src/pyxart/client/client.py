from keys import KeyPairCurve25519
class Client:

    def __init__(self, name) -> None:
        self.name = name
        self.iden_key = KeyPairCurve25519.generate()
        self.pre_key = KeyPairCurve25519.generate()
        self.group_keys = {}
    
    def __repr__(self) -> str:
        return f"Client{self.name}"
    
    def __str__(self) -> str:
        return f"Client name is {self.name}"
    
    def add_to_cache(self, group_name, group_secret):
        self.group_keys[group_name] = group_secret
    
    def in_cache(self, group_name):
        return group_name in self.group_keys
    
    def get_key(self, group_name):
        return self.group_keys[group_name]