from pyxart.keys import KeyPairCurve25519
class Client:

    def __init__(self, name) -> None:
        self.name = name
        self.iden_key = KeyPairCurve25519.generate()
        self.pre_key = KeyPairCurve25519.generate()
    
    def __repr__(self) -> str:
        return f"Client{self.name}"
    
    def __str__(self) -> str:
        return f"Client name is {self.name}"