# -*- coding: utf-8 -*-
import numpy as np

from math import cos, sin


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)


class Line(object):

    def __init__(self, k, b, left_x=-1, right_x=1, down_y=-1, up_y=1, step=0.1):
        self.k = k
        self.b = b
        self.left_x = left_x
        self.right_x = right_x
        self.down_y = down_y
        self.up_y = up_y
        self.step = step

    @property
    def points(self):
        result = []
        for x in np.arange(self.left_x, self.right_x, self.step):
            y = self.k * x + self.b
            # window for y coordinate
            if self.up_y > y > self.down_y:
                result.append(Point(x, y))
        return result

    def __str__(self):
        return 'y = %s * x + %s' % (self.k, self.b)


class Ellipse(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.points = [Point(a * cos(t), b * sin(t)) for t in np.arange(0, 2 * 3.14, 0.001)] + [Point(0.0, 0.0)]


class Oval(object):

    def __init__(self, a, b, power, offset_x=1, offset_y=1):
        self.power = power
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.points = [Point((p.x + a + offset_x) ** power, p.y) for p in Ellipse(a, b).points]

    def projective_transform(self, a0, a1, a2, b0, b1, b2, d1, d2):
        transformed_points = []
        for p in self.points:
            first_numerator = a0 + a1 * p.x + a2 * p.y
            second_numerator = b0 + b1 * p.x + b2 * p.y
            divider = 1 + d1 * p.x + d2 * p.y
            x_transformed = first_numerator / divider
            y_transformed = second_numerator / divider
            transformed_points.append(Point(x_transformed, y_transformed))
        self.points = transformed_points

    def derivative(self, a1, a2, c1, c2):
        return (a1.y + a2.y - c1.y - c2.y) / (a1.x + a2.x - c1.x - c2.x)

    def get_tangent_line(self, point, left_power=1.0, right_power=1.0, down_power=1.0, up_power=1.0, step=0.01):
        l1 = l2 = r1 = r2 = None
        for i, p in enumerate(self.points):
            if p == point:
                if i == len(self.points) - 2:
                    l1, l2, p, r1 = self.points[i - 2:i + 2]
                    r2 = self.points[0]
                elif i == len(self.points) - 1:
                    l1, l2, p = self.points[i - 2:]
                    r1. r2 = self.points[:2]
                elif i == 0:
                    p, r1, r2 = self.points[:i + 3]
                    l1, l2 = self.points[-2:]
                elif i == 1:
                    l2, p, r1, r2 = self.points[:i + 4]
                    l1 = self.points[-1]
                else:
                    l1, l2, p, r1, r2 = self.points[i-2:i+3]
        if l1 is None:
            raise Exception('Point %s was not found!', point)
        k = self.derivative(l1, l2, r1, r2)
        b = point.y - point.x * k
        left_x = self.min_x * left_power
        right_x = self.max_x * right_power
        down_y = self.min_y * down_power
        up_y = self.max_y * up_power
        return Line(k, b, left_x, right_x, down_y, up_y, step)

    # Remove this shit soon
    def form_line_by_two_points(self, first_point, second_point, **kwargs):
        a = np.array([[first_point.x, 1], [second_point.x, 1]])
        b = np.array([first_point.y, second_point.y])
        return Line(*np.linalg.solve(a, b), **kwargs)

    @property
    def min_x(self):
        return min([p.x for p in self.points])

    @property
    def max_x(self):
        return max([p.x for p in self.points])

    @property
    def min_y(self):
        return min([p.y for p in self.points])

    @property
    def max_y(self):
        return max([p.y for p in self.points])
