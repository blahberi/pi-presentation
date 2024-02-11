from gruvbox_manim import gruvbox, font
from manim import *
import numpy as np
from utils import *
from manim_revealjs import PresentationScene

def write_row(scene, row):
    scene.play(*[Write(cell.set_opacity(1)) for cell in row])

class Slide4(PresentationScene):
    def construct(self):
        title = Tex(r"Ancient Approximations of $\pi$", color=gruvbox.SECONDARY).scale(2)
        self.add(title)

        self.play(title.animate.to_edge(UP, buff=0.5))
        cols = [Tex("Who"), Tex("Approximation"), Tex("Absolute Error"), Tex("Relative Error")]
        rows = [
            [Tex("The Bible"), Tex(r"$\pi \approx 3$"), Tex(r"$0.141$"), Tex(r"$4.5\%$")],
            [Tex("India"), Tex(r"$\pi \approx (9785/11136)^2 = 3.088...$"), Tex(r"$0.053$"), Tex(r"$1.7\%$")],
            [Tex("Egypt"), Tex(r"$\pi \approx (16/9) = 3.16...$"), Tex(r"$0.02$"), Tex(r"$0.6\%$")],
            [Tex("Babylon"), Tex(r"$\pi \approx 3 + 1/8 = 3.125$"), Tex(r"$0.017$"), Tex(r"$0.53\%$")],
            [Tex("Ancient Greece"), Tex(r"$\pi \approx \sqrt{2} + \sqrt{3} = 3.146...$"), Tex(r"$0.004$"), Tex(r"$0.13\%$")]
        ]

        table = MobjectTable(rows, col_labels=cols, include_background_rectangle=True, background_rectangle_color=gruvbox.BG0H, line_config={"color": gruvbox.FG, "stroke_width": 3}, include_outer_lines=True).scale(0.5)

        for row in rows:
            for cell in row:
                cell.set_opacity(0)
                
        self.play(DrawBorderThenFill(table))
        self.end_fragment()
        
        # the bible
        write_row(self, rows[0][:1])
        self.end_fragment()
        text_str = [
            "And he made a molten sea of ten cubits", 
            "from brim to brim, ..., and a line of 30 cubits", 
            "did compass it round about. (1 Kings 7:23)"
        ]
        text = VGroup(*[Text(string, color=gruvbox.FG) for string in text_str]).arrange(DOWN, buff=SMALL_BUFF, aligned_edge=LEFT).scale(0.4).to_edge(LEFT, buff=0.5).shift(UP)

        self.play(FadeIn(text), table.animate.scale(0.35/0.5).to_edge(RIGHT))
        self.end_fragment()

        circle = Circle(color=gruvbox.FG, stroke_width=3, radius=1).scale(2).next_to(text, DOWN, buff=0.3)
        self.play(Create(circle))
        self.end_fragment()

        diameter = Line(circle.get_left(), circle.get_right(), color=gruvbox.PRIMARY, stroke_width=3)
        d = Tex(r"$10$", color=gruvbox.PRIMARY).next_to(diameter, DOWN, buff=0.25)
        self.play(Create(diameter), Write(d))
        self.end_fragment()

        circumference = circle.copy().set_color(gruvbox.PRIMARY)
        c = Tex(r"$30$", color=gruvbox.PRIMARY).next_to(circumference, RIGHT, buff=0.25)
        self.play(Create(circumference), Write(c))
        self.end_fragment()

        tex1 = Tex(r"$10\pi = 30$", color=gruvbox.SECONDARY)
        tex1[0][2].set_color(gruvbox.CYAN)
        tex2 = Tex(r"$\pi = \frac{30}{10}$", color=gruvbox.SECONDARY)
        tex2[0][0].set_color(gruvbox.CYAN)
        tex3 = Tex(r"$=3$", color=gruvbox.SECONDARY)
        tex1.next_to(circle, RIGHT, buff=LARGE_BUFF).shift(DOWN)
        tex2.move_to(tex1)
        tex3.next_to(tex2, RIGHT, buff=SMALL_BUFF)

        self.play(TransformFromCopy(d, tex1[0][:2]), TransformFromCopy(c, tex1[0][4:]), Write(tex1[0][2:4]))
        self.end_fragment()
        self.play(
            Transform(tex1[0][:2], tex2[0][5:]), 
            Transform(tex1[0][2], tex2[0][0]),
            Transform(tex1[0][3], tex2[0][1]),
            Transform(tex1[0][4:], tex2[0][2:4]),
            Write(tex2[0][4])
        )
        self.play(Write(tex3))
        self.end_fragment()
        write_row(self, rows[0][1:])

        self.play(
            table.animate.scale(0.5/0.35).move_to(ORIGIN), 
            FadeOut(text), 
            FadeOut(circle), 
            FadeOut(diameter), 
            FadeOut(d), 
            FadeOut(circumference), 
            FadeOut(c), 
            FadeOut(tex1), 
            FadeOut(tex2), 
            FadeOut(tex3)
        )
        self.end_fragment()

        # india
        write_row(self, rows[1])
        self.end_fragment()

        # egypt
        write_row(self, rows[2])
        self.end_fragment()

        # babylon
        write_row(self, rows[3])
        self.end_fragment()

        # ancient greece
        write_row(self, rows[4])
        self.end_fragment()
