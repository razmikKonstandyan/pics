# -*- coding: utf-8 -*-
import numpy as np
from geometry import Point


def get_lines_intersection_point(first_line, second_line):
    a = np.array([[-first_line.k, 1], [-second_line.k, 1]])
    b = np.array([first_line.b, second_line.b])
    return Point(*np.linalg.solve(a, b))


def get_wurf_value(p1, p2, p3, p4):
    # TODO Добавить проверку что они коллинеары
    a = ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5
    b = ((p3.x - p2.x) ** 2 + (p3.y - p2.y) ** 2) ** 0.5
    c = ((p4.x - p3.x) ** 2 + (p4.y - p3.y) ** 2) ** 0.5
    return float((a + b) * (b + c)) / float((b * (a + b + c)))
