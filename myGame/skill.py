import random

from pico2d import *



class Skill:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    image = None
    hit = None

    def __init__(self):
        self.x, self.y = 1100, 50
        self.frame = 0
        #
        self.life_time = 0.0
        self.total_frames = 0.0
        #
        self.hit = False
        self.frame_hit = 0

        if Skill.image == None:
            Skill.image = load_image('Resource/Skill.png')


    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.life_time += frame_time
        self.total_frames += Skill.FRAMES_PER_ACTION * Skill.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 2


    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 55, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 25, self.x + 25, self.y + 20

    def handle_event(self, event):
        pass






