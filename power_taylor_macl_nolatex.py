from manim import *
import numpy as np
import random
import math

# -------------------------------------------------------------
# Helper: arbitrary power series (with random coefficients)
# -------------------------------------------------------------
def random_power_series(a, degree):
    coeffs = [random.uniform(-1, 1) for _ in range(degree + 1)]
    def p(x):
        s = 0
        for n, c in enumerate(coeffs):
            s += c * (x - a)**n
        return s
    return p, coeffs


# -------------------------------------------------------------
# Helper: Taylor polynomial of e^x
# -------------------------------------------------------------
def taylor_poly_ex(a, degree):
    def p(x):
        s = 0
        for n in range(degree + 1):
            s += (np.exp(a) * (x - a)**n) / math.factorial(n)
        return s
    return p


class PowerTaylorMac(Scene):
    def construct(self):

        # f(x) = e^x
        f = lambda x: np.exp(x)

        # Axes without LaTeX labels
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 10, 1],
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
            tips=False
        )

        axes_labels = VGroup(
            Text("x").next_to(axes.x_axis.get_end(), RIGHT),
            Text("y").next_to(axes.y_axis.get_end(), UP)
        )

        self.play(Create(axes), FadeIn(axes_labels))

        # ---------------------------------------------------------
        # 1. General power series: random coefficients
        # ---------------------------------------------------------
        degree = 5
        a = 1  # center for power series
        power_func, coeffs = random_power_series(a, degree)

        graph_power = axes.plot(power_func, color=PURPLE)
        label_power = Text("General Power Series", font_size=32, color=PURPLE).to_corner(UL)

        self.play(Create(graph_power), FadeIn(label_power))
        self.wait(1)

        # Mark center point
        center_dot = Dot(axes.c2p(a, power_func(a)), color=RED)
        center_text = Text("Center a = 1", font_size=24, color=RED).to_corner(UR)

        self.play(FadeIn(center_dot), FadeIn(center_text))
        self.wait(0.5)

        # ---------------------------------------------------------
        # 2. Transition to Taylor series of e^x
        # ---------------------------------------------------------
        label_taylor = Text("Taylor Series of e^x at a = 1", font_size=30, color=BLUE).to_corner(UL)

        # Fade out power-series label; fade in Taylor label
        self.play(
            FadeOut(label_power),
            FadeIn(label_taylor)
        )

        # Replace random power series graph with Taylor polynomial graph
        taylor_func = taylor_poly_ex(a, degree)
        graph_taylor = axes.plot(taylor_func, color=BLUE)

        self.play(Transform(graph_power, graph_taylor))  # overwrite graph_power
        self.wait(1)

        # ---------------------------------------------------------
        # 3. Move center a = 1 to a = 0 (Maclaurin)
        # ---------------------------------------------------------
        label_mac = Text("Maclaurin Series (a = 0)", font_size=30, color=GREEN).to_corner(UL)

        self.play(
            center_dot.animate.move_to(axes.c2p(0, f(0))),
            center_text.animate.become(Text("Center a = 0", font_size=24, color=RED).to_corner(UR)),
            FadeOut(label_taylor),
            FadeIn(label_mac),
            run_time=2
        )
        self.wait(0.7)

        # New Taylor polynomial centered at 0
        mac_func = taylor_poly_ex(0, degree)
        graph_mac = axes.plot(mac_func, color=GREEN)

        self.play(Transform(graph_power, graph_mac))  # same graph morphs
        self.wait(1)

        # Final display
        self.wait(2)
