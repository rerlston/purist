import json

from typing import Any, Dict, List

class Node():
    """
    Abstract Syntax Tree Node
    """

    def __init__(self, node_name: str, value: str | int | float | None = None) -> None:
        self._node_name = node_name
        self._value = value
        self._children: 'List[Node]|None' = None

    @property
    def children(self) -> 'List[Node]|None':
        """
        Returns the children of the node
        """
        return self._children

    def add_child(self, node: 'Node|None') -> None:
        """
        Adds a child to the parent (current) node
        Args:
            node: the node to add as a child
        """
        if node is not None:
            if self._children is None:
                self._children = []
            self._children.append(node)

    @property
    def value(self) -> str | int | float | None:
        """
        Returns the value of the node

        Returns:
            str|int|float|None: the value of the node
        """
        return self._value

    @value.setter
    def value(self, value: str | int | float) -> None:
        self._value = value

    def __repr__(self) -> str:
        response: Dict[str, Any] = {}
        response['type'] = self._node_name
        if self._value is not None:
            response['value'] = self._value
        if self._children is not None:
            children: List[Dict[str, Any]] = []
            for child in self._children:
                children.append(json.loads(child.__repr__()))
            response['children'] = children
        return json.dumps(response, indent=4)
