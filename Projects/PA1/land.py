# FINDING ISLAND CLASS

class IslandFinder:
    def __init__(self, path):       # Initializing land, cellstack, explored list, and _MaxArea.
        self._land = self.text_to_array(path)
        self._cellstack = []
        self._explored = []
        self._maxArea = 0

    def text_to_array(self, path):
        with open(path, 'r') as input_file:           # Reading input_file and returning it as an list.
            return [list(line.strip()) for line in input_file]

    def get_a_neighbor(self, a_tuple):
        row, column = a_tuple  # automatically tuple from python built in structure.
        neighbors = []  # empty list
        # Below code we are checking the around of the cells.
        # To control upper cell
        if row > 0 and self._land[row - 1][column] == '1' and (row - 1, column) not in self._explored:
            neighbors.append((row - 1, column))
        # To control right cell
        if column < len(self._land[0]) - 1 and self._land[row][column + 1] == '1' and (row, column + 1) not in self._explored:
            neighbors.append((row, column + 1))
        # To control lower cell
        if row < len(self._land) - 1 and self._land[row + 1][column] == '1' and (row + 1, column) not in self._explored:
            neighbors.append((row + 1, column))
        # To control left cell
        if column > 0 and self._land[row][column - 1] == '1' and (row, column - 1) not in self._explored:
            neighbors.append((row, column - 1))

        # Returning a valid neighbor
        return neighbors[0] if neighbors else None

    def find_island(self):  # Finding Island function
        # Clearing and initializing _cellstack and _explored.
        self._cellstack = []
        self._explored = []
        self._maxArea = 0
        # Iterating through each cell in the grid.
        for row in range(len(self._land)):
            for column in range(len(self._land[0])):
                current_cell = (row, column)
                # If the current cell is part of an island and not in _explored
                if self._land[row][column] == '1' and current_cell not in self._explored:
                    # Initializing _area to 0
                    _area = 0
                    # Pushing the current cell to _cellstack
                    self._cellstack.append(current_cell)
                    # While _cellstack is not empty, loop
                    while self._cellstack:
                        # Geting the top cell c from the _cellstack
                        c = self._cellstack.pop()
                        # If c is not in _explored
                        if c not in self._explored:
                            # Marking c as visited
                            self._explored.append(c)
                            # Incrementing _area
                            _area += 1
                            # Adding unvisited neighbors of c to _cellstack
                            neighbor = self.get_a_neighbor(c)
                            if neighbor:
                                self._cellstack.append(neighbor)
                    # Updating _maxArea with the maximum of _maxArea and _area
                    self._maxArea = max(self._maxArea, _area)
        # Return _maxArea, which represents the maximum area of an island in the grid
        return self._maxArea
    
# LAND CLASS

class InvalidLandException(Exception):
    pass

class Land:
    def __init__(self, structure_of_land):
        self.validating_structure_of_land(structure_of_land) # We are utilizing validating_structure_of_land function to check the mentioned rules in the constructor.
        self.structure_of_land = structure_of_land

    def validating_land_strucure(self, structure_of_land): # This functions checks the mentioned rules in the assignment.           
        if not isinstance(structure_of_land, list) or not all(isinstance(row, list) and len(row) > 3 for row in structure_of_land): # Checking the internal lists and their lengths.
            raise InvalidLandException("Invalid land structure: It has to be a mxn array where m > 3 and n > 3, and and each of the internal lists should be of length n.")
        validated_characters = {'0', '1'}
        for row in structure_of_land: # Checking each cells characters whether they are 0,1 or not.
            for cell in row:
                if len(cell) != 1 or cell not in validated_characters:
                    raise InvalidLandException("Invalid land structure: Each cell has to be a single character '0'(water) or '1'(island)).")
        if len(structure_of_land) < 4 or any(len(row) != len(structure_of_land[0]) for row in structure_of_land): # Checking the array.
            raise InvalidLandException("Invalid land structure: Have be a mxn array where m > 3 and n > 3.")
    def get_start(self):
        return (0, 0)

# STACK CLASS

# Basic ArrayStack class implementation.

class Empty(Exception):
    """Error attempting to access an element from an container."""
    pass

class ArrayStack:
    """LIFO Stack implementation using a Python list as underlying storage."""

    def __init__(self):
        """Create an empty stack."""
        self._data = []         # nonpublic list instance
    
    def __len__(self):
        """Return the number of elements in the stack."""
        return len(self._data)
    
    def is_empty(self):
        """Return True if the stack is empty."""
        return len(self._data) == 0
    
    def push(self, e):
        """Add element e to the top of the stack."""
        self._data.append(e)            # new item stored at the end of list

    def top(self):
        """Return (but do not remove) the element at the top of the stack.
        
        Raise Empty exception if the stack is empty."""
        if self.is_empty():
            raise Empty('Stack is empty.')
        return self._data[-1]           # the last item in the list
    
    def pop(self):
        """Remove and return the element from the top of the stack (i.e., LIFO).
        
        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty.')
        return self._data.pop()         # remove last item from list