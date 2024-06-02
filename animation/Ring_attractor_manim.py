from manim import *
import numpy as np
import os

config.frame_rate = 60

class RingAttractorAnimation(Scene):
    def setup(self):
        self.camera.background_color = WHITE

    def construct(self):

        activity_data = np.load(os.path.join('./simulation/data/','attractor_activations.npy'))
        n_cells = activity_data.shape[1]
        radius = 3  # Radius of the ring where neurons are placed

        # Create a ring of circles (balls) representing neurons, only every 5th neuron
        balls = VGroup(*[
            Circle(radius=0.4, stroke_color=BLACK, stroke_opacity=1, fill_opacity=0).move_to(
                radius * np.array([
                    np.cos(2 * np.pi * i / n_cells),
                    np.sin(2 * np.pi * i / n_cells),
                    0
                ])
            ) for i in range(0, n_cells, 5) 
        ])
        self.add(balls)


        step_size = 10 
        for step in range(0, len(activity_data), step_size):
            state = activity_data[step]
            animations = []
            for i, ball in enumerate(balls):
                index = i * 5 
                normalized_activity = state[index] / np.max(activity_data) if np.max(state) > 0 else 0
                color_intensity = normalized_activity 
                ball_color = interpolate_color(WHITE, RED, color_intensity)
                animations.append(ball.animate.set_fill(ball_color, opacity=1 if color_intensity > 0 else 0))

            # Play all animations together smoothly
            self.play(*animations, run_time=0.1, rate_func=smooth)

# To run this, use: manim -pql ./animation/Ring_attractor_manim.py RingAttractorAnimation
