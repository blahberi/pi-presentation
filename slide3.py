import color_schemes
from color_schemes import gruvbox
import fonts
from manim import *
import numpy as np
from utils import *
from manim_revealjs import PresentationScene


class Slide3(PresentationScene):
    def construct(self):
        color_schemes.set_theme(self, gruvbox)
        fonts.set_font()

        title = Tex(r"What about the area?", color = gruvbox.PRIMARY).scale(2)
        self.add(title)


        circle = Circle(color=gruvbox.FG, fill_color=gruvbox.SECONDARY, fill_opacity=0.5, stroke_width=3, radius=1).scale(2)
        self.play(title.animate.to_edge(UP, buff=0.5), run_time=1)
        self.play(DrawBorderThenFill(circle))
        self.end_fragment()


        n = 8
        sectors = sector_dissect_circle(circle, n, stroke_width=2).set_opacity(0)
        dissection = dissect_circle(circle, n, stroke_width=2)
        self.play(draw_dissection(dissection))
        self.add(sectors)
        self.play(sectors.animate.set_opacity(1), circle.animate.set_opacity(0))
        self.remove(*dissection)
        self.end_fragment()


        group = VGroup(circle, sectors)
        laid_sectors = sectors.copy()
        dtheta = TAU/n
        angles = np.arange(0, TAU, dtheta)
        for sector, angle in zip(laid_sectors, angles):
            sector.rotate(-90*DEGREES - angle - dtheta/2, about_point=circle.get_center())
        laid_sectors.arrange(RIGHT, buff=0, aligned_edge=DOWN)
        laid_sectors.scale(0.5).to_edge(RIGHT, buff=0.75)
        self.play(group.animate.to_edge(LEFT, buff=1))
        self.play(TransformFromCopy(sectors, laid_sectors), run_time=2)
        self.wait(1)
        self.end_fragment()


        lh, rh = VGroup(*laid_sectors[:n // 2]), VGroup(*laid_sectors[n // 2:])
        d = circle.get_width()*(1-np.cos(PI/n))/8
        lh.generate_target()
        rh.generate_target()
        rh.target.rotate(PI).shift(lh.get_width()*LEFT/2)
        lh.target.move_to(rh.target).shift(LEFT*rh[0].get_width()/2 + (0.5 + d)*DOWN)
        rh.target.shift((0.5 + d)*UP)
        self.play(MoveToTarget(lh), MoveToTarget(rh, path_arc=PI), run_time=2)
        self.wait(0.5)
        self.play(lh.animate.shift(0.5*UP), rh.animate.shift(0.5*DOWN))
        rectangle = VGroup(lh, rh)
        self.play(rectangle.animate.scale(2))
        self.end_fragment()


        for n in [16, 32, 64, 128, 256]:
            new_sectors = sector_dissect_circle(circle, n, stroke_width=16/n)

            laid_sectors  = new_sectors.copy()
            dtheta = TAU/n
            angles = np.arange(0, TAU, dtheta)
            
            for sector, angle in zip(laid_sectors, angles):
                sector.rotate(-90*DEGREES - angle - dtheta/2, about_point=circle.get_center())

            laid_sectors.scale(0.5).arrange(RIGHT, buff=0, aligned_edge=DOWN)
            laid_sectors.to_edge(RIGHT, buff=0.75)

            next_lh, next_rh = VGroup(*laid_sectors[:n // 2]), VGroup(*laid_sectors[n // 2:])
            d = circle.get_width()*(1-np.cos(PI/n))/8
            next_rh.rotate(PI).shift(next_lh.get_width()*LEFT/2)
            next_lh.move_to(next_rh).shift(LEFT*next_rh[0].get_width()/2 + (d*DOWN))
            next_rh.shift(d*UP)
            VGroup(next_lh, next_rh).scale(2)
            self.play(Transform(sectors, new_sectors), Transform(lh, next_lh), Transform(rh, next_rh))
            self.wait(0.5)
        self.end_fragment()
        
        
        rectangle = VGroup(lh, rh)
        next_rectangle = Rectangle(width=PI*circle.get_width()/2, height=circle.get_width()/2, fill_color=darken_color(gruvbox.SECONDARY, 0.2), fill_opacity=1, stroke_width=0).move_to(rectangle)
        circle.set_fill(color=darken_color(gruvbox.SECONDARY, 0.2)).set_stroke(width=0)
        self.play(FadeTransform(rectangle, next_rectangle), sectors.animate.set_opacity(0), circle.animate.set_opacity(1))
        rectangle = next_rectangle
        self.end_fragment()
        

        base = Line(rectangle.get_corner(DL), rectangle.get_corner(DR), color=gruvbox.PRIMARY, stroke_width=4)
        self.play(Create(base))
        self.end_fragment()
        

        halfcircle = ArcBetweenPoints(circle.get_left(), circle.get_right(), angle=PI, color=gruvbox.PRIMARY, stroke_width=4)
        self.play(TransformFromCopy(base, halfcircle), run_time=2)
        self.end_fragment()
        

        base_text = Tex(r"$\pi r$", color=gruvbox.PRIMARY).next_to(base, DOWN, buff=0.3)
        self.play(Write(base_text))
        self.end_fragment()


        height = Line(rectangle.get_corner(UL), rectangle.get_corner(DL), color=gruvbox.PRIMARY, stroke_width=4)
        self.play(Create(height), FadeOut(halfcircle))
        self.end_fragment()


        radius = Line(circle.get_center(), circle.get_right(), color=gruvbox.PRIMARY, stroke_width=4)
        self.play(TransformFromCopy(height, radius), run_time=2)
        self.end_fragment()


        height_text = Tex(r"$r$", color=gruvbox.PRIMARY).next_to(height, LEFT, buff=0.3)
        self.play(Write(height_text))
        self.end_fragment()


        formula = Tex(r"$A = r \cdot \pi r = \pi r^2$", color=gruvbox.CYAN).to_edge(DOWN, buff=1)
        formula2 = Tex(r"$A = \pi r^2$", color=gruvbox.CYAN).move_to(formula)
        self.play(FadeOut(radius), Write(formula[0][:2]), TransformFromCopy(height_text, formula[0][2]), Write(formula[0][3]), TransformFromCopy(base_text, formula[0][4:6]))
        self.end_fragment()


        self.play(Write(formula[0][6:]))
        self.play(Transform(formula[0][:2], formula2[0][:2]), Transform(formula[0][7:], formula2[0][2:]), FadeOut(formula[0][2:7]))
        self.end_fragment()