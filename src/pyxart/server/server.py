from pyxart.client import Client
from collections import namedtuple

Bundle = namedtuple('Bundle', 'iden_key pre_key')
class Server:

    def __init__(self) -> None:
        self.clients = {}
    
    def register(self, client):
        self.clients[client.name] = client
    
    def getBundle(self, client_name):
        client = self.clients[client_name]
        return Bundle(client.iden_key, client.pre_key)