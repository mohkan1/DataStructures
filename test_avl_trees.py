class Node:
    def __init__(self, item, left, right):
        self.item = item
        self.left = left
        self.right = right
        self.height = 1 + max(node_height(left), node_height(right))
    
    def set_left(self,left):
        self.left = left
        self.height = 1 + max(node_height(left), node_height(self.right))
          
    def set_right(self,right):
        self.right = right
        self.height = 1 + max(node_height(self.left), node_height(right))
    

def node_height(node: Node):
    return node.height if node is None else None

def height_diff(node: Node):
    return node.height(node.left) - node.height(node.right)


class AVL:
    _root: Node

    def contains(self, item):
        return self._contains(self._root, item)

    def _contains(self, node: Node, item):
        while node is not None:
            if item < node.item:
                node = node.left
            elif item > node.item:
                node = node.right
            else:
                return True
        return False

    def add(self, item):
        self._root = self._add(self._root, item)

    def _add(self, node: Node, item):
        if node is None:
            return Node(item, None, None)
        elif item < node.item:
            node.set_left(self._add(node.left, item))
        
