from manim import *
import numpy as np
from color_schemes import gruvbox


def get_vertices(n, circle):
    return [circle.point_from_proportion(i/n) for i in range(n)]

def approximate_circle_inner(n, circle):
    return Polygon(*get_vertices(n, circle), color=gruvbox.PRIMARY, stroke_width=2)

def approximate_circle_outer(n, circle):
    r = circle.get_width()/2
    c = circle.get_center()
    vertices = [(c[0] + (r/np.cos(PI/n))*np.cos(2*PI*i/n + PI/4), c[1] + (r/np.cos(PI/n))*np.sin(2*PI*i/n + PI/4), 0) for i in range(n)]

    return Polygon(*vertices, color=gruvbox.PRIMARY, stroke_width=2)


def dissect_polygon(polygon):
    return VGroup(*[Line(polygon.get_center(), polygon.get_vertices()[i], color=gruvbox.PRIMARY, stroke_width=1) for i in range(len(polygon.get_vertices()))])

def dissect_circle(circle, n):
    return VGroup(*[Line(circle.get_center(), circle.point_from_proportion(i/n), color=gruvbox.PRIMARY, stroke_width=1) for i in range(n)])

def draw_dissection(dissection):
    return AnimationGroup(*[Create(line) for line in dissection])

def get_riemann_rectangles(axis, function, dx=0.5):
    rectangles = axis.get_riemann_rectangles(function, dx=dx, x_range=[-1, 1], stroke_color=gruvbox.BG, stroke_width=10*dx)
    start_color = ManimColor(gruvbox.LIGHT_BLUE)
    end_color = ManimColor(gruvbox.CYAN)
    for i, rect in enumerate(rectangles):
        rect.set_fill(color=interpolate_color(start_color, end_color, i/len(rectangles)))
    return rectangles