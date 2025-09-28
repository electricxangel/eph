import time
import pygame as p

class Window:
    def __init__(self, width: int, height: int, caption: str, fullscreen: str):
        p.display.set_caption(caption)
        self.previous_time = time.time()

        if fullscreen == "y":
            self.window = p.display.set_mode((width, height), p.FULLSCREEN)
        else:
            self.window = p.display.set_mode((width, height), p.RESIZABLE)

    def draw(self, sprite):
        self.window.blit(sprite.surface, (sprite.position.x, sprite.position.y))

    def swap_buffers(self): #swaps the two buffers in order to update the image displayed
        p.display.flip()

    def clear(self):
        self.window.fill((0, 0, 0))

    def get_dt(self):
        current_time = time.time()
        dt = current_time - self.previous_time
        self.previous_time = current_time
        return dt

    def get_size(self):
        return self.window.get_size()