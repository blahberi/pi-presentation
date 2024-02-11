from gruvbox_manim import gruvbox
from manim import *
from manim_revealjs import PresentationScene, LOOP
import numpy as np
from utils import *

def interpolate_time(min_time, max_time, min_val, max_val, val):
    return (val - min_val)/(max_val - min_val)*(max_time - min_time) + min_time

class Slide1(PresentationScene):
    def construct(self):
        circle1 = Circle(stroke_width=3, radius=1).scale(2).to_corner(DR)
        self.add(circle1)

        n1 = 6
        inner_polygon = approximate_circle_inner(n1, circle1)
        dissection = dissect_polygon(inner_polygon)
        outer_polygon = approximate_circle_outer(n1, circle1)


        dx = 0.15
        axis = Axes(color=gruvbox.FG, x_range=[-1.25, 1.25], y_range=[-0.5, 1.25], x_length=abs(1.25-(-1.25)), y_length=abs(1.25-(-0.5)), axis_config={"color": gruvbox.FG, "stroke_width": 2}, tips=False).scale(2).to_corner(UL)
        circle2 = axis.plot(lambda x: np.sqrt(1 - x**2), x_range=[-1, 1, 0.001], color=gruvbox.FG, stroke_width=2, use_smoothing=False)
        reimann_rects = get_riemann_rectangles(axis, circle2, dx)

        self.add(inner_polygon)
        self.add(dissection)
        self.add(outer_polygon)
        self.add(axis)
        self.add(circle2)
        self.add(reimann_rects)

        text = Text("The history of", color = gruvbox.FG).scale(2).to_corner(UR, buff=1).shift(0.5*RIGHT)
        pi = Tex(r"$\pi$", color = gruvbox.YELLOW).scale(10)

        ramanujan = MathTex(r" = \left(12 \sum_{k=0}^{\infty} \frac{(-1)^k (6k)! (545140134k + 13591409)}{(3k)!(k!)^3 640320^{3k + \frac{3}{2}}}\right)^{-1}", color = gruvbox.FG).scale(0.75).to_corner(DL, buff=1).to_edge(LEFT, buff=0.5)
        credits = Tex("A presentation by Eitan H. celebrating $\pi$ day 2024", color = gruvbox.PRIMARY).scale(0.5).next_to(ramanujan, DOWN, buff=0.5)


        self.add(text)
        self.add(pi)
        self.add(ramanujan)
        self.add(credits)
        for n, dx in zip([8, 10, 16, 20, 30, 50, 100, 6], [0.1, 0.05, 0.03, 0.01, 0.005, 0.003, 0.001, 0.15]):
            next_inner_polygon = approximate_circle_inner(n, circle1)
            next_dissection = dissect_polygon(next_inner_polygon) 
            next_outer_polygon = approximate_circle_outer(n, circle1)
            
            angle = PI
            time = 0.5

            always_rotate(inner_polygon, rate=angle/time)
            always_rotate(next_inner_polygon, rate=angle/time)
            always_rotate(dissection, rate=angle/time)
            always_rotate(next_dissection, rate=angle/time)
            always_rotate(outer_polygon, rate=angle/time)
            always_rotate(next_outer_polygon, rate=angle/time)

            self.play(Transform(inner_polygon, next_inner_polygon), Transform(dissection, next_dissection), Transform(outer_polygon, next_outer_polygon), run_time=time + 0.01, rate_func=linear)
            
            inner_polygon.clear_updaters()
            next_inner_polygon.clear_updaters()
            dissection.clear_updaters()
            next_dissection.clear_updaters()
            outer_polygon.clear_updaters()

            inner_polygon.rotate(-angle)
            dissection.rotate(-angle)
            outer_polygon.rotate(-angle)
            
            loc = 0.1
            scale = 0.1
            wait = np.random.normal(loc, scale)
            wait = max(loc - scale, min(loc + scale, wait))
            self.wait(wait)
            self.play(Transform(reimann_rects, get_riemann_rectangles(axis, circle2, dx)), run_time=time)

            self.wait(1)
        self.end_fragment(fragment_type=LOOP)
