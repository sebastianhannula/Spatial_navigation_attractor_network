from manim import *
import numpy as np

config.frame_rate = 60

class RingAttractorAnimation(Scene):
    def setup(self):
        self.camera.background_color = WHITE

    def construct(self):
        # Constants for visualization
        n_cells = 20  # Total number of cells (adjust as needed)
        radius = 1.8  # Radius for the main ring
        ec_radius = 2.6  # Radius for the EC ring
        wc_radius = 3  # Radius for the WC ring
        angle_offset = 2 * np.pi / n_cells  # Angular offset for each cell

        # Create a ring of circles for main neurons
        balls = VGroup(*[
            Circle(radius=0.25, stroke_color=BLACK, stroke_opacity=1, fill_opacity=0).move_to(
                radius * np.array([
                    np.cos(i * angle_offset),
                    np.sin(i * angle_offset),
                    0
                ])
            ) for i in range(n_cells)
        ])
        self.add(balls)

        # Create rings for east and west velocity-sensitive cells
        balls_ec = VGroup(*[
            Circle(radius=0.15, stroke_color=GREEN, stroke_width=6, stroke_opacity=1, fill_opacity=0).move_to(
                ec_radius * np.array([
                    np.cos(i * angle_offset),
                    np.sin(i * angle_offset),
                    0
                ])
            ) for i in range(n_cells)
        ])
        self.add(balls_ec)

        balls_wc = VGroup(*[
            Circle(radius=0.15, stroke_color=BLUE, stroke_width=6, stroke_opacity=1, fill_opacity=0).move_to(
                wc_radius * np.array([
                    np.cos(i * angle_offset),
                    np.sin(i * angle_offset),
                    0
                ])
            ) for i in range(n_cells)
        ])
        self.add(balls_wc)

        # Additional balls for east and west movement
        east_ball = Circle(radius=0.3, stroke_color=GREEN, stroke_width=6, fill_opacity=0)
        west_ball = Circle(radius=0.3, stroke_color=BLUE, stroke_width=6, fill_opacity=0, stroke_opacity=1)
        east_ball.move_to(wc_radius * np.array([np.cos(1/4*np.pi), np.sin(1/4*np.pi), 0]) + RIGHT * 2)  
        west_ball.move_to(wc_radius * np.array([np.cos(3/4*np.pi), np.sin(3/4*np.pi), 0]) + LEFT * 2) 
        self.add(east_ball, west_ball)


        self.wait(1)

        self.play(
            *[wc_ball.animate.set_stroke(opacity=0.2) for wc_ball in balls_wc],
            west_ball.animate.set_stroke(opacity=0.2),
            run_time=2
        )

        self.wait(1)
        # Animate connections from main ring to east cells
        connections = VGroup()
        for main_ball, ec_ball in zip(balls, balls_ec):
            arrow_dir = ec_ball.get_center() - main_ball.get_center()
            arrow = Arrow(main_ball.get_center() + arrow_dir * 0.3, ec_ball.get_center() - arrow_dir * 0.2, buff=1, stroke_width=2, color=BLUE, tip_length=0.1)
            connections.add(arrow)
        self.play(FadeIn(connections), run_time=1)
        self.wait(7)
        self.play(FadeOut(connections), run_time=1)

        arrows = VGroup()
        for ec_ball in balls_ec:
            arrow_dir = ec_ball.get_center() - east_ball.get_center()
            unit_dir = arrow_dir / np.abs(np.linalg.norm(arrow_dir))
            arrow = Arrow(east_ball.get_center() + 0.5*unit_dir, east_ball.get_center() + (arrow_dir-0.2*unit_dir), buff=0, stroke_width=2, color=RED, tip_length=0.1).set_opacity(0.5)
            arrows.add(arrow)
        self.play(FadeIn(arrows), run_time=1)
        self.wait(7)
        self.play(FadeOut(arrows), run_time=1)

        # Draw connections from east cells to main ring with a clockwise bias
        bias_arrows = VGroup()
        for i, ec_ball in enumerate(balls_ec):
            target_index = (i - 2) % n_cells
            tgt_ball = balls[target_index]
            arrow_dir = tgt_ball.get_center() - ec_ball.get_center()
            unit_dir = arrow_dir / np.abs(np.linalg.norm(arrow_dir))
            orthogonal_dir = np.array([-unit_dir[1], unit_dir[0], 0])
            arrow = Arrow(ec_ball.get_center() + 0.2*unit_dir, ec_ball.get_center() + (arrow_dir-0.2*unit_dir+0.2*orthogonal_dir) , buff=0, stroke_width=2, color=PURPLE, tip_length=0.1)
            bias_arrows.add(arrow)
        self.play(FadeIn(bias_arrows), run_time=1)
        self.wait(7)
        self.play(FadeOut(bias_arrows), run_time=1)

        self.play([FadeIn(connections), FadeIn(arrows), FadeIn(bias_arrows)], run_time=1)

        self.wait(5) 
