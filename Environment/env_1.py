import pygame
from Environment.base_env import BaseEnvironment

class Env1(BaseEnvironment):
    def __init__(self, width, height):
        super().__init__(width, height)

        # Circle obstacle in the center
        radius = min(width, height) // 8
        x = width / 2
        y = height / 2
        self.create_obstacle(
            'circle',
            x=x, y=y,
            radius=radius,
            color=(200, 50, 50)
        )

        # Small circle obstacle in the top-left corner
        small_radius = radius // 2
        self.create_obstacle(
            'circle',
            x=width / 4,
            y=height / 4,
            radius=small_radius,
            color=(200, 200, 50)
        )

        # Small circle obstacle in the bottom-right corner
        self.create_obstacle(
            'circle',
            x=3 * width / 4,
            y=3 * height / 4,
            radius=small_radius,
            color=(50, 200, 200)
        )
