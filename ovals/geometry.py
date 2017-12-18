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



# from math_calculations import get_lines_intersection_point

#
# def get_lines_intersection_point(first_line, second_line):
#     a = np.array([[-first_line.k, 1], [-second_line.k, 1]])
#     b = np.array([first_line.b, second_line.b])
#     return Point(*np.linalg.solve(a, b))
#
# def get_support_points(L, R, A, T):
#     LA = oval.form_line_by_two_points(L, A)
#     LT = oval.form_line_by_two_points(L, T)
#     RA = oval.form_line_by_two_points(R, A)
#     RT = oval.form_line_by_two_points(R, T)
#
#
#     L_tangent = oval.get_tangent_line(L, down_power=2., up_power=2.0, left_power=2.0, right_power=2.0)
#     R_tangent = oval.get_tangent_line(R, left_power=1, right_power=1.3, down_power=12.7, up_power=1)
#     A_tangent = oval.get_tangent_line(A, left_power=1, right_power=.3, down_power=1.7, up_power=1)
#     T_tangent = oval.get_tangent_line(T, left_power=1, right_power=.3, down_power=1.7, up_power=1)
#
#     L_R = get_lines_intersection_point(L_tangent, R_tangent)
#     L_T = get_lines_intersection_point(L_tangent, T_tangent)
#     A_L = get_lines_intersection_point(A_tangent, L_tangent)
#     R_A = get_lines_intersection_point(R_tangent, A_tangent)
#     RA_LT = get_lines_intersection_point(RA, LT)
#     A_L__RA_LT = oval.form_line_by_two_points(A_L, RA_LT)
#     A_L__RA_LT___R = get_lines_intersection_point(R_tangent, A_L__RA_LT)
#     LA_R = get_lines_intersection_point(LA, R_tangent)
#     RT_A_L__RA_LT = get_lines_intersection_point(RT, A_L__RA_LT)
#     RT_LA = get_lines_intersection_point(RT, LA)
#     L_R__RT_LA = oval.form_line_by_two_points(L_R, RT_LA)
#     L_R__RT_LA___A_L__RA_LT = get_lines_intersection_point(L_R__RT_LA, A_L__RA_LT)
#     T_A = get_lines_intersection_point(T_tangent, A_tangent)
#     LA__A_L__RA_LT = get_lines_intersection_point(LA, A_L__RA_LT)
#     result = {
#         'points': [L_R, L, R, T, A, L_T, RA_LT, LA_R, A_L, R_A, A_L__RA_LT___R, RT_A_L__RA_LT, T_A, RT_LA, LA__A_L__RA_LT, L_R__RT_LA___A_L__RA_LT],
#         'labels': ['L_R', 'L', 'R', 'T', 'A', 'L_T', 'RA_LT', 'LA_R', 'A_L', 'R_A', 'A_L__RA_LT___R', 'RT_A_L__RA_LT', 'T_A', 'RT_LA', 'LA__A_L__RA_LT', 'L_R__RT_LA___A_L__RA_LT']
#     }
#     return result
#
# def get_wurf_value(p1, p2, p3, p4):
#     # TODO Добавить проверку что они коллинеары
#     la = ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5
#     lb = ((p3.x - p2.x) ** 2 + (p3.y - p2.y) ** 2) ** 0.5
#     lc = ((p4.x - p3.x) ** 2 + (p4.y - p3.y) ** 2) ** 0.5
#     return float((la + lb) * (lb + lc)) / float((lb * (la + lb + lc)))
#
# a = 2
# b = 4
# power = 1.3
# oval = Oval(a, b, power)
# oval.projective_transform(10, 12, 3, 10, 4, 12, 6, 2)
# L = oval.points[-253]
# R = oval.points[-2393]
# A = oval.points[3300]
# T = oval.points[2600]
# for T in oval.points:
#     for A in oval.points:
#         L_R, L, R, T, A, L_T, RA_LT, LA_R, A_L, R_A, A_L__RA_LT___R, RT_A_L__RA_LT, T_A, RT_LA, LA__A_L__RA_LT, L_R__RT_LA___A_L__RA_LT = get_support_points(L, R, A, T)['points']
#         v1 = get_wurf_value(A_L, T_A, A, R_A)
#         v2 = get_wurf_value(A_L, L_T, L, L_R)
#         v3 = get_wurf_value(L, RT_LA, A, LA_R)
#         v4 = get_wurf_value(L, A, LA__A_L__RA_LT, LA_R)
#         v5 = get_wurf_value(L_T, T, T_A, A_L__RA_LT___R)
#         v6 = get_wurf_value(L_R, R, R_A, A_L__RA_LT___R)
#         w1 = get_wurf_value(LA__A_L__RA_LT, A, RT_LA, L)
#         w2 = get_wurf_value(RT_A_L__RA_LT, T, RT_LA, R)
#         w3 = get_wurf_value(L_R__RT_LA___A_L__RA_LT, T_A, RT_LA, L_R)
#         F = abs(w1 - 1) + abs(w2 - 1) + abs(w3 - 1) + abs(v1 - v3) + abs(v1 * v2 - 1) + abs(v4 - v1 - 1)
