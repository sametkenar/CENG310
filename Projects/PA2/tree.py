from collections import deque


class Tree:
    """Abstract base class representing a tree structure."""

    # ------------------------------- nested Position class -------------------------------
    class Position:
        """An abstraction representing the location of a single element."""

        def element(self):
            """Return the element stored at this Position."""
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            """Return True if other Position represents the same location."""
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other):
            """Return True if other does not represent the same location."""
            return not (self == other)  # opposite of eq

    # ---------- abstract methods that concrete subclass must support ----------
    def root(self):
        """Return Position representing the tree s root (or None if empty)."""
        raise NotImplementedError('must be implemented by subclass')

    def parent(self, p):
        """Return Position representing p s parent (or None if p is root)."""
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """Return the number of children that Position p has."""
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p):
        """Generate an iteration of Positions representing p s children."""
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """Return the total number of elements in the tree."""
        raise NotImplementedError('must be implemented by subclass')

    # ---------- concrete methods implemented in this class ----------
    def is_root(self, p):
        """Return True if Position p represents the root of the tree."""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if Position p does not have any children."""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0

    def depth(self, p):
        """Return the number of levels separating Position p from the root."""
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def _height2(self, p):  # time is linear in size of subtree
        """Return the height of the subtree rooted at Position p."""
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height2(c) for c in self.children(p))

    def height(self, p=None):
        """ Return the height of the subtree rooted at Position p.
            If p is None, return the height of the entire tree.
        """
        if p is None:
            p = self.root()
        return self._height2(p)  # start height2 recursion


class BinaryTree(Tree):
    """Abstract base class representing a binary tree structure."""

    # --------------------- additional abstract methods ---------------------
    def left(self, p):
        """Return a Position representing p's left child.

        Return None if p does not have a left child.
        """
        raise NotImplementedError("Must be implemented by subclass")

    def right(self, p):
        """Return a Position representing p's right child.

        Return None if p does not have a right child.
        """
        raise NotImplementedError("Must be implemented by subclass")

    # ---------- concrete methods implemented in this class ----------
    def sibling(self, p):
        """Return a Position representing p's sibling (or None if no sibling)."""
        parent = self.parent(p)
        if parent is None:  # p must be the root
            return None  # root has no sibling
        else:
            if p == self.left(parent):
                return self.right(parent)  # possibly None
            else:
                return self.left(parent)  # possibly None

    def children(self, p):
        """Generate an iteration of Positions representing p's children."""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)


