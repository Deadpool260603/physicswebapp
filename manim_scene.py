from manim import *
class SinWave(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 10], y_range=[-1.5, 1.5], tips=True)
        graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        self.play(Create(axes), Create(graph))
        self.wait(1)