import pygame, random

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
        self.perception = 50    # perception radius

    def apply_force(self, force):
        """Accumulate steering force into acceleration."""
        self.acceleration += force

    def alignment(self, boids):
        """
        Steer towards average heading of local flockmates.
        """
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other is not self:
                distance = self.position.distance_to(other.position)
                if distance < self.perception:
                    steering += other.velocity
                    total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def cohesion(self, boids):
        """
        Steer towards average position of local flockmates.
        """
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other is not self:
                distance = self.position.distance_to(other.position)
                if distance < self.perception:
                    steering += other.position
                    total += 1
        if total > 0:
            steering /= total
            steering = (steering - self.position)
            steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def separation(self, boids):
        """
        Steer to avoid crowding local flockmates.
        """
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other is not self:
                distance = self.position.distance_to(other.position)
                if distance < self.perception and distance > 0:
                    diff = (self.position - other.position) / distance
                    steering += diff
                    total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def flock(self, boids):
        """
        Calculate and apply steering from alignment, cohesion, and separation.
        """
        align_force = self.alignment(boids)
        coh_force   = self.cohesion(boids)
        sep_force   = self.separation(boids)

        self.apply_force(align_force)
        self.apply_force(coh_force)
        self.apply_force(sep_force)



    def update(self):
        """Integrate acceleration into velocity and position."""
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration = pygame.Vector2(0, 0)

    def draw(self, screen):
        """Draw the bird as a triangle pointing in direction of its velocity."""
        angle = self.velocity.angle_to(pygame.Vector2(1, 0))
        head  = self.position + pygame.Vector2(10, 0).rotate(-angle)
        left  = self.position + pygame.Vector2(-5, 5).rotate(-angle)
        right = self.position + pygame.Vector2(-5, -5).rotate(-angle)
        pygame.draw.polygon(screen, (255, 255, 255), [head, left, right])
