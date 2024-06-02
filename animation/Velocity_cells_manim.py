from manim import *
import numpy as np
import os

config.frame_rate = 60

class RingAttractorAnimation(Scene):
    def setup(self):
        # Set the background color to white
        self.camera.background_color = WHITE

    def construct(self):
        # Load activity data
        activity_data = np.load(os.path.join('./simulation/data/','velocity_activations.npy'))
        activity_data_ec = np.load(os.path.join('./simulation/data/','velocity_activations_ec.npy'))
        activity_data_wc = np.load(os.path.join('./simulation/data/','velocity_activations_wc.npy'))

        # Constants for visualization
        n_cells = activity_data.shape[1]
        radius = 1.8  # Radius for the main ring
        ec_radius = 2.4  # Radius for the EC and WC rings
        wc_radius = 2.8  # Radius for the EC and WC rings

        # Create a ring of circles for main neurons, only every 5th neuron
        balls = VGroup(*[
            Circle(radius=0.25, stroke_color=BLACK, stroke_opacity=1, fill_opacity=0).move_to(
                radius * np.array([
                    np.cos(2 * np.pi * i / n_cells),
                    np.sin(2 * np.pi * i / n_cells),
                    0
                ])
            ) for i in range(0, n_cells, 5)
        ])
        self.add(balls)

        # Create rings for east and west velocity-sensitive cells
        balls_ec = VGroup(*[
            Circle(radius=0.15, stroke_color=GREEN, stroke_width=6, stroke_opacity=1, fill_opacity=0).move_to(
                ec_radius * np.array([
                    np.cos(2 * np.pi * i / n_cells),
                    np.sin(2 * np.pi * i / n_cells),
                    0
                ])
            ) for i in range(0, n_cells, 5)
        ])
        balls_wc = VGroup(*[
            Circle(radius=0.15, stroke_color=BLUE, stroke_width=6, stroke_opacity=1, fill_opacity=0).move_to(
                wc_radius * np.array([
                    np.cos(2 * np.pi * i / n_cells),
                    np.sin(2 * np.pi * i / n_cells),
                    0
                ])
            ) for i in range(0, n_cells, 5)
        ])
        self.add(balls_ec, balls_wc)

        # Additional balls for east and west movement
        east_ball = Circle(radius=0.3, stroke_color=GREEN, stroke_width=6, fill_opacity=0)
        west_ball = Circle(radius=0.3, stroke_color=BLUE, stroke_width=6, fill_opacity=0)
        east_ball.move_to(wc_radius * np.array([np.cos(1/4*np.pi), np.sin(1/4*np.pi), 0]) + RIGHT * 2) 
        west_ball.move_to(wc_radius * np.array([np.cos(3/4*np.pi), np.sin(3/4*np.pi), 0]) + LEFT * 2) 
        self.add(east_ball, west_ball)

        # Line along which the mouse moves
        movement_line = Line(LEFT * 4 + DOWN * 3.5, RIGHT * 4 + DOWN * 3.5, color=GRAY, stroke_opacity=0.7)
        self.add(movement_line)

        # Create the mouse as a brown ball
        mouse = Circle(radius=0.2, stroke_color=GREY_BROWN, fill_color=GREY_BROWN, fill_opacity=1)
        mouse_start = LEFT * 4 + DOWN * 3.5
        mouse.move_to(mouse_start)
        self.add(mouse)

        # Animate activity in all rings
        step_size = 10 
        for step in range(0, len(activity_data), step_size):
            state = activity_data[step]
            state_ec = activity_data_ec[step]
            state_wc = activity_data_wc[step]
            animations = []
            if np.any(state_ec > 0):
                current_x = mouse.get_center()[0]
                new_x = current_x + 0.02
                mouse.move_to(np.array([new_x, mouse.get_center()[1], 0]))
                east_ball.set_fill(color=RED, opacity=1)
        
            for i, (ball, ball_ec, ball_wc) in enumerate(zip(balls, balls_ec, balls_wc)):
                index = i * 5 if i < len(balls) else i 
                normalized_activity = state[index] / np.max(activity_data) if np.max(state) > 0 else 0
                normalized_activity_ec = state_ec[index] / np.max(activity_data_ec) if np.max(state_ec) > 0 else 0
                normalized_activity_wc = state_wc[index] / np.max(activity_data_wc) if np.max(state_wc) > 0 else 0

                ball_color = interpolate_color(WHITE, RED, normalized_activity)
                ec_color = interpolate_color(WHITE, RED, normalized_activity_ec)
                wc_color = interpolate_color(WHITE, RED, normalized_activity_wc)

                animations.extend([
                    ball.animate.set_fill(ball_color, opacity=1 if normalized_activity > 0 else 0),
                    ball_ec.animate.set_fill(ec_color, opacity=1 if normalized_activity_ec > 0 else 0),
                    ball_wc.animate.set_fill(wc_color, opacity=1 if normalized_activity_wc > 0 else 0)
                ])
            # Play all animations together smoothly
            self.play(*animations, run_time=0.05, rate_func=smooth)