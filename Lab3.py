import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt

def hermite(p0, p1, t0, t1, n=100):
    t = np.linspace(0, 1, n)
    h00 = 2 * t**3 - 3 * t**2 + 1
    h10 = t**3 - 2 * t**2 + t
    h01 = -2 * t**3 + 3 * t**2
    h11 = t**3 - t**2
    return h00[:, None]*p0 + h10[:, None]*t0 + h01[:, None]*p1 + h11[:, None]*t1

def compute_T(P, i, t=0, c=0, b=0):
    Pi_1, Pi, Pi1 = P[i-1], P[i], P[i+1]
    T_plus = ((1 - c)*(Pi1 - Pi) + (1 + c)*(Pi - Pi_1)) / 2
    T_minus = ((1 + c)*(Pi1 - Pi) + (1 - c)*(Pi - Pi_1)) / 2
    T_plus *= (1 - t) * (1 + b)
    T_minus *= (1 - t) * (1 - b)
    return T_plus, T_minus
"""
T (натяг) — наскільки крива "натягнута" 

C (неперервність) — як різко вона змінює напрям

B (нахил) — чи крива зміщується трохи вгору або вниз, лівіше чи правіше"""
def get_points():
    n = int(input("Скільки точок? (мінімум 4): "))
    while n < 4:
        print("Потрібно принаймні 4 точки для побудови ТСВ-сплайну!")
        n = int(input("Скільки точок введеш? "))

    points = []
    for i in range(n):
        coords = input(f"Введи координати точки {i+1} у форматі x y: ").strip().split()
        x, y = float(coords[0]), float(coords[1])
        points.append([x, y])
    return np.array(points)

print("Побудова ТСВ-сплайну")

P = get_points()

P = np.vstack([P[0], P, P[-1]])

curves = []
for i in range(1, len(P) - 2):
    T_plus, _ = compute_T(P, i)
    _, T_minus = compute_T(P, i + 1)
    curve = hermite(P[i], P[i+1], T_plus, T_minus)
    curves.append(curve)

for curve in curves:
    plt.plot(curve[:, 0], curve[:, 1], 'b')

original_points = P[1:-1]
plt.plot(original_points[:, 0], original_points[:, 1], 'ro--', label='Контрольні точки')

plt.title("ТСВ-сплайн з проходженням через крайні точки")
plt.grid()
plt.axis('equal')
plt.legend()
plt.show()

