from manim import *
import numpy as np

class PlotXPower8(Scene):
    def construct(self):
        # Set up axes
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-1, 300, 50],
            x_length=7,
            y_length=5,
            axis_config={"include_tip": True}
        )

        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        self.play(Create(axes), Write(labels))

        # LaTeX label
        func_label = MathTex("f(x) = x^8")
        func_label.to_corner(UL)
        self.play(Write(func_label))

        # Define function and plot
        def func(x):
            return x ** 8

        graph = axes.plot(func, color=BLUE)
        self.play(Create(graph), run_time=2)
        self.wait(1)
