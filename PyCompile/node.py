class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []


    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, children={self.children})"