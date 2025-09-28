from sprite import Sprite
import pygame


# Unmoving text or images
# Inherits from Sprite

class Label(Sprite):
    def __init__(self, width: int, height: int, text_red: int, text_green: int, text_blue: int, x, y, text: str,
                 font: pygame.font.SysFont("Calibri", 28), background=None):
        if background is None:

            super().__init__(width, height, 0, 0, 0, x, y)
        else:
            super().__init__(width, height, 0, 0, 0, x, y, file_path=background)

        self.text = text
        self.font = font
        rendered_text = font.render(text, True, (text_red, text_green, text_blue))
        rendered_text = pygame.transform.scale(rendered_text, (width, height))
        self.surface.blit(rendered_text, (0, 0))