import pyxart_pb2_grpc
import pyxart_pb2
#import sys
#sys.path.append('src/pyxart')
from src.pyxart.server import Server


class PyxartServicer(pyxart_pb2_grpc.PyxartServicer):

    def __init__(self) -> None:
        super().__init__()
        self.server = Server()

    def ping(self, request, context):
        return pyxart_pb2.Pong(msg=f"Received ping {request.msg}")

    def register(self, request, context):
        self.server.register(request.name, request.iden_key_pub, request.pre_key_pub)
        return pyxart_pb2.Pong(msg=f"Received register request {request.iden_key_pub}")

    def get_users(self, request, context):
        for name, bundle in self.server.clients.items():
            yield pyxart_pb2.ClientRegistration(name=name, iden_key_pub=bundle.iden_key_pub, pre_key_pub=bundle.pre_key_pub)
    
    def create_group(self, request, context):
        # GroupSetupMessage(creator_name, [p.name for p in members], setup_key.pub, create_proof_tree(tree))
        grp_key, members = self.server.register_group(request.art)
        return pyxart_pb2.GroupName(name=grp_key)

    def get_my_groups(self, request, context):
        for group_key, creation_message in self.server.get_groups(request.name):
            yield pyxart_pb2.GroupInfo(name=pyxart_pb2.GroupName(name=group_key), creation_message=pyxart_pb2.GroupCreation(art=creation_message))
    
    def send_encrypted_message(self, request, context):
        self.server.store_message(request.group.name, request.msg.msg)
        return pyxart_pb2.Pong(msg="Stored message")
    
    def retrieve_encrypted_messages(self, request, context):
        for msg in self.server.get_messages(request.name):
            yield pyxart_pb2.Text(msg=msg)
