# -*- coding: utf-8 -*-


def get_figure(plt, title, figsize=(20, 10)):
    """ Plot configuration function"""
    plt.figure(figsize=figsize)
    plt.title(title, fontsize=18)
    plt.xlabel('x', fontsize=14)
    plt.ylabel('y', fontsize=14)
    return plt


def put_points(plt, points, color='ro', markersize=1, labels=None):
    """Put points on the plot with the labels"""
    x_points = [p.x for p in points]
    y_points = [p.y for p in points]
    plt.plot(x_points, y_points, color, markersize=markersize)
    if labels:
        for label, x, y in zip(labels, x_points, y_points):
            plt.annotate(label, xy=(x, y), xytext=(-20, 20), textcoords='offset points', ha='right', va='bottom',
                         bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                         arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    return plt
