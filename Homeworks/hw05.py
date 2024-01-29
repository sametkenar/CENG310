class Node:
    def __init__(self, index, value, next=None):
        self.index = index
        self.value = value
        self.next = next

class SparseArray:
    def __init__(self, size):
        self.size = size
        self.head = None

    def __getitem__(self, j):
        if not (0 <= j < self.size):
            raise IndexError(f"Index {j} out of range")

        current = self.head
        while current:
            if current.index == j:
                return current.value
            current = current.next
        return None

    def __setitem__(self, j, e):
        if not (0 <= j < self.size):
            raise IndexError(f"Index {j} out of range")

        if e is None:
            return  # Do not store None values in the sparse array

        current = self.head
        prev = None

        while current and current.index < j:
            prev = current
            current = current.next

        if current and current.index == j:
            current.value = e
        else:
            new_node = Node(j, e, current)

            if prev:
                prev.next = new_node
            else:
                self.head = new_node


"""In this implementation, the Node class represents each nonempty cell in the sparse array, 
and the SparseArray class uses a linked list to efficiently store and retrieve values. 
The getitem method allows you to retrieve the value at a given index, 
and the setitem method allows you to set the value at a given index.
The efficiency of the getitem method is O(m), where m is the number of nonempty entries in the sparse array. 
The setitem method also has an efficiency of O(m) because it may involve 
traversing the linked list to find the correct position to insert or update a node.
"""

sa = SparseArray(100) # All cells will have value None

sa[23] = 'C'
sa[24] = [1,2] # at this moment linked list should have only two nodes.
print(sa[23])
print(sa[24])
print(sa[25]) # should return None, but internally no node #25 should exist.
sa[100] = 1 #should raise IndexError