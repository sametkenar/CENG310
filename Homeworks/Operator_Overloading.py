class Vector:
    """Represent a vector in a multidimensional space"""
# TASK-8 This part is modified. 
    def __init__(self,d):
        """Create a vector of zeros with a given dimension or based on a sequence.""" 
        if isinstance(d, int):
            self._coords = [0] * d
        elif isinstance(d, (list,tuple)):
            self._coords = list(d)
        else: 
            raise ValueError('Invalid argument. Please provide an integer or a sequence of numbers.')
    
    def __len__(self):
        """Return the dimension of the vector."""
        return len(self._coords)
    
    def __getitem__(self, j):
        """Return the jth coordinate of vector."""
        return self._coords[j]
    
    def __setitem__(self, j, val):
        """Set jth coordinate of vector to given value."""
        self._coords[j] = val

    def __add__(self,other):
        """Return sum of two vectors."""
        if len(self) != len(other):             # relies on __len__ method
            raise ValueError('dimensions must agree')
        result = Vector(len(self))              # start with vector of zeros
        for j in range(len(self)):
            result[j] = self[j] + other[j]
        return result

    def __eq__(self,other):
        """Return True if vector has same coordinates as other."""
        return self._coords == other._coords

    def __ne__(self,other):
        """Return True if vector differs from other."""
        return not self == other                # rely on existing __eq__ function
    def __str__(self):
        """Produce string representation of vector."""
        return '<' + ', '.join(map(str, self._coords)) + '>'      
# TASK-2
    def __sub__(self, other):       # Vector extraction
        """Return the difference between two vectors."""
        if len(self) != len(other): # Check if dimensions agree
            raise ValueError('Dimensions must agree')
        result = Vector(len(self)) # Create a new vector for the result
        for j in range(len(self)):
            result[j] = self[j] - other[j] # Subract corresponding coordinates
        return result       
# TASK-3
    def __neg__(self):    
        """Return a new vector with negated coordinates."""
        result = Vector(len(self)) # Create a new vector for the result
        for j in range(len(self)):
            result[j] = -self[j] # Negate each coordinate
        return result

 # TASK-4 (In here, we are adding a list to a Vector to create a new vector. With this method we can do this.)
    def __radd__(self,other):
        """Return a new vector by adding a list to the vector."""
        if isinstance(other,list):
            if len(other) != len(self):
                raise ValueError('List and vector dimensions must agree')
            result = Vector(len(self)) # Create a new vector for the result
            for j in range(len(self)):
                result[j] = other[j] + self[j]
            return result
        else:
            raise TypeError('Unsupported operand type. You can only add a list to a vector.')
        
# TASK-5-7 In here we are enhanced the mull function.
    def __mul__(self,other):
        """Return the dot product of two vectors or perform scalar multiplication with a vector.""" 
        if isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError('Vector dimensions must be the same for dot product calculation.')
            dot_product = 0
            for j in range(len(self)):
                dot_product += self[j] * other[j]
            return dot_product
        elif isinstance(other, (int,float)):
            result = Vector(len(self)) # Create a new vector for scalar multipliciation
            for j in range(len(self)):
                result[j] = self[j] * other
            return result
        else: 
            raise TypeError('Unsupported operand type. You can multiply a vector by another vector or a scalar.')

# TASK-6
    def __rmul__(self,scalar):
        """Return a new vector with coordinates multiplied by the scalar (scalar on the right)."""
        if not isinstance(scalar, (int,float)):
            raise TypeError('Unsupported operand type. You can only multiply a vector by a scalar.')
        result = Vector(len(self)) # Create a new vector for the result
        for j in range(len(self)):
            result[j] = self[j] * scalar
        return result 

# TASK-2 TEST
# Create two vectors
u = Vector(3)
u[0] = 1
u[1] = 2
u[2] = 3
v = Vector(3)
v[0] = 4
v[1] = 5
v[2] = 6
# Substract v from u 
result = u - v
# Print the result
print("TASK-2 EXAMPLE")
print(result)

# TASK-3 TEST
# Create a vector
v = Vector(3)
v[0] = 1
v[1] = 2
v[2] = 3
# Negate the vector -v
result = -v
# Print the result
print("TASK-3 EXAMPLE")
print(result)

# TASK-4 TEST
u = Vector(5)
u[0] = 1
u[1] = 2
u[2] = 3
u[3] = 4
u[4] = 5
v = [5, 3, 10, -2, 1] + u # This will work
print("TASK-4 EXAMPLE")
print(v)

# TASK-5 TEST
v = Vector(3)
v[0] = 1
v[1] = 2
v[2] = 3
# Multiply the vector by a scalar
result = v*3
# Print the result
print("TASK-5 EXAMPLE")
print(result)

# TASK-6 TEST
v = Vector(3)
v[0] = 1
v[1] = 2
v[2] = 3
# Perform a scalar multiplication with the vector on the right
result = 3*v
# Print the result
print("TASK-6 EXAMPLE")
print(result)

# TASK-7 TEST
# Create two vectors
u = Vector(3)
u[0] = 1
u[1] = 2
u[2] = 3
v = Vector(3)
v[0] = 4
v[1] = 5
v[2] = 6
# Calculate the dot product of the vectors
result = u * v
# Print the result
print("TASK-7 EXAMPLE")
print(result) 

# TASK-8 TEST
# Create a vector of zeros with a dimension of 3
zero_vector = Vector(3)
print("TASK-8 EXAMPLE")
print(zero_vector) 
# Create a vector based on a list of numbers
custom_vector = Vector([1,2,3])
print(custom_vector)