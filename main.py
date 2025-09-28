import sys

import pygame as p
import pygame
p.init()
from audio import Audio
import asyncio
import time

if sys.platform != "emscripten":
    import importlib
    importlib.import_module("pygame")

async def main():
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

        def swap_buffers(self):  # swaps the two buffers in order to update the image displayed
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

        def __init__(self, width: int, height: int, red: int, green: int, blue: int, x: int, y: int, file_path=None):
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

        def update(self, dt):  # changes sprite position based on velocity
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

    class Label(Sprite):  # unmoving text or images
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

    class Button(Label):  # clickable text or images, inherits from label
        def __init__(self, width: int, height: int, text_red: int, text_green: int, text_blue: int, x, y, text: str,
                     font: pygame.font.SysFont("Calibri", 28), background=None, command=None):
            super().__init__(width, height, text_red, text_green, text_blue, x, y, text, font, background)
            self.command = command

        def mouse_touching(self, mouse_x, mouse_y):
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
            Label.__init__(self, self.width, self.height, self.text_red, self.text_green, self.text_blue,
                           int(self.position.x), int(self.position.y), time_string, self.font, self.background)

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


    class CustomChart():
        def __init__(self, chart_file_path: str):
            self.chart_file_path = chart_file_path

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

    window = Window(1000, 720, "eph :3", "n")


    windowcolour = p.Surface((1000, 720))
    windowcolour.fill((148, 201, 224))
    font = p.font.SysFont('Comic Sans MS', 32)
    level_list = []
    mult = 1
    # menu
    bg = Sprite(1000, 720, 0, 0, 0, 0, 0, file_path="assets/bg.png")
    orph = Sprite(300, 300, 255, 255, 255, 600, 300, file_path="assets/orph-default.png")
    game_title = Label(800, 150, 255, 255, 255, 100, 60, "eph :3", font, background="assets/button bg.png")
    mode_1 = Button(200, 100, 255, 255, 255, 300, 300, "play :3", font, background="assets/button bg.png")
    exit_button = Button(150, 100, 255, 255, 255, 350, 450, "exit :(", font, background="assets/button bg.png")
    pause = Label(650, 200, 255, 255, 255, 100, 255, "pause", font, background="assets/button bg.png")
    exit_return = Button(150, 100, 255, 255, 255, 350, 450, "nevermind", font, background="assets/button bg.png")
    exit_confirm = Button(150, 100, 255, 255, 255, 350, 200, "exit :(", font, background="assets/button bg.png")
    retry_button = Button(150, 100, 255, 255, 255, 350, 200, "retry", font, background="assets/button bg.png")
    menu_button = Button(150, 100, 255, 255, 255, 350, 400, "menu", font, background="assets/button bg.png")
    level_select_menu_button = Button(150, 100, 255, 255, 255, 350, 600, "level select", font,
                                      background="assets/button bg.png")
    selected_level_button = Button(150, 100, 255, 255, 255, 350, 600, "e", font, background="assets/button bg.png")
    mult_label = font.render(f"multiplier: {mult}", False, (255, 255, 255))

    # in-game
    tap_line = Sprite(35, 350, 255, 255, 255, 50, 0)
    tap_line_2 = Sprite(35, 350, 255, 255, 255, 50, 370)
    score = 0
    score_text = font.render("score: " + str(score), False, (255, 255, 255))
    win = font.render("you win!", False, (255,255,255))
    timer = 0
    positions = [85, 355]
    notes = []
    game_state = 0
    health_bar = HealthBar(200, 25, 255, 255, 255, 750, 50, 179, 229, 252, 100)
    chart = CustomChart("levels/level1/test_chart.txt")
    chart.read_chart()

    def notehit():
        print("hit")
        health_bar.current_health += 25
        score_text = font.render("score: " + str(score), False, (255, 255, 255))
        notes.pop(0)

    def start():
        score = 0
        health_bar.current_health = 50
        chart.read_chart()

    while True:
        await asyncio.sleep(0)

        # input section
        for event in p.event.get():
            if event.type == p.QUIT:
                print("you scored", str(score))
                p.quit()
                quit(0)
            elif event.type == p.KEYDOWN:
                for note in notes:
                    if event.key == p.K_j or event.key == p.K_k:
                        if Sprite.does_collide(note, tap_line_2):
                            score += 1*mult
                            if health_bar.current_health != 100 and mult >= 2:
                                mult -= 1
                            notehit()


                    elif event.key == p.K_f or event.key == p.K_d:
                        if Sprite.does_collide(note, tap_line):
                            score += 1*mult
                            if health_bar.current_health != 100 and mult >= 2:
                                mult -= 1
                            notehit()

                if event.key == p.K_ESCAPE:
                    if game_state == 1:
                        game_state = 3
                    elif game_state == 3:
                        game_state = 1

            elif event.type == p.MOUSEBUTTONDOWN:
                    if event.button == p.BUTTON_RIGHT:
                        for note in notes:
                            if Sprite.does_collide(note, tap_line_2):
                                score += 1*mult
                                if health_bar.current_health != 100 and mult >= 2:
                                    mult -= 1
                                notehit()


                    elif event.button == p.BUTTON_LEFT:
                        if game_state == 0:
                            mouse_x, mouse_y = event.pos
                            if mode_1.mouse_touching(mouse_x, mouse_y):
                                start()
                                game_state = 1
                            if exit_button.mouse_touching(mouse_x, mouse_y):
                                game_state = 5

                        elif game_state == 1:
                            for note in notes:
                                if Sprite.does_collide(note, tap_line):
                                    score += 1*mult
                                    if health_bar.current_health != 100 and mult >= 2:
                                        mult -= 1
                                    notehit()

                        elif game_state == 5:
                            mouse_x, mouse_y = event.pos
                            if exit_confirm.mouse_touching(mouse_x, mouse_y):
                                p.quit()
                                exit(0)
                            elif exit_return.mouse_touching(mouse_x, mouse_y):
                                game_state = 0

                        elif game_state == 6:
                            mouse_x, mouse_y = event.pos
                            if retry_button.mouse_touching(mouse_x, mouse_y):
                                score = 0
                                start()
                                game_state = 1

                            elif menu_button.mouse_touching(mouse_x, mouse_y):
                                score = 0
                                game_state = 0

            elif timer <= 0:
                if game_state == 1:
                    try:
                        if chart.notes_array[0][1] == "R":
                            notes.append(Sprite(100, 100, 0, 0, 0, 1000, 510, file_path="assets/shark.png"))
                            chart.notes_array.pop(0)

                        elif chart.notes_array[0][1] == "L":
                            notes.append(Sprite(100, 100, 0, 0, 0, 1000, 150, file_path="assets/shark.png"))
                            chart.notes_array.pop(0)

                        elif chart.notes_array[0][0] == "END":
                            if notes == []:
                                game_state = 6

                        elif chart.notes_array[0][1] == "DOUBLE":
                            notes.append(Sprite(100, 100, 0, 0, 0, 1000, 510, file_path="assets/shark.png"))
                            notes.append(Sprite(100, 100, 0, 0, 0, 1000, 150, file_path="assets/shark.png"))
                            chart.notes_array.pop(0)
                        else:
                            timer = float(chart.notes_array[0][1])
                            chart.notes_array.pop(0)
                    except IndexError:
                        pass
                    print(chart.notes_array)

        # update section
        deltatime = window.get_dt()
        timer = timer - deltatime
        if game_state == 1:
            for note in notes:
                if note.position.x < 0:
                    health_bar.current_health -= 25
                    mult += 1
                    notes.pop(0)
                note.velocity = Vector(-800, 0)
                note.update(deltatime)

            if health_bar.current_health == 0:  #game over
                print("you scored", str(score))
                game_state = 6

        health_bar.update_appearance()
        score_text = font.render("score: " + str(score), False, (255, 255, 255))
        mult_label = font.render(f"multiplier: {mult}", False, (255, 255, 255))


        # render section
        window.clear()
        window.window.blit(windowcolour, (0, 0))


        if game_state == 0: #title screen
            window.draw(game_title)
            window.draw(mode_1)
            window.draw(exit_button)
            window.draw(orph)


        if game_state == 1:
            #game
            window.draw(bg)
            window.window.blit(score_text, (775, 125))
            window.window.blit(mult_label, (775, 160))
            window.draw(health_bar)
            window.draw(tap_line)
            window.draw(tap_line_2)
            for note in notes:
                window.draw(note)

        elif game_state == 3:   #pause
            window.draw(pause)
            window.draw(orph)


        elif game_state == 5:   #exit confirmation
            window.draw(exit_confirm)
            window.draw(exit_return)

        elif game_state == 6:   #game over
            window.window.blit(win, (50,50))
            window.draw(retry_button)
            window.draw(menu_button)



        window.swap_buffers()


asyncio.run(main())