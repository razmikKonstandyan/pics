# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from math import cos, sin


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Elipse(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_points(self):
        points = []
        for t in np.arange(0, 2 * 3.14, 0.001):
            x = self.a * cos(t)
            y = self.b * sin(t)
            points.append(Point(x, y))
        return points

    def draw(self):
        x_points = [point.x for point in self.get_points()]
        y_points = [point.y for point in self.get_points()]
        plt.plot(x_points, y_points, 'ro')
        plt.show()


class Oval(Elipse):

    def __init__(self, a, b, power, offset_x=1, offset_y=1):
        super(Oval, self).__init__(a, b)
        self.power = power
        self.offset_x = offset_x
        self.offset_y = offset_y

    def projective_transform(self, a0, a1, a2, b0, b1, b2, d1, d2):
        transformed_points = []
        for p in self.get_points():
            first_numerator = a0 + a1 * p.x + a2 * p.y
            second_numerator = b0 + b1 * p.x + b2 * p.y
            divider = 1 + d1 * p.x + d2 * p.y
            x_transformed = first_numerator / divider
            y_transformed = second_numerator / divider
            transformed_points.append(Point(x_transformed, y_transformed))

        x_points = [point.x for point in transformed_points]
        y_points = [point.y for point in transformed_points]
        plt.plot(x_points, y_points, 'ro')
        plt.show()

    def get_points(self):
        power_points = []
        for p in super(Oval, self).get_points():
            x = (p.x + self.a + self.offset_x) ** self.power
            y = (p.y + self.b + self.offset_y) ** self.power
            power_points.append(Point(x, y))
        return power_points

if __name__ == '__main__':
    o = Oval(4, 2, 2.3)
    o.draw()
    o.projective_transform(0.1, 0.2, 0.1, -2, 0.3, 2, 0.3, 0.1)
