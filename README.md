# pyxart
Python implementation of Asynchronous Ratchet Trees

# Setup

## Install (conda + pip)

```
conda create --name <venv name> python=3.10
pip install .
```
## gRPC and protobuf

```
python -m grpc_tools.protoc -I src/pyxart/protobuf --python_out=. --grpc_python_out=. src/pyxart/protobuf/*
```

## start server

```
python demo_server.py
```

## start client

```
python demo_client.py <client_name>
```

## Orchestration

Create four shells A, B, C, and D

In A,
```
python demo_server.py Alice
register
```

In B

```
python demo_client.py Bob
register
```

In C

```
python demo_client.py Charlie
register
```

In D
```
python demo_client.py Dave
register
```

In B


```
create_group charlie dave
```

In C, D

```
get_my_groups
```

In B

```
send_message <group_name_from_previous_output> <plain text message>
```
In C, D

```
get_messages <group_name>
```

# Demo

The following screenshot shows a demo of a grpc server and four clients.

![](https://github.com/PranayAnchuri/pyxart/blob/main/demo.gif)



# references

- https://research.facebook.com/publications/on-ends-to-ends-encryption-asynchronous-group-messaging-with-strong-security-guarantees/
