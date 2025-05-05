import pygame
from Environment.base_env import BaseEnvironment

class Env2(BaseEnvironment):
    def __init__(self, width, height):
        super().__init__(width, height)
        
        self.create_target()