class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure."""

    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

    def _validate(self, p):
        """Return associated node, if the position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError("p must be a proper Position type")
        if p._container is not self:
            raise ValueError("p does not belong to this container")
        if p._node._parent is p._node:  # convention for deprecated nodes
            raise ValueError("p is no longer valid")
        return p._node

    def _make_position(self, node):
        """Return Position instance for the given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None

    # -------------------------- binary tree constructor --------------------------

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    # -------------------------- public accessors --------------------------
    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def root(self):
        """Return the root Position of the tree (or None if the tree is empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return the Position of p's parent (or None if p is the root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        """Return the Position of p's left child (or None if no left child)."""
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        """Return the Position of p's right child (or None if no right child)."""
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        count = 0
        if node._left is not None:  # left child exists
            count += 1
        if node._right is not None:  # right child exists
            count += 1
        return count

    def _add_root(self, e):
        """Place element e at the root of an empty tree and return new Position.

        Raise ValueError if the tree is nonempty.
        """
        if self._root is not None:
            raise ValueError("Root exists")
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_left(self, p, e):
        """Create a new left child for Position p, storing element e.

        Return the Position of the new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        """
        node = self._validate(p)
        if node._left is not None:
            raise ValueError("Left child exists")
        self._size += 1
        node._left = self._Node(e, node)  # node is its parent
        return self._make_position(node._left)

    def _add_right(self, p, e):
        """Create a new right child for Position p, storing element e.

        Return the Position of the new node.
        Raise ValueError if Position p is invalid or p already has a right child.
        """
        node = self._validate(p)
        if node._right is not None:
            raise ValueError("Right child exists")
        self._size += 1
        node._right = self._Node(e, node)  # node is its parent
        return self._make_position(node._right)

    def replace(self, p, e):
        """Replace the element at position p with e, and return old element."""
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p):
        """Delete the node at Position p and replace it with its child, if any.

        Return the element that had been stored at Position p.
        Raise ValueError if Position p is invalid or p has two children.
        """
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError("Position has two children")

        child = node._left if node._left else node._right  # might be None
        if child is not None:
            child._parent = node._parent  # child's grandparent becomes parent
        if node is self._root:
            self._root = child  # child becomes root
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node  # convention for deprecated node
        return node._element

    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external p."""
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError("Position must be a leaf")
        if not all(isinstance(tree, type(self)) for tree in (t1, t2)):
            raise TypeError("Tree types must match")

        self._size += len(t1) + len(t2)

        if not t1.is_empty():
            # Attach t1 as the left subtree of the node
            t1._root._parent = node
            node._left = t1._root
            t1._root = None  # Set t1 instance to empty
            t1._size = 0

        if not t2.is_empty():
            # Attach t2 as the right subtree of the node
            t2._root._parent = node
            node._right = t2.root
            t2._root = None  # Set t2 instance to empty
            t2._size = 0

    def find_child_by_value(self, p, value):
        for i in self.children(p):
            if i._node._element == value:
                return i
        return None

    def fill(self, elements):
        """Fill the binary tree with elements in a level-order manner.

          Parameters:
          - elements: List of elements to fill the tree with.
          """
        our_queue = deque()                 # the empty our_queue
        self._root = self._Node(elements[0])
        self._size += 1                     
        our_queue.append(self._root)        # enqueue operation for our_queue for root
        pointer_value = 1     # It is the indexes of elements in the list from the beginning.
        while pointer_value < len(elements):
            the_node = our_queue.popleft()  # popleft removes an element from the left side of the our_queue this means its deque our_queue
            if pointer_value < len(elements):   # for left child adding operation
                the_node._left = self._Node(elements[pointer_value], the_node)
                self._size += 1
                our_queue.append(the_node._left)    # enqueue operation
                pointer_value += 1
            if pointer_value < len(elements):       # for right child adding operation
                the_node._right = self._Node(elements[pointer_value], the_node)
                self._size += 1
                our_queue.append(the_node._right)   # enqueue operation
                pointer_value += 1

    def levelorder(self):
        """Perform a level-order traversal of the tree and return a list of elements."""
        if self.is_empty():
            return None
        result = []                 # empty list
        our_queue = deque([self._root]) # Initializing the our_queue to contain self.root()

        while our_queue:                # while q is not empty
            the_node = our_queue.popleft()      # dequeue for our_queue 
            result.append(the_node._element)    # enqueue our_queue the element

            if the_node._left:                  # enqueue our_queue for the left node
                our_queue.append(the_node._left)
            if the_node._right:                 # enqueue our_queue for the right node
                our_queue.append(the_node._right)
        return result                           # returning the result as a list
    
    def preorder(self, p=None):
        """Generate a preorder traversal of the tree rooted at Position p."""
        if p is None:       # for the position none it equates to root
            p = self.root()
        yield p.element()   # performing the visit action for position p
        for c in self.children(p):  # preorder part
            yield from self.preorder(c)

    def inorder(self, p=None):
        """Generate an inorder traversal of the tree rooted at Position p."""
        if p is None:        # for the position none it equates to root
            p = self.root()
        if self.left(p) is not None:    # visiting the nodes of the left subtree
            yield from self.inorder(self.left(p))
        yield p.element()               # root node
        if self.right(p) is not None:   # visiting the nodes of the right subtree
            yield from self.inorder(self.right(p))
        
    def postorder(self, p=None):
        """Generate a postorder traversal of the tree rooted at Position p."""
        if p is None:
            p = self.root()
        for c in self.children(p):  # first each of the subtrees that are rooted at the children of root node are visited than the root node is visited .
            yield from self.postorder(c)
        yield p.element()

    def read_elements_from_file(self,filename):
        with open(filename, 'r') as input_file:
              return [list(line.strip()) for line in input_file]

def main():
    tree = LinkedBinaryTree()
    # Fill the tree with elements in a level-order manner
    elements = tree.read_elements_from_file("test.txt")
    tree.fill(elements)
    # Display tree properties
    print("Tree size:", len(tree))
    print("Root element:", tree.root().element())
    print("Left child of the root:", tree.left(tree.root()).element())
    print("Right child of the root:", tree.right(tree.root()).element())
    # Perform traversals and print the elements
    print("Level traversal:", list(tree.levelorder()))
    print("Preorder traversal:", list(tree.preorder()))
    print("Inorder traversal:", list(tree.inorder()))
    print("Postorder traversal:", list(tree.postorder()))
if __name__ == "__main__":
    main()
