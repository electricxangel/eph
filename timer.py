from label import Label
import pygame

class Timer(Label):
    def __init__(self, width: int, height: int, text_red: int, text_green: int, text_blue: int, x, y, start_time,
                 time_scale, font: pygame.font.SysFont("Calibri", 28), background=None):
        Label.__init__(self, width, height, text_red, text_green, text_blue, x, y, "00:00", font, background)

        self.width = width
        self.height = height
        self.text_red = text_red
        self.text_green = text_green
        self.text_blue = text_blue
        self.start_time = start_time
        self.current_time = start_time
        self.time_scale = time_scale
        self.font = font
        self.background = background

    def recreate_timer(self):
        minutes = int(self.current_time) // 60
        seconds = int(self.current_time) % 60
        time_string = "{:02}:{:02}".format(minutes, seconds)
        Label.__init__(self, self.width, self.height, self.text_red, self.text_green, self.text_blue, int(self.position.x), int(self.position.y), time_string, self.font, self.background)

    def update(self, dt):
        self.current_time += (dt * self.time_scale)
