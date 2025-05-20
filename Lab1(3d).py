import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

class Square:
    def __init__(self, cx, cy, cz, size):
        self.center = np.array([cx, cy, cz], dtype=float)
        self.size = size
        self.angle = 0

    def get_corners(self):
        half = self.size / 2
        base = [
            [half, -half],  # Передній правий
            [-half, -half], # Передній лівий
            [-half, half],  # Задній лівий
            [half, half]    # Задній правий
        ]
        rotated = []
        for x, y in base:
            xr = x * np.cos(self.angle) - y * np.sin(self.angle)
            yr = x * np.sin(self.angle) + y * np.cos(self.angle)
            rotated.append(self.center + np.array([xr, yr, 0]))
        return rotated

    def move(self, direction, angle_step):
        self.center += direction
        self.angle += angle_step

    def draw(self, ax):
        corners = self.get_corners()
        x, y, z = zip(*corners)
        x += (x[0],)
        y += (y[0],)
        z += (z[0],)
        ax.plot(x, y, z, 'b-', linewidth=2)

class Line3D:
    def __init__(self, point, direction):
        self.point = np.array(point, dtype=float)
        self.direction = np.array(direction, dtype=float)
        self.direction /= np.linalg.norm(self.direction)

    def draw(self, ax):
        t = np.linspace(-20, 20, 200)
        x = self.point[0] + self.direction[0] * t
        y = self.point[1] + self.direction[1] * t
        z = self.point[2] + self.direction[2] * t
        ax.plot(x, y, z, 'r-', linewidth=2)

    def distance_to_point(self, p):
        ap = p - self.point
        proj = np.dot(ap, self.direction) * self.direction
        perp = ap - proj
        return np.linalg.norm(perp), -perp / np.linalg.norm(perp)

# Ввід
cx, cy, cz = map(float, input("Enter square center (x y z): ").split())
size = float(input("Enter square size: "))
line_point = list(map(float, input("Enter a point on the line (x y z): ").split()))
line_dir = list(map(float, input("Enter direction vector of the line (dx dy dz): ").split()))

square = Square(cx, cy, cz, size)
line = Line3D(line_point, line_dir)

rotation_step = np.pi / 36
dist, move_dir = line.distance_to_point(square.center)

# Визначаємо площину перевірки дотику (попереду квадрата)
plane_distance = dist - size / 2
plane_point = square.center + move_dir * plane_distance

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Головний цикл
while True:
    ax.clear()
    square.move(move_dir * 0.05, rotation_step)

    # Перевіряємо **усі** кути квадрата
    collision = False
    for corner in square.get_corners():
        projected_distance = np.dot(corner - plane_point, move_dir)
        if projected_distance >= 0:
            collision = True
            break  # Зупиняємось, якщо хоч один кут перетнув площину

    if collision:
        break

    # Малюємо
    line.draw(ax)
    square.draw(ax)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-10, 10)
    ax.set_title("3D Square Approaching Line")
    plt.pause(0.05)

# Фінальна сцена
ax.clear()
line.draw(ax)
square.draw(ax)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)
ax.set_title("Touch Detected")
plt.ioff()
plt.show()
