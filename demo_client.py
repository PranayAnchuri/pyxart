import asyncio
from email.headerregistry import Group
import logging
import random
from typing import Iterable, List
import grpc
import pickle
import pyxart_pb2_grpc
import pyxart_pb2
from cmd2 import Cmd
import sys
#sys.path.append('src/pyxart')
from src.pyxart.client import Client
from src.pyxart.group import create_group, process_group_message, update_group_message
import nacl.secret
from rich import print
from rich.console import Console

client = Client(name=sys.argv[1].casefold())
console = Console()


def print_server_message(msg):
    print(f'[bold uu green] :closed_mailbox_with_lowered_flag: {msg}')


def print_local_message(msg):
    print(f'[italic frame blue] :rolled-up_newspaper: {msg}')


class GroupMessaging(Cmd):
    intro = 'Welcome to the pyxart shell. Type help or ? to list commands.\n'
    prompt = '(pyxart) '
    channel = grpc.insecure_channel('localhost:50051')
    stub = pyxart_pb2_grpc.PyxartStub(channel)

    def __init__(self):
        Cmd.__init__(self, allow_cli_args=False, include_py=True, include_ipy=True)

    # basic pyxart commands
    def do_ping(self, arg):
        'Ping server'
        response = GroupMessaging.stub.ping(
            pyxart_pb2.Ping(msg=f'hi, are you alive?'))
        print_server_message(response.msg)

    def do_register(self, arg):
        'Register client at the server by sending public keys'
        response = GroupMessaging.stub.register(
            pyxart_pb2.ClientRegistration(
                name=client.name,
                iden_key_pub=client.get_iden_key_pub(),
                pre_key_pub=client.get_pre_key_pub()))
        print_server_message(response.msg)

    def do_clear_db(self, arg):
        '''Clear stored keys'''
        client.shelf.clear()

    def do_get_users(self, arg):
        'Get public keys for all registered users'
        response = GroupMessaging.stub.get_users(pyxart_pb2.Empty())
        for r in response:
            print_local_message(r)

    def do_create_group(self, arg):
        'Create a group with all users (default) or specified list of users'
        response = GroupMessaging.stub.get_users(pyxart_pb2.Empty())
        others = []
        # get case insensitive users
        members = [x.casefold() for x in arg.split()] if len(arg) > 0 else None
        for r in response:
            if r.name != client.name and (members is None
                                          or r.name.casefold() in members):
                others.append(r)
        creation_message, secret, creator_key = create_group(
            others, client.name, client.get_iden_key_priv())
        creation_bytes = pickle.dumps(creation_message)
        response = GroupMessaging.stub.create_group(
            pyxart_pb2.GroupCreation(art=creation_bytes))
        print_server_message(response)
        client.add_to_cache(response.name, secret)
        client.add_creator_key(response.name, creator_key)

    def do_get_my_groups(self, arg):
        'Get all groups'
        response = GroupMessaging.stub.get_my_groups(
            pyxart_pb2.ClientName(name=client.name))
        for grp in response:
            # reconstruct group secret
            print_local_message(f"Discovered group {grp.name.name}")
            secret = process_group_message(
                grp.name.name, grp.creation_message.art, client,
                [_ for _ in GroupMessaging.stub.get_users(pyxart_pb2.Empty())])
            #print_local_message(f"{grp.name.name} secret is {secret}")
            client.add_to_cache(grp.name.name, secret)

    def do_update(self, arg):
        '''Update client keys and correspondingly leaf nodes in groups'''
        client.update_keys()
        self.do_register(arg)
        response = GroupMessaging.stub.get_my_groups(
            pyxart_pb2.ClientName(name=client.name))
        for grp in response:
            print_local_message(f"Updating key in {grp.name.name}")
            # update tree
            secret, updated_creation_bytes = update_group_message(
                grp.name.name, grp.creation_message.art, client,
                [_ for _ in GroupMessaging.stub.get_users(pyxart_pb2.Empty())])
            # update my key
            client.add_to_cache(grp.name.name, secret)
            # send updates to server
            response = GroupMessaging.stub.update_group(
                pyxart_pb2.GroupInfo(
                    name=pyxart_pb2.GroupName(name=grp.name.name),
                    creation_message=pyxart_pb2.GroupCreation(
                        art=updated_creation_bytes)))
            print(response)

    def do_send_message(self, arg):
        'Send encrypted message in a group'
        grp_name = arg.split()[0]
        message = ' '.join(arg.split()[1:])
        box = nacl.secret.SecretBox(client.get_key(grp_name))
        encrypted_message = box.encrypt(message.encode())
        print_local_message(
            f"Sending encrypted message \n :locked_with_key: {encrypted_message} \n to group {grp_name}"
        )
        response = GroupMessaging.stub.send_encrypted_message(
            pyxart_pb2.Payload(group=pyxart_pb2.GroupName(name=grp_name),
                               msg=pyxart_pb2.Text(msg=encrypted_message)))
        print_server_message(response)

    def do_get_messages(self, arg):
        'Retrieve encrypted messages and decrypt them locally'
        grp_name = arg.split()[0]
        response = GroupMessaging.stub.retrieve_encrypted_messages(
            pyxart_pb2.GroupName(name=grp_name))
        encrypted_messages = [x.msg for x in response]
        print_server_message(encrypted_messages)
        try:
            box = nacl.secret.SecretBox(client.get_key(grp_name))
            for m in encrypted_messages:
                try:
                    print_local_message(
                        f"Decrypted message :unlocked: {box.decrypt(m).decode()}")
                except:
                    print_local_message(f"Can't decrypt message {m} with key {client.get_key(grp_name)}")
        except:
            print_local_message(f"I don't have a key for the group {grp_name}")

    def do_impersonate(self, arg):
        '''Impersonate other user by chaning name'''
        client.name = arg


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    #asyncio.get_event_loop().run_until_complete(main(sys.argv[1]))
    #main(sys.argv[1])
    GroupMessaging().cmdloop()
