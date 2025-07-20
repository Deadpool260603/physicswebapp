
from manim import *
import numpy as np

class UserFunctionPlot(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-5.0, 5.0],
            y_range=[-5.0, 5.0],
            axis_config={"include_tip": True}
        )
        self.play(Create(axes))

        # Display LaTeX version
        
        latex_label = MathTex(r"f(x) = \exp(-x)")
        latex_label.to_corner(UL)
        self.play(Write(latex_label))

        try:
            func = lambda x: eval("np.exp(-x)", {"np": np, "x": x})
            graph = axes.plot(func, color=BLUE)
            self.play(Create(graph), run_time=2)
            self.wait(1)
        except Exception as e:
            error_text = Text("Error in function:\n" + str(e), color=RED).scale(0.5)
            error_text.next_to(latex_label, DOWN)
            self.play(Write(error_text))
            self.wait(2)
