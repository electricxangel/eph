from label import Label
import pygame

#Button class
#Inherits from label - makes it clickable!

class Button(Label):
    def __init__(self, width: int, height: int, text_red: int, text_green: int, text_blue: int, x, y, text: str,
                 font: pygame.font.SysFont("Calibri", 28), background=None, command=None):
        super().__init__(width, height, text_red, text_green, text_blue, x, y, text, font, background)
        self.command = command

    def mouse_touching(self,  mouse_x, mouse_y):
        # Collision detection between mouse and button
        return (
                self.get_left() <= mouse_x <= self.get_right()
                and self.get_top() <= mouse_y <= self.get_bottom()
        )

    def button_clicked(self):
        if self.command is not None:
            self.command()