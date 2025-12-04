from manim import *
import numpy as np
import math

def taylor_polynomial(f, x0, degree):
    """Return numerical Taylor polynomial of f around x0."""
    def p(x):
        s = 0
        for n in range(degree + 1):
            # For e^x, all derivatives at x0 equal e^x0
            s += (f(x0) * (x - x0)**n) / math.factorial(n)
        return s
    return p


class TaylorToMaclaurin(Scene):
    def construct(self):

        # Function f(x) = e^x
        f = lambda x: np.exp(x)

        # Axes (labels removed to avoid LaTeX)
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 8, 1],
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
            tips=False
        )

        axes_labels = VGroup(
            Text("x").next_to(axes.x_axis.get_end(), RIGHT),
            Text("y").next_to(axes.y_axis.get_end(), UP)
        )

        self.play(Create(axes), FadeIn(axes_labels))
        self.wait(0.5)

        # Real function plot
        graph_f = axes.plot(f, color=YELLOW)
        label_f = Text("f(x) = e^x", font_size=28).to_corner(UL).set_color(YELLOW)

        self.play(Create(graph_f), FadeIn(label_f))
        self.wait(1)

        # Starting Taylor expansion point
        x0 = 1
        dot = Dot(axes.c2p(x0, f(x0)), color=RED)
        txt = Text("Center x₀ = 1", font_size=28, color=RED).to_corner(UR)

        self.play(FadeIn(dot), FadeIn(txt))
        self.wait(0.5)

        # Show Taylor approximations at x0 = 1
        for deg in range(1, 6):
            p = taylor_polynomial(f, x0, deg)
            graph_p = axes.plot(p, color=BLUE)
            label_p = Text(f"T{deg}(x)", font_size=24, color=BLUE).next_to(axes, DOWN)

            self.play(Create(graph_p), FadeIn(label_p))
            self.wait(0.7)
            self.play(FadeOut(graph_p), FadeOut(label_p))

        # Move to Maclaurin (x0 = 0)
        new_x0 = 0
        self.play(
            dot.animate.move_to(axes.c2p(new_x0, f(new_x0))),
            txt.animate.become(Text("Center x₀ = 0 (Maclaurin)", font_size=28, color=RED).to_corner(UR)),
            run_time=2
        )
        self.wait(0.5)

        # Show Maclaurin approximations
        for deg in range(1, 6):
            p = taylor_polynomial(f, 0, deg)
            graph_p = axes.plot(p, color=GREEN)
            label_p = Text(f"M{deg}(x)", font_size=24, color=GREEN).next_to(axes, DOWN)

            self.play(Create(graph_p), FadeIn(label_p))
            self.wait(0.7)
            self.play(FadeOut(graph_p), FadeOut(label_p))

        self.wait(1)
