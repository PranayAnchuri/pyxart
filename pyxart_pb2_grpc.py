# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import pyxart_pb2 as pyxart__pb2


class PyxartStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ping = channel.unary_unary(
                '/Pyxart/ping',
                request_serializer=pyxart__pb2.Ping.SerializeToString,
                response_deserializer=pyxart__pb2.Pong.FromString,
                )
        self.register = channel.unary_unary(
                '/Pyxart/register',
                request_serializer=pyxart__pb2.ClientRegistration.SerializeToString,
                response_deserializer=pyxart__pb2.Pong.FromString,
                )
        self.get_users = channel.unary_stream(
                '/Pyxart/get_users',
                request_serializer=pyxart__pb2.Empty.SerializeToString,
                response_deserializer=pyxart__pb2.ClientRegistration.FromString,
                )
        self.get_my_groups = channel.unary_stream(
                '/Pyxart/get_my_groups',
                request_serializer=pyxart__pb2.ClientName.SerializeToString,
                response_deserializer=pyxart__pb2.GroupInfo.FromString,
                )
        self.create_group = channel.unary_unary(
                '/Pyxart/create_group',
                request_serializer=pyxart__pb2.GroupCreation.SerializeToString,
                response_deserializer=pyxart__pb2.GroupName.FromString,
                )
        self.update_group = channel.unary_unary(
                '/Pyxart/update_group',
                request_serializer=pyxart__pb2.GroupInfo.SerializeToString,
                response_deserializer=pyxart__pb2.GroupName.FromString,
                )
        self.send_encrypted_message = channel.unary_unary(
                '/Pyxart/send_encrypted_message',
                request_serializer=pyxart__pb2.Payload.SerializeToString,
                response_deserializer=pyxart__pb2.Pong.FromString,
                )
        self.retrieve_encrypted_messages = channel.unary_stream(
                '/Pyxart/retrieve_encrypted_messages',
                request_serializer=pyxart__pb2.GroupName.SerializeToString,
                response_deserializer=pyxart__pb2.Text.FromString,
                )


class PyxartServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ping(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_users(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_my_groups(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def create_group(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_group(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def send_encrypted_message(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def retrieve_encrypted_messages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PyxartServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ping': grpc.unary_unary_rpc_method_handler(
                    servicer.ping,
                    request_deserializer=pyxart__pb2.Ping.FromString,
                    response_serializer=pyxart__pb2.Pong.SerializeToString,
            ),
            'register': grpc.unary_unary_rpc_method_handler(
                    servicer.register,
                    request_deserializer=pyxart__pb2.ClientRegistration.FromString,
                    response_serializer=pyxart__pb2.Pong.SerializeToString,
            ),
            'get_users': grpc.unary_stream_rpc_method_handler(
                    servicer.get_users,
                    request_deserializer=pyxart__pb2.Empty.FromString,
                    response_serializer=pyxart__pb2.ClientRegistration.SerializeToString,
            ),
            'get_my_groups': grpc.unary_stream_rpc_method_handler(
                    servicer.get_my_groups,
                    request_deserializer=pyxart__pb2.ClientName.FromString,
                    response_serializer=pyxart__pb2.GroupInfo.SerializeToString,
            ),
            'create_group': grpc.unary_unary_rpc_method_handler(
                    servicer.create_group,
                    request_deserializer=pyxart__pb2.GroupCreation.FromString,
                    response_serializer=pyxart__pb2.GroupName.SerializeToString,
            ),
            'update_group': grpc.unary_unary_rpc_method_handler(
                    servicer.update_group,
                    request_deserializer=pyxart__pb2.GroupInfo.FromString,
                    response_serializer=pyxart__pb2.GroupName.SerializeToString,
            ),
            'send_encrypted_message': grpc.unary_unary_rpc_method_handler(
                    servicer.send_encrypted_message,
                    request_deserializer=pyxart__pb2.Payload.FromString,
                    response_serializer=pyxart__pb2.Pong.SerializeToString,
            ),
            'retrieve_encrypted_messages': grpc.unary_stream_rpc_method_handler(
                    servicer.retrieve_encrypted_messages,
                    request_deserializer=pyxart__pb2.GroupName.FromString,
                    response_serializer=pyxart__pb2.Text.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Pyxart', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Pyxart(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Pyxart/ping',
            pyxart__pb2.Ping.SerializeToString,
            pyxart__pb2.Pong.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Pyxart/register',
            pyxart__pb2.ClientRegistration.SerializeToString,
            pyxart__pb2.Pong.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_users(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Pyxart/get_users',
            pyxart__pb2.Empty.SerializeToString,
            pyxart__pb2.ClientRegistration.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_my_groups(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Pyxart/get_my_groups',
            pyxart__pb2.ClientName.SerializeToString,
            pyxart__pb2.GroupInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def create_group(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Pyxart/create_group',
            pyxart__pb2.GroupCreation.SerializeToString,
            pyxart__pb2.GroupName.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update_group(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Pyxart/update_group',
            pyxart__pb2.GroupInfo.SerializeToString,
            pyxart__pb2.GroupName.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def send_encrypted_message(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Pyxart/send_encrypted_message',
            pyxart__pb2.Payload.SerializeToString,
            pyxart__pb2.Pong.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def retrieve_encrypted_messages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Pyxart/retrieve_encrypted_messages',
            pyxart__pb2.GroupName.SerializeToString,
            pyxart__pb2.Text.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
