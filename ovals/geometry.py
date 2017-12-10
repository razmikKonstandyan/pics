# -*- coding: utf-8 -*-
import numpy as np

from math import cos, sin


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


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
