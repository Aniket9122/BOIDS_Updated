import pygame
import random

class Bird:
    def __init__(self, x, y):
        # Position, random initial velocity, and physics
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-2, 2),
                                       random.uniform(-2, 2))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 4      # matches pilot.py
        self.max_force = 0.1    # matches pilot.py
        self.perception = 50    # matches pilot.py

    def apply_force(self, force):
        self.acceleration += force

    def flock(self, boids):
        alignment = pygame.Vector2(0, 0)
        cohesion  = pygame.Vector2(0, 0)
        separation = pygame.Vector2(0, 0)
        total = 0

        for other in boids:
            if other is not self:
                distance = self.position.distance_to(other.position)
                if distance < self.perception:
                    # alignment
                    alignment += other.velocity
                    # cohesion
                    cohesion += other.position
                    # separation
                    diff = self.position - other.position
                    if distance > 0:
                        diff /= distance
                    separation += diff
                    total += 1

        if total > 0:
            # ALIGNMENT
            alignment /= total
            alignment.scale_to_length(self.max_speed)
            alignment -= self.velocity
            if alignment.length() > self.max_force:
                alignment.scale_to_length(self.max_force)
            self.apply_force(alignment)

            # COHESION
            cohesion /= total
            cohesion = cohesion - self.position
            cohesion.scale_to_length(self.max_speed)
            cohesion -= self.velocity
            if cohesion.length() > self.max_force:
                cohesion.scale_to_length(self.max_force)
            self.apply_force(cohesion)

            # SEPARATION
            separation /= total
            separation.scale_to_length(self.max_speed)
            separation -= self.velocity
            if separation.length() > self.max_force:
                separation.scale_to_length(self.max_force)
            self.apply_force(separation)

    def update(self):
        # integrate physics
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration = pygame.Vector2(0, 0)

    def draw(self, screen):
        # draw as triangle pointing along velocity
        angle = self.velocity.angle_to(pygame.Vector2(1, 0))
        head  = self.position + pygame.Vector2(10, 0).rotate(-angle)
        left  = self.position + pygame.Vector2(-5, 5).rotate(-angle)
        right = self.position + pygame.Vector2(-5, -5).rotate(-angle)
        pygame.draw.polygon(screen, (255, 255, 255), [head, left, right])
