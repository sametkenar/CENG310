from tree import LinkedBinaryTree

tree = LinkedBinaryTree()

# Fill the tree with elements with elements in a level-order manner
elements = tree.read_elements_from_file("test.txt")
tree.fill(elements)

# Display tree properties
print("Tree size:", len(tree))
print("Root element", tree.root().element())
print("Left child of the root:", tree.left(tree.root()).element())
print("Right child of the root:", tree.right(tree.root()).element())
tree.levelorder()
# Perform traversals and print the elements
print("Preorder traversal:", list(tree.preorder()))
print("Inorder traversal:", list(tree.inorder()))
print("Postorder traversal:", list(tree.postorder()))
