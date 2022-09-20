import asyncio
from email.headerregistry import Group
import logging
import random
from typing import Iterable, List
import grpc
import pickle
import pyxart_pb2_grpc
import pyxart_pb2
from cmd import Cmd
import sys
#sys.path.append('src/pyxart')
from src.pyxart.client import Client
from src.pyxart.group import create_group, process_group_message
import nacl.secret

client = Client(name=sys.argv[1])

class GroupMessaging(Cmd):
    intro = 'Welcome to the pyxart shell. Type help or ? to list commands.\n'
    prompt = '(pyxart) '
    channel = grpc.insecure_channel('localhost:50051')
    stub = pyxart_pb2_grpc.PyxartStub(channel)

    # basic pyxart commands
    def do_ping(self, arg):
        'Ping server'
        response = GroupMessaging.stub.ping(pyxart_pb2.Ping(msg=f'hi, are you alive?'))
        print("Message from server: " + response.msg)
    
    def do_register(self, arg):
        'Register client at the server by sending public keys'
        response = GroupMessaging.stub.register(pyxart_pb2.ClientRegistration(name=client.name, iden_key_pub=client.iden_key.pub, pre_key_pub=client.pre_key.pub))
        print("Message from server: " + response.msg)

    def do_get_users(self, arg):
        'Get public keys for all registered users'
        response = GroupMessaging.stub.get_users(pyxart_pb2.Empty())
        for r in response:
            print(r)
    
    def do_create_group(self, arg):
        'Create a group'
        response = GroupMessaging.stub.get_users(pyxart_pb2.Empty())
        others = []
        for r in response:
            if r.name != client.name:
                others.append(r)
        creation_message, secret, creator_key = create_group(others, client.name, client.iden_key.priv)
        creation_bytes = pickle.dumps(creation_message)
        response = GroupMessaging.stub.create_group(pyxart_pb2.GroupCreation(art=creation_bytes))
        print(response)
        client.add_to_cache(response.name, secret)
        client.add_creator_key(response.name, creator_key)
        print(f"Secret is {secret}")

    def do_get_my_groups(self, arg):
        'Get all groups'
        response = GroupMessaging.stub.get_my_groups(pyxart_pb2.ClientName(name=client.name))
        for grp in response:
            # reconstruct group secret
            print(f"Discovered group {grp.name.name}")
            secret = process_group_message(grp, client, [_ for _ in GroupMessaging.stub.get_users(pyxart_pb2.Empty())])
            print(f"Current group secret is {secret}")
            client.add_to_cache(grp.name.name, secret)
    
    def do_send_message(self, arg):
        'Send encrypted message in a group'
        grp_name = arg.split()[0]
        message = ' '.join(arg.split()[1:])
        box = nacl.secret.SecretBox(client.get_key(grp_name))
        encrypted_message = box.encrypt(message.encode())
        print(f"Sending encrypted message {encrypted_message} to group {grp_name}")
        response = GroupMessaging.stub.send_encrypted_message(pyxart_pb2.Payload(group=pyxart_pb2.GroupName(name=grp_name), msg=pyxart_pb2.Text(msg=encrypted_message)))
        print(response)

    def do_get_messages(self, arg):
        'Retrieve encrypted messages and decrypt them locally'
        grp_name = arg.split()[0]
        response = GroupMessaging.stub.retrieve_encrypted_messages(pyxart_pb2.GroupName(name=grp_name))
        encrypted_messages = [x.msg for x in response]
        print(f"Encrypted messages in the group \n {encrypted_messages}")
        box = nacl.secret.SecretBox(client.get_key(grp_name))
        for m in encrypted_messages:
            print(f"Decrypted message {box.decrypt(m).decode()}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    #asyncio.get_event_loop().run_until_complete(main(sys.argv[1]))
    #main(sys.argv[1])
    GroupMessaging().cmdloop()
