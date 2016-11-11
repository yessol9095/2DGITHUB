import random

from pico2d import *

class Bullet:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    image = None

    def __init__(self):
        self.x, self.y = 100, 90
        self.frame = 0
        #
        self.life_time = 0.0
        self.total_frames = 0.0
        self.shot = 0
        self.dir = 0

        if Bullet.image == None:
            Bullet.image = load_image('Resource/bullet.png')

    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.life_time += frame_time
        self.speed = Bullet.RUN_SPEED_PPS * frame_time
        self.total_frames += Bullet.MES_PER_ACTION * Bullet.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frFRAames) % 2
        self.x += (self.dir * self.speed)



    def draw(self):
        if(self.shot):
            self.Bullet.clip_draw(self.frame * 100, self.frame * 100, 100, 100, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 25, self.y + 50

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
                self.shot = True






