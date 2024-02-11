from manim import *
import numpy as np
from gruvbox_manim import gruvbox
import itertools as it


def darken_color(color, factor):
    rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    darkened_rgb = tuple(max(int(component * (1 - factor)), 0) for component in rgb)
    darkened_hex = '#%02x%02x%02x' % darkened_rgb
    return darkened_hex


def get_vertices(n, circle):
    return [circle.point_from_proportion(i/n) for i in range(n)]

def approximate_circle_inner(n, circle):
    return Polygon(*get_vertices(n, circle), color=gruvbox.PRIMARY, stroke_width=2)

def approximate_circle_outer(n, circle):
    r = circle.get_width()/2
    c = circle.get_center()
    vertices = [(c[0] + (r/np.cos(PI/n))*np.cos(2*PI*i/n + PI/n), c[1] + (r/np.cos(PI/n))*np.sin(2*PI*i/n + PI/n), 0) for i in range(n)]

    return Polygon(*vertices, color=gruvbox.PRIMARY, stroke_width=2)

def dissect_polygon(polygon, color=gruvbox.PRIMARY, stroke_width=1):
    return VGroup(*[Line(polygon.get_center(), polygon.get_vertices()[i], color=color, stroke_width=stroke_width) for i in range(len(polygon.get_vertices()))])

def dissect_circle(circle, n, color=gruvbox.FG, stroke_width=1):
    return VGroup(*[Line(circle.get_center(), circle.point_from_proportion(i/n), color=color, stroke_width=stroke_width) for i in range(n)])

def sector_dissect_circle(circle, n_slices=20, color=gruvbox.FG, fill_colors=[gruvbox.LIGHT_BLUE, darken_color(gruvbox.LIGHT_BLUE, 0.2)], fill_opacity=1, stroke_width=1):
    angle = TAU / n_slices
    sectors = VGroup(*(
        Sector(angle=angle, start_angle=i * angle, fill_color=c, fill_opacity=1)
        for i, c in zip(range(n_slices), it.cycle(fill_colors))
    ))
    sectors.set_stroke(color, stroke_width)
    sectors.replace(circle, stretch=True)
    return sectors

def draw_dissection(dissection):
    return AnimationGroup(*[Create(line) for line in dissection])

def draw_sector_dissection(dissection):
    return AnimationGroup(*[DrawBorderThenFill(sector) for sector in dissection])

def get_riemann_rectangles(axis, function, dx=0.5):
    rectangles = axis.get_riemann_rectangles(function, dx=dx, x_range=[-1, 1], stroke_color=gruvbox.BG, stroke_width=10*dx)
    start_color = ManimColor(gruvbox.LIGHT_BLUE)
    end_color = ManimColor(gruvbox.CYAN)
    for i, rect in enumerate(rectangles):
        rect.set_fill(color=interpolate_color(start_color, end_color, i/len(rectangles)))
    return rectangles