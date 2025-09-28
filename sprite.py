from vector import Vector
import pygame as p

class Sprite:
    def does_collide(sprite1: "Sprite", sprite2: "Sprite"):
        return (sprite1.get_left() <= sprite2.get_right() and
                sprite1.get_right() >= sprite2.get_left() and
                sprite1.get_top() <= sprite2.get_bottom() + 5 and
                sprite1.get_bottom() >= sprite2.get_top())


    def __init__(self, width: int, height: int, red: int, green:int, blue:int, x:int, y:int, file_path=None):
        if file_path is None:
            self.surface = p.Surface((width, height))
            self.surface.fill((red, green, blue))
        else:
            self.surface = p.image.load(file_path).convert_alpha()
            self.surface = p.transform.scale(self.surface, (width, height))

        self.position = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.width = width
        self.height = height

    def update(self, dt):   # changes sprite position based on velocity
        movement = Vector(self.velocity.x * dt, self.velocity.y * dt)
        self.position += movement

    def get_top(self):
        return self.position.y

    def get_bottom(self):
        return self.position.y + self.height
    def get_left(self):
        return self.position.x
    def get_right(self):
        return self.position.x + self.width
