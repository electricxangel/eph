from sprite import Sprite
import pygame

#Health bar
#Inherits from sprite
# Fills and empties as player hits or misses notes

class HealthBar(Sprite):
    def __init__(self, width, height, emp_r, emp_g, emp_b, x, y, full_r, full_g, full_b, max_health):
        super().__init__(width, height, emp_r, emp_g, emp_b, x, y)
        self.full_r = full_r
        self.full_g = full_g
        self.full_b = full_b
        self.emp_r = emp_r
        self.emp_g = emp_g
        self.emp_b = emp_b
        self.max_health = max_health
        self.current_health = max_health / 2

    def update_appearance(self):
        # Updates health level when user heals or takes damage

        # If health below/above min/max, don't
        if self.current_health < 0:
            self.current_health = 0
        if self.current_health > 100:
            self.current_health = 100
        full_width = (self.current_health / self.max_health) * self.width
        empty_width = self.width - full_width

        # Fill full bar with colour
        full_bar = pygame.Surface((full_width, self.height))
        full_bar.fill((self.full_r, self.full_g, self.full_b))

        # Fill empty bar with white
        empty_bar = pygame.Surface((empty_width, self.height))
        empty_bar.fill((self.emp_r, self.emp_g, self.emp_b))

        self.surface.blit(full_bar, (0, 0))
        self.surface.blit(empty_bar, (full_width, 0))
