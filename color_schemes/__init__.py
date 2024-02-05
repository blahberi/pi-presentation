from manim import *


def set_theme(scene, theme, extra=False):
    scene.camera.background_color = theme.BG
    if extra:
        scene.camera.background_color = theme.BG_FILL
    Text.set_default(color=theme.FG)
    Tex.set_default(color=theme.FG)
    MathTex.set_default(color=theme.FG)
    DecimalNumber.set_default(color=theme.FG)
