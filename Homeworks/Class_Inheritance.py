import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

class Shape:
    def __init__(self):
        self.leftTop = None
        self.points = []

    def calculatePoints(self):
        raise NotImplementedError("Subclasses must implement calculatePoints")

    def calculateArea(self):
        raise NotImplementedError("Subclasses must implement calculateArea")

    def calculatePerimeter(self):
        raise NotImplementedError("Subclasses must implement calculatePerimeter")

    def move(self, new_leftTop):
        if not isinstance(new_leftTop, Point):
            raise ValueError("new_leftTop should be a Point object")
        dx = new_leftTop.x - self.leftTop.x
        dy = new_leftTop.y - self.leftTop.y
        self.leftTop = new_leftTop
        for point in self.points:
            point.x += dx
            point.y += dy

class Rectangle(Shape):
    def __init__(self, leftTop, height, width):
        super().__init__()
        self.leftTop = leftTop
        self.height = height
        self.width = width
        self.calculatePoints()

    def calculatePoints(self):
        self.points = [self.leftTop,
                       Point(self.leftTop.x + self.width, self.leftTop.y),
                       Point(self.leftTop.x + self.width, self.leftTop.y + self.height),
                       Point(self.leftTop.x, self.leftTop.y + self.height)]

    def calculateArea(self):
        return self.width * self.height

    def calculatePerimeter(self):
        return 2 * (self.width + self.height)

    def __str__(self):
        return f"Rectangle with top left at {self.leftTop}, height {self.height}, width {self.width}, area {self.calculateArea()}, perimeter {self.calculatePerimeter()}"

class Circle(Shape):
    def __init__(self, leftTop, radius):
        super().__init__()
        self.leftTop = leftTop
        self.radius = radius
        self.calculatePoints()

    def calculatePoints(self):
        self.points = [self.leftTop,
                       Point(self.leftTop.x + 2 * self.radius, self.leftTop.y + 2 * self.radius)]

    def calculateArea(self):
        return math.pi * (self.radius ** 2)

    def calculatePerimeter(self):
        return 2 * math.pi * self.radius

    def __str__(self):
        return f"Circle with top left at {self.leftTop}, radius {self.radius}, area {self.calculateArea()}, perimeter {self.calculatePerimeter()}"

# Main program
shapes = []
while True:
    command = input("Type of shape (r for rectangle, c for circle, q to quit): ").strip().lower()

    if command == 'q':
        break
    elif command == 'r':
        x = float(input("Enter the x-coordinate of the top-left point: "))
        y = float(input("Enter the y-coordinate of the top-left point: "))
        height = float(input("Enter the height: "))
        width = float(input("Enter the width: "))
        rectangle = Rectangle(Point(x, y), height, width)
        shapes.append(rectangle)
        print(rectangle)

        move_command = input("Enter 'm' to move the last created shape (or any other key to skip): ").strip().lower()
        if move_command == 'm':
            new_x = float(input("Enter the new x-coordinate of the top-left point: "))
            new_y = float(input("Enter the new y-coordinate of the top-left point: "))
            rectangle.move(Point(new_x, new_y))
            print(rectangle)

    elif command == 'c':
        x = float(input("Enter the x-coordinate of the top-left point: "))
        y = float(input("Enter the y-coordinate of the top-left point: "))
        radius = float(input("Enter the radius: "))
        circle = Circle(Point(x, y), radius)
        shapes.append(circle)
        print(circle)

        move_command = input("Enter 'm' to move the last created shape (or any other key to skip): ").strip().lower()
        if move_command == 'm':
            new_x = float(input("Enter the new x-coordinate of the top-left point: "))
            new_y = float(input("Enter the new y-coordinate of the top-left point: "))
            circle.move(Point(new_x, new_y))
            print(circle)

# End of the program
print("Exiting the program.")

