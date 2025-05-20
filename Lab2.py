import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class Fractal:
    def __init__(self, size):
        self.size = size
        self.x = [-size, size]
        self.y = [0, 0]
        self.center = [0, 0]

    def side(self, x, y, size):
        left_x = x - size / 2
        right_x = x + size / 2
        top_y = y + size / 2
        bottom_y = y - size / 2
        return [(left_x, top_y), (left_x, bottom_y), (right_x, top_y), (right_x, bottom_y)]



    def draw(self, x, y, size, depth):
        if depth == 0:
            return

        ax1.plot([x - size / 2, x + size / 2], [y, y], color='black')

        coords = self.side(x, y, size)

        for i in range(0, len(coords), 2):
            ax1.plot([coords[i][0], coords[i + 1][0]], [coords[i][1], coords[i + 1][1]], color='black')

        for cx, cy in coords:
            self.draw(cx, cy, size / 3, depth - 1)

fig, ax1 = plt.subplots()
e_depth = input("Enter the depth of the fractal: ")
fractal = Fractal(10)
fractal.draw(0, 0, 10, int(e_depth))

ax1.set_aspect('equal')
ax1.axis('off')
plt.show()
