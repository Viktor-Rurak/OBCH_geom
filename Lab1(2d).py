import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


class Square:
    def __init__(self, x1, y1, x2, y2):
        self.center_x = (x1 + x2) / 2
        self.center_y = (y1 + y2) / 2
        self.size = abs(x2 - x1)
        self.angle = 0

    def get_corners(self):
        half_size = self.size / 2
        corners = [
            (-half_size, -half_size),
            (-half_size, half_size),
            (half_size, half_size),
            (half_size, -half_size)
        ]
        rotated_corners = [
            (self.center_x + x * np.cos(self.angle) - y * np.sin(self.angle),
             self.center_y + x * np.sin(self.angle) + y * np.cos(self.angle))
            for x, y in corners
        ]
        return rotated_corners

    def move(self, dx, dy, rotation_step):
        self.center_x += dx
        self.center_y += dy
        self.angle += rotation_step

    def draw_square(self):
        corners = self.get_corners()
        x_coords, y_coords = zip(*corners)
        plt.plot(list(x_coords) + [x_coords[0]], list(y_coords) + [y_coords[0]], "b-", linewidth=2)


class Line:
    def __init__(self, slope, intercept, x_range):
        self.x = np.linspace(x_range[0] - 5, x_range[1] + 5, 200)  # Подовжуємо пряму
        self.y = slope * self.x + intercept  # Обчислюємо відповідні y
        self.slope = slope
        self.intercept = intercept

    def draw_line(self):
        plt.plot(self.x, self.y, "r-", linewidth=2)

    def distance_to_square(self, square):
        corners = square.get_corners()
        distances = [
            abs(self.slope * x - y + self.intercept) / np.sqrt(self.slope ** 2 + 1)
            for x, y in corners
        ]
        return min(distances)

    def intersects_square(self, square):
        corners = square.get_corners()
        edges = [(corners[i], corners[(i + 1) % 4]) for i in range(4)]
        for (x1, y1), (x2, y2) in edges:
            if self.line_intersects_segment(x1, y1, x2, y2):
                return True
        return False

    def line_intersects_segment(self, x1, y1, x2, y2):
        y1_line = self.slope * x1 + self.intercept
        y2_line = self.slope * x2 + self.intercept
        return (y1 - y1_line) * (y2 - y2_line) <= 0


#протилежні точки квадрата
x1, y1 = map(float, input("Enter coordinates of first corner (x1 y1): ").split())
x2, y2 = map(float, input("Enter coordinates of opposite corner (x2 y2): ").split())

square = Square(x1, y1, x2, y2)


#(y = kx + c)
slope = float(input("Enter the slope of the line (k): "))
intercept = float(input("Enter the intercept of the line (c): "))

x_range = [min(x1, x2) - 3, max(x1, x2) + 3]

line = Line(slope, intercept, x_range)

if line.intersects_square(square):
    print("The given line passes through the square. Please enter different data.")

else:
    pass

dx = -slope / np.sqrt(slope ** 2 + 1) * 0.1
dy = 1 / np.sqrt(slope ** 2 + 1) * 0.1
rotation_step = np.pi / 36

plt.ion()
fig, ax = plt.subplots()

while line.distance_to_square(square) > 0.1:
    ax.clear()
    square.move(dx, dy, rotation_step)
    line.draw_line()
    square.draw_square()
    plt.grid(True)
    plt.title("Moving Rotating Square Towards Line")
    plt.pause(0.05)

plt.ioff()
plt.show()