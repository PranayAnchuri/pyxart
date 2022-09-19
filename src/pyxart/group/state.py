from .art import GroupSetupMessage

class GroupState:

    def __init__(self, name: str, setup_message : GroupSetupMessage) -> None:
        self.tree = setup_message.tree
        self.myname = name
