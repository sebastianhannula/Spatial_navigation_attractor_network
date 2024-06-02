from manim import *
import numpy as np
import os

config.frame_rate = 60

class RingAttractorAnimation(Scene):
    def setup(self):
        self.camera.background_color = WHITE

    def construct(self):
        # Load activity data
        activity_data = np.load(os.path.join('./simulation/data/','full_velocity_activations.npy'))  
        activity_data_ec = np.load(os.path.join('./simulation/data/','full_activations_ec.npy'))
        activity_data_wc = np.load(os.path.join('./simulation/data/','full_activations_wc.npy'))
        w1_data = np.load(os.path.join('./simulation/data/','full_w1_history.npy'))
        w2_data = np.load(os.path.join('./simulation/data/','full_w2_history.npy'))
        landmark_1_data = np.load(os.path.join('./simulation/data/','full_landmark_1.npy'))
        landmark_2_data = np.load(os.path.join('./simulation/data/','full_landmark_2.npy'))

        # Constants for visualization
        n_cells = activity_data.shape[1]
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
            ) for i in range(0, n_cells, 5)
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
            ) for i in range(0, n_cells, 5)
        ])
        self.add(balls_ec)

        balls_wc = VGroup(*[
            Circle(radius=0.15, stroke_color=BLUE, stroke_width=6, stroke_opacity=1, fill_opacity=0).move_to(
                wc_radius * np.array([
                    np.cos(i * angle_offset),
                    np.sin(i * angle_offset),
                    0
                ])
            ) for i in range(0, n_cells, 5)
        ])
        self.add(balls_wc)

        # Additional balls for east and west movement
        east_ball = Circle(radius=0.3, stroke_color=GREEN, stroke_width=6, fill_opacity=0)
        west_ball = Circle(radius=0.3, stroke_color=BLUE, stroke_width=6, fill_opacity=0, stroke_opacity=1)
        east_ball.move_to(wc_radius * np.array([np.cos(1/4*np.pi), np.sin(1/4*np.pi), 0]) + RIGHT * 2)  
        west_ball.move_to(wc_radius * np.array([np.cos(3/4*np.pi), np.sin(3/4*np.pi), 0]) + LEFT * 2) 
        self.add(east_ball, west_ball)

        # Landmark cells
        landmark_1 = Circle(radius=0.4, stroke_color=ORANGE, stroke_width=10, fill_opacity=0)
        landmark_2 = Circle(radius=0.4, stroke_color=ORANGE, stroke_width=10, fill_opacity=0)
        landmark_1.move_to(LEFT * 5)
        landmark_2.move_to(RIGHT * 5)
        self.add(landmark_1, landmark_2)

        label_1 = Text("#1", font_size=32, color=DARK_GRAY)
        label_2 = Text("#2", font_size=32, color=DARK_GRAY)
        label_1.next_to(landmark_1, UP, buff=0.2)
        label_2.next_to(landmark_2, UP, buff=0.2) 
        self.add(label_1, label_2)

        # Line along which the mouse moves
        movement_line = Line(LEFT * 4 + DOWN * 3.5, RIGHT * 4 + DOWN * 3.5, color=GRAY, stroke_opacity=0.7)
        self.add(movement_line)

        # Create boxes at each end of the line
        box_size = 0.5 
        left_box = Square(side_length=box_size, color=ORANGE, fill_opacity=0.5, stroke_opacity=1)
        right_box = Square(side_length=box_size, color=ORANGE, fill_opacity=0.5, stroke_opacity=1)
        left_box.move_to(LEFT * 4 + DOWN * 3.5)
        right_box.move_to(RIGHT * 4 + DOWN * 3.5)
        self.add(left_box, right_box)

        label_3 = Text("#1", font_size=24, color=DARK_GRAY)
        label_4 = Text("#2", font_size=24, color=DARK_GRAY)
        label_3.next_to(left_box, UP, buff=0.1)
        label_4.next_to(right_box, UP, buff=0.1) 
        self.add(label_3, label_4)

        # Create the mouse as a brown ball
        mouse = Circle(radius=0.2, stroke_color=GREY_BROWN, fill_color=GREY_BROWN, fill_opacity=1, stroke_opacity=1)
        mouse_start = LEFT * 4 + DOWN * 3.5 
        mouse.move_to(mouse_start)
        self.add(mouse)

        self.wait(2)

        arrs_1 = VGroup()
        arrs_2 = VGroup()
        # Create arrows for conections from landmark cells to main ring
        for i, main_ball in enumerate(balls):
            w1 = w1_data[0][::5][i]
            w2 = w2_data[0][::5][i]
            norm_w1 = w1 / np.max(w1_data) if np.max(w1_data) > 0 else 0
            norm_w2 = w2 / np.max(w2_data) if np.max(w2_data) > 0 else 0
            norm_w1 = 0 if norm_w1 < 0.5 else norm_w1
            norm_w2 = 0 if norm_w2 < 0.5 else norm_w2
            arrow1_dir = main_ball.get_center() - landmark_1.get_center()
            arrow2_dir = main_ball.get_center() - landmark_2.get_center()
            unit_dir_1 = arrow1_dir / np.linalg.norm(arrow1_dir)
            unit_dir_2 = arrow2_dir / np.linalg.norm(arrow2_dir)
            arrow1 = Arrow(landmark_1.get_center() + unit_dir_1 * 0.5, main_ball.get_center()-0.25*unit_dir_1, buff=0, stroke_width=2*norm_w1, color=RED, tip_length=0.1).set_opacity(norm_w1)  
            arrow2 = Arrow(landmark_2.get_center() + unit_dir_2 * 0.5, main_ball.get_center()-0.25*unit_dir_2, buff=0, stroke_width=2*norm_w2, color=RED, tip_length=0.1).set_opacity(norm_w2)
            arrs_1.add(arrow1)
            arrs_2.add(arrow2)
        self.play([FadeIn(arrs_1), FadeIn(arrs_2)], run_time=1)

        # Animate activity
        step_size = 10 
        for step in range(0, len(activity_data), step_size):
            state = activity_data[step]
            state_ec = activity_data_ec[step]
            state_wc = activity_data_wc[step]
            w1_selected = w1_data[step][::5]
            w2_selected = w2_data[step][::5]
            animations = []
            if np.any(state_ec > 0):
                current_x = mouse.get_center()[0]
                new_x = current_x + 0.08
                mouse.move_to(np.array([new_x, mouse.get_center()[1], 0]))
                east_ball.set_fill(color=RED, opacity=1)
            else:
                east_ball.set_fill(color=RED, opacity=0)
            if np.any(state_wc > 0):
                current_x = mouse.get_center()[0]
                new_x = current_x - 0.08
                mouse.move_to(np.array([new_x, mouse.get_center()[1], 0]))
                west_ball.set_fill(color=RED, opacity=1)
            else:
                west_ball.set_fill(color=RED, opacity=0)

            for i, (w1, w2, arrow1, arrow2) in enumerate(zip(w1_selected, w2_selected, arrs_1, arrs_2)):
                index = i * 5 if i < len(balls) else i
                ball = balls[i]
                ball_ec = balls_ec[i]
                ball_wc = balls_wc[i]
                normalized_activity = state[index] / np.max(activity_data) if np.max(state) > 0 else 0
                normalized_activity_ec = state_ec[index] / np.max(activity_data_ec) if np.max(state_ec) > 0 else 0
                normalized_activity_wc = state_wc[index] / np.max(activity_data_wc) if np.max(state_wc) > 0 else 0

                ball_color = interpolate_color(WHITE, RED, normalized_activity)
                ec_color = interpolate_color(WHITE, RED, normalized_activity_ec)
                wc_color = interpolate_color(WHITE, RED, normalized_activity_wc)
                landmark1_color = interpolate_color(WHITE, RED, landmark_1_data[step] if step < len(landmark_1_data) else 0)
                landmark2_color = interpolate_color(WHITE, RED, landmark_2_data[step] if step < len(landmark_2_data) else 0)

                animations.extend([
                    ball.animate.set_fill(ball_color, opacity=1 if normalized_activity > 0 else 0),
                    ball_ec.animate.set_fill(ec_color, opacity=1 if normalized_activity_ec > 0 else 0),
                    ball_wc.animate.set_fill(wc_color, opacity=1 if normalized_activity_wc > 0 else 0),
                    landmark_1.animate.set_fill(landmark1_color, opacity=1),
                    landmark_2.animate.set_fill(landmark2_color, opacity=1)
                ])

                norm_w1 = w1 / np.max(w1_data) if np.max(w1_data) > 0 else 0
                norm_w2 = w2 / np.max(w2_data) if np.max(w2_data) > 0 else 0
                norm_w1 = 0 if norm_w1 < 0.5 else norm_w1
                norm_w2 = 0 if norm_w2 < 0.5 else norm_w2
                animations.append(arrow1.animate.set_opacity(norm_w1).set_stroke(width=2*norm_w1))
                animations.append(arrow2.animate.set_opacity(norm_w2).set_stroke(width=2*norm_w2))

            # Play all animations together smoothly
            self.play(*animations, run_time=0.05, rate_func=smooth)

        self.wait(5) 