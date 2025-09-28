import pygame as p
import time
import pygame.font

p.init()


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)
    def __str__(self):
        return f"({self.x}, {self.y})"

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


class Label(Sprite):    # unmoving text or images
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

class Button(Label): # clickable text or images, inherits from label
    def __init__(self, width: int, height: int, text_red: int, text_green: int, text_blue: int, x, y, text: str,
                 font: pygame.font.SysFont("Calibri", 28), background=None, command=None):
        super().__init__(width, height, text_red, text_green, text_blue, x, y, text, font, background)
        self.command = command

    def mouse_touching(self,  mouse_x, mouse_y):
        return (
                self.get_left() <= mouse_x <= self.get_right()
                and self.get_top() <= mouse_y <= self.get_bottom()
        )

    def button_clicked(self):
        if self.command is not None:
            self.command()

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
        if self.current_health < 0:
            self.current_health = 0
        if self.current_health > 100:
            self.current_health = 100
        full_width = (self.current_health / self.max_health) * self.width
        empty_width = self.width - full_width


        full_bar = pygame.Surface((full_width, self.height))
        full_bar.fill((self.full_r, self.full_g, self.full_b))

        empty_bar = pygame.Surface((empty_width, self.height))
        empty_bar.fill((self.emp_r, self.emp_g, self.emp_b))

        self.surface.blit(full_bar, (0, 0))
        self.surface.blit(empty_bar, (full_width, 0))

class Audio:
    def __init__(self, file_path: str):
        self.sound = p.mixer.Sound(file_path)

    def play(self, loops: bool = False):
        if loops:
            self.sound.play(loops=-1)
        else:
            self.sound.play()

    def stop(self):
        self.sound.stop()

class CustomChart(Audio):
    def __init__(self, chart_file_path: str, file_path: str=None):
        super().__init__(file_path)
        self.chart_file_path = chart_file_path
        self.file_path = file_path

    def read_chart(self):
        chart_file = open(self.chart_file_path, "r")
        self.notes_to_spawn = chart_file.readlines()
        self.notes_array = []
        for i in range(len(self.notes_to_spawn)):
            self.notes_array.append(self.notes_to_spawn[i].split(" "))
        print(self.notes_array)
        for i in range(len(self.notes_array)):
            self.notes_array[i][1] = self.notes_array[i][1].replace("\n", "")

        print(self.notes_array)
        chart_file.close()
        return self.notes_to_spawn
