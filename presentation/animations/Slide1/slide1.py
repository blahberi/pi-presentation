import color_schemes
from color_schemes import gruvbox
import fonts
from manim import *
from manim_revealjs import PresentationScene, LOOP
import random
import numpy as np
from utils import *


def interpolate_time(min_time, max_time, min_val, max_val, val):
    return (val - min_val)/(max_val - min_val)*(max_time - min_time) + min_time


class Slide1(PresentationScene):
    def construct(self):
        color_schemes.set_theme(self, gruvbox)
        fonts.set_font()

        circle1 = Circle(color=gruvbox.FG, stroke_width=3, radius=1).scale(2).to_corner(DR)
        self.add(circle1)

        n1 = 6
        polygon = approximate_circle_inner(n1, circle1)
        dissection = dissect_polygon(polygon)

        dx = 0.15
        axis = Axes(color=gruvbox.FG, x_range=[-1.25, 1.25], y_range=[-0.5, 1.25], x_length=abs(1.25-(-1.25)), y_length=abs(1.25-(-0.5)), axis_config={"color": gruvbox.FG, "stroke_width": 2}, tips=False).scale(2).to_corner(UL)
        circle2 = axis.plot(lambda x: np.sqrt(1 - x**2), x_range=[-1, 1, 0.001], color=gruvbox.FG, stroke_width=2, use_smoothing=False)
        reimann_rects = get_riemann_rectangles(axis, circle2, dx)

        self.add(polygon)
        self.add(dissection)
        self.add(axis)
        self.add(circle2)
        self.add(reimann_rects)

        text = Text("The history of", color = gruvbox.FG).scale(2).to_corner(UR, buff=1).shift(0.5*RIGHT)
        pi = Tex(r"$\pi$", color = gruvbox.YELLOW).scale(10)

        ramanujan = MathTex(r" = \frac{1}{\frac{2\sqrt{2}}{9801} \sum_{k=0}^{\infty} \frac{(4k)!(1103+26390k)}{(k!)^4 396^{4k}}}", color = gruvbox.FG).scale(1).to_corner(DL, buff=1).shift(0.5*RIGHT)
        credits = Tex("A presentation by Eitan H. celebrating $\pi$ day 2024", color = gruvbox.PRIMARY).scale(0.5).next_to(ramanujan, DOWN, buff=0.5)


        self.add(text)
        self.add(pi)
        self.add(ramanujan)
        self.add(credits)
        
        for n, dx in zip([10, 8, 6, 12, 8, 10, 8, 6], [0.1, 0.05, 0.03, 0.01, 0.005, 0.003, 0.001, 0.15]):
            next_polygon = approximate_circle_inner(n, circle1)
            next_dissection = dissect_polygon(next_polygon)
            
            direction = 1 if n > n1 else -1
            angle = direction*int(n/1.5)*2*PI/n
            time = 0.5 + interpolate_time(0.0, 0.1, 2, 6, abs(n1 - n))

            always_rotate(polygon, rate=angle/time)
            always_rotate(next_polygon, rate=angle/time)
            always_rotate(dissection, rate=angle/time)
            always_rotate(next_dissection, rate=angle/time)

            self.play(Transform(polygon, next_polygon), Transform(dissection, next_dissection), run_time=time + 0.01, rate_func=linear)
            
            polygon.clear_updaters()
            next_polygon.clear_updaters()
            dissection.clear_updaters()
            next_dissection.clear_updaters()

            polygon.rotate(-angle)
            dissection.rotate(-angle)
            
            loc = 0.1
            scale = 0.1
            wait = np.random.normal(loc, scale)
            wait = max(loc - scale, min(loc + scale, wait))
            self.wait(wait)
            self.play(Transform(reimann_rects, get_riemann_rectangles(axis, circle2, dx)), run_time=time)

            self.wait(1)
            n1 = n
        self.end_fragment(fragment_type=LOOP)
