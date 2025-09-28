import pygame as p

class Audio:
    def __init__(self, file_path: str):
        self.sound = p.mixer.Sound(file_path)   #Finds audio file in directory

    def play(self, loops: bool = False):    #Play function allows for looping if needed
        if loops:
            self.sound.play(loops=-1)
        else:
            self.sound.play()

    def stop(self):
        self.sound.stop()
