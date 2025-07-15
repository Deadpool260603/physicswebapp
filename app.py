from flask import Flask, render_template, request
import subprocess
import shutil
import os
import re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index1.html")

@app.route("/generate", methods=["POST"])
def generate():
    user_function = request.form.get("question")
    x_min = float(request.form.get("x_min", -5))
    x_max = float(request.form.get("x_max", 5))
    y_min = float(request.form.get("y_min", -5))
    y_max = float(request.form.get("y_max", 5))

    # Convert to LaTeX-safe expression
    latex_expr = convert_to_latex(user_function)

    # Write the dynamic Manim script
    with open("manim1.py", "w") as f:
        f.write(generate_manim_code(user_function, latex_expr, x_min, x_max, y_min, y_max))

    # Run Manim to generate video
    subprocess.run(["manim", "-ql", "manim1.py", "UserFunctionPlot"])

    # Copy video to static folder
    source_path = "media/videos/manim1/480p15/UserFunctionPlot.mp4"
    dest_path = os.path.join("static", "user_plot.mp4")
    shutil.copy(source_path, dest_path)

    return render_template("result1.html", question=user_function, video_path="user_plot.mp4")

# converts user input to LaTeX
def convert_to_latex(expr):
    expr = expr.replace("**", "^")
    expr = re.sub(r"\^(\d+|\w+)", r"^{\1}", expr)

    replacements = {
        "np.": "",
        "sin": r"\sin",
        "cos": r"\cos",
        "tan": r"\tan",
        "log": r"\log",
        "exp": r"\exp",
        "sqrt": r"\sqrt",
        "*": r"\cdot ",
    }
    for k, v in replacements.items():
        expr = expr.replace(k, v)
    expr = re.sub(r"(?<!\\)frac", r"\\frac", expr)
    expr = re.sub(r"(\w+|\(.+?\))/(\w+)", r"\\frac{\1}{\2}", expr)
    return expr

# generates the manim1.py script
def generate_manim_code(user_function, latex_expr, x_min, x_max, y_min, y_max):
    def preprocess_function(expr):
        expr = expr.replace("^", "**")
        function_names = ['sin', 'cos', 'tan', 'log', 'exp', 'sqrt']
        for func in function_names:
            expr = re.sub(rf'\b{func}\b', f'np.{func}', expr)
        return expr

    safe_func = preprocess_function(user_function).replace('"', '\\"')
    return f'''
from manim import *
import numpy as np

class UserFunctionPlot(Scene):
    def construct(self):
        axes = Axes(
            x_range=[{x_min}, {x_max}],
            y_range=[{y_min}, {y_max}],
            axis_config={{"include_tip": True}}
        )
        self.play(Create(axes))

        # Display LaTeX version
        
        latex_label = MathTex(r"f(x) = {latex_expr}")
        latex_label.to_corner(UL)
        self.play(Write(latex_label))

        try:
            func = lambda x: eval("{safe_func}", {{"np": np, "x": x}})
            graph = axes.plot(func, color=BLUE)
            self.play(Create(graph), run_time=2)
            self.wait(1)
        except Exception as e:
            error_text = Text("Error in function:\\n" + str(e), color=RED).scale(0.5)
            error_text.next_to(latex_label, DOWN)
            self.play(Write(error_text))
            self.wait(2)
'''

if __name__ == "__main__":
    app.run(debug=True)
