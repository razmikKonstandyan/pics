# -*- coding: utf-8 -*-
import numpy as np
from geometry import Point


def get_lines_intersection_point(first_line, second_line):
    a = np.array([[-first_line.k, 1], [-second_line.k, 1]])
    b = np.array([first_line.b, second_line.b])
    return Point(*np.linalg.solve(a, b))


