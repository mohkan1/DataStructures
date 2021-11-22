import random

class Node:
    def __init__(self, item, left, right):
        self.item = item
        self.left = left
        self.right = right
        self.height = 1 + max(node_height(left), node_height(right))

    def set_left(self, left):
        self.left = left
        self.height = 1 + max(node_height(self.left), node_height(self.right))

    def set_right(self, right):
        self.right = right
        self.height = 1 + max(node_height(self.left), node_height(self.right))

    def __str__(self):
        result = "Node(item=%s, height=%d" % (self.item, self.height)
        if self.left is not None:
            result += ", left=%s" % self.left
        if self.right is not None:
            result += ", right=%s" % self.right
        result += ")"
        return result

    def __repr__(self):
        return str(self)

def node_height(node: Node):
    if node is None:
        return 0
    else:
        return node.height

def height_diff(node: Node):
    return node_height(node.left) - node_height(node.right)

class AVL:
    _root: Node

    def _rotateLeft(self, node: Node) -> Node:
        x = node
        y = x.right
        B = y.left

        x.set_right(B)
        y.set_left(x)
        return y

    def _rotateRight(self, node: Node) -> Node:
        y = node
        x = y.left
        B = x.right

        y.set_left(B)
        x.set_right(y)
        return x

    def _balance(self, node: Node) -> Node:
        # height difference -2,-1,0,1,2

        heightDiff = height_diff(node)

        if heightDiff == 2:
            # Left-left or left-right case
            leftDiff = height_diff(node.left)

            if leftDiff <= 0:
                # Left-right case
                node.set_left(self._rotateLeft(node.left))

            node = self._rotateRight(node)
        elif heightDiff == -2:
            # Right-left or right-right case
            rightDiff = height_diff(node.right)

            if rightDiff >= 0:
                # Right-left case
                node.set_right(self._rotateRight(node.right))

            node = self._rotateLeft(node)

        return node

    def __init__(self):
        """Creates an empty set."""

        self._root = None

    def contains(self, item):
        """Returns true if the item is present in the set."""

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
        """Adds an item to the set."""

        self._root = self._add(self._root, item)

    def _add(self, node: Node, item):
        """Helper function for _add."""

        if node is None:
            return Node(item, None, None)
        elif item < node.item:
            node.set_left(self._add(node.left, item))
        elif item > node.item:
            node.set_right(self._add(node.right, item))
        else:
            # The item is already present
            pass

        return self._balance(node)

    def __iter__(self):
        """Iterates through all items in the set, in ascending order."""

        # Here is one way to solve this problem.
        # We use an in-order traveral to add all items to a list, then
        # iterate through the list.
        items = []
        self._append_items(self._root, items)
        return iter(items)

    def _append_items(self, node: Node, items: list):
        """Does an in-order traversal of 'node', adding all items in it
        to the 'items' list."""

        if node is None:
            return None
        else:
            self._append_items(node.left, items)
            items.append(node.item)
            self._append_items(node.right, items)

    def check(self):
        """Check that the tree is a valid AVL tree."""
        
        if not self._isWellTyped(self._root):
            raise AssertionError("A field of a node has the wrong type", self._root)
        if not self._isBST(self._root):
            raise AssertionError("Keys are not in the correct BST order", self._root)
        if not self._heightsOK(self._root):
            raise AssertionError("Height field is wrong", self._root)
        if not self._isAVL(self._root):
            raise AssertionError("Tree is unbalanced", self._root)

    def _isWellTyped(self, node: Node) -> bool:
        """Checks that the types are correct."""

        if node is None:
            return True
        if not isinstance(node, Node):
            return False
        return self._isWellTyped(node.left) and self._isWellTyped(node.right)

    def _isBST(self, node: Node, lo=None, hi=None) -> bool:
        """Returns true if the tree is a valid BST.

        If lo is not None, also checks that all items are > lo.
        If hi is not None, also checks that all items are < hi."""

        if node is None:
            return True
        if lo is not None and node.item <= lo:
            return False
        if hi is not None and node.item >= hi:
            return False
        return self._isBST(node.left, lo, node.item) and \
               self._isBST(node.right, node.item, hi)
    
    def _heightsOK(self, node: Node) -> bool:
        if node is None: return True
        left_height = 0 if node.left is None else node.left.height
        right_height = 0 if node.right is None else node.right.height
        if node.height != 1 + max(left_height, right_height): return False
        return self._heightsOK(node.left) and self._heightsOK(node.right)

    def _isAVL(self, node: Node):
        if node is None: return True
        left_height = 0 if node.left is None else node.left.height
        right_height = 0 if node.right is None else node.right.height
        if left_height - right_height <= -2: return False
        if left_height - right_height >= 2: return False
        return self._isAVL(node.left) and self._isAVL(node.right)

    # Functions that allow the BST to be used like a Python dict

    def __contains__(self, item):
        """This is called when the user writes 'item in bst'."""

        return self.contains(item)

    def __str__(self):
        """This is called to show the BST as a string."""

        return str([item for item in self])

    def __repr__(self):
        """This is called to show the BST as a string."""

        return repr([item for item in self])

# Some code to check that the AVL tree is working
if __name__ == '__main__':
    bst = AVL()
    items = list(range(100))
    #random.shuffle(items)

    for item in items:
        print("inserting", item)
        bst.add(item)
        bst.check()
    for item in items:
        assert item in bst
    print("final bst contains", bst)
    print("final bst is", bst._root)
