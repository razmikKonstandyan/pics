# -*- coding: utf-8 -*-
import numpy as np

from math import cos, sin


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Line(object):

    def __init__(self, k, b, left_x, right_x, step=0.01):
        self.k = k
        self.b = b
        self.left_x = left_x
        self.right_x = right_x
        self.step = step

    @property
    def points(self):
        result = []
        for x in np.arange(self.left_x, self.right_x, self.step):
            y = self.k * x + self.b
            result.append(Point(x, y))
        return result


class Ellipse(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def points(self):
        points = [Point(0.0, 0.0)]
        for t in np.arange(0, 2 * 3.14, 0.001):
            x = self.a * cos(t)
            y = self.b * sin(t)
            points.append(Point(x, y))
        return points


class Oval(Ellipse):

    def __init__(self, a, b, power, offset_x=1, offset_y=1):
        super(Oval, self).__init__(a, b)
        self.power = power
        self.offset_x = offset_x
        self.offset_y = offset_y

    def projective_transform(self, a0, a1, a2, b0, b1, b2, d1, d2):
        transformed_points = []
        for p in self.points:
            first_numerator = a0 + a1 * p.x + a2 * p.y
            second_numerator = b0 + b1 * p.x + b2 * p.y
            divider = 1 + d1 * p.x + d2 * p.y
            x_transformed = first_numerator / divider
            y_transformed = second_numerator / divider
            transformed_points.append(Point(x_transformed, y_transformed))
        return transformed_points

    @property
    def points(self):
        power_points = []
        for p in super(Oval, self).points:
            x = (p.x + self.a + self.offset_x) ** self.power
            y = (p.y + self.b + self.offset_y) ** self.power
            power_points.append(Point(x, y))
        return power_points

    def derivative(self, a1, a2, c1, c2):
        return (a1.y + a2.y - c1.y - c2.y) / (a1.x + a2.x - c1.x - c2.x)

    def get_tangent_points(self, point, left_power=0, right_power=0):
        l1 = l2 = r1 = r2 = None
        for i, p in enumerate(self.points):
            if p == point:
                import logging
                logging.info(self.points[i-2:i+3])
                l1, l2, p, r1, r2 = self.points[i-2:i+3]
        if l1 is None:
            raise Exception('Point %s was not found!', point)
        k = self.derivative(l1, l2, r1, r2)
        b = point.y - point.x * k
        left_x = self.min_x - self.min_x * left_power
        right_x = self.max_x + self.max_x * right_power
        return Line(k, b, left_x, right_x).points

    @property
    def min_x(self):
        return min([p.x for p in self.points])

    @property
    def max_x(self):
        return max([p.x for p in self.points])
