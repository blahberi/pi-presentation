import color_schemes
from color_schemes import gruvbox
import fonts
from manim import *
from manim_revealjs import PresentationScene


class Slide2(PresentationScene):
    def construct(self):
        color_schemes.set_theme(self, gruvbox)
        fonts.set_font()

        title = Tex(r"What is $\pi$?", color = gruvbox.SECONDARY).scale(2)
        self.add(title)

        self.play(title.animate.to_edge(UP, buff=0.5), run_time=1)
        
        circle = Circle(color=gruvbox.FG, stroke_width=3, radius=1).scale(2).to_edge(RIGHT, buff=1)
        diameter = Line(circle.get_left(), circle.get_right(), color=gruvbox.PRIMARY, stroke_width=3)
        d = Tex(r"$d$", color = gruvbox.PRIMARY).next_to(diameter, DOWN, buff=0.1)
        dg = VGroup(diameter, d)
        text = Tex(r"$\pi$ is the ratio of a circle's \\ circumference to its diameter.", color = gruvbox.FG).scale(1).to_edge(LEFT, buff=0.5)

        self.play(
            LaggedStart(
                Create(circle),
                AnimationGroup(
                    Create(diameter),
                    Write(d)
                ),
                lag_ratio=0.3
            ),
            Write(text)
        )

        self.end_fragment()

        dg2 = dg.copy().move_to(ORIGIN).to_edge(DOWN, buff=1)
        self.play(TransformFromCopy(dg, dg2))

        self.end_fragment()

        dgc = dg2.copy().set_z_index(1)
        dgc[0].scale(PI).to_edge(LEFT).set_color(gruvbox.SECONDARY)
        dgc[1].become(Tex(r"$\pi d$", color = gruvbox.SECONDARY).next_to(dgc[0], DOWN, buff=0.1))
        self.play(Transform(dg2, dgc), run_time=1)

        self.end_fragment()

        self.play(Transform(dg2[0], circle.copy().set_color(gruvbox.SECONDARY)), dg2[1].animate.next_to(circle, DOWN, buff=0.1), run_time=2)

        self.end_fragment()

        formula = MathTex(r"C = \pi d", color = gruvbox.CYAN).scale(1.5).next_to(text, DOWN, buff=0.5)
        self.play(Write(formula[0][:2]), Transform(dg2[1][0].copy(), formula[0][2:]), run_time=1)

        self.end_fragment()