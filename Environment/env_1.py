import pygame
from Environment.base_env import BaseEnvironment

class Env1(BaseEnvironment):
    def __init__(self, width, height):
        super().__init__(width, height)

        # rectangle half the env size, centered
        rect_w, rect_h = width // 3, height // 3
        x = (width - rect_w) / 2
        y = (height - rect_h) / 2

        self.create_obstacle(
            'rectangle',
            x=x, y=y,
            width=rect_w, height=rect_h,
            color=(200, 50, 50)
        )