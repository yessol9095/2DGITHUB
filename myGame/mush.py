import random
from pico2d import *
from player import *
player = None

class Mush:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3

    image = None
    die = None
    hit = None

    def __init__(self):
        self.x, self.y = random.randint(130, 850), 110
        self.frame = 0
        self.dir = -1
        self.fy = 0
        #
        self.life_time = 0.0
        self.total_frames = 0.0
        #
        self.die = False
        self.frame_die = 0
        self.total_die = 0.0
        #
        self.hit = False
        self.frame_hit = 0

        if Mush.image == None:
            Mush.image = load_image('Resource/mush_run.png')
        if Mush.die == None:
            Mush.die = load_image('Resource/sheep_die.png')
        if Mush.hit == None:
            Mush.die = load_image('Resource/sheep_hit.png')

    def update(self, frame_time):
        global player
        player = Player()
        player.x, player.y = player.get_xy()
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.life_time += frame_time
        self.speed = Mush.RUN_SPEED_PPS * frame_time
        self.total_frames += Mush.FRAMES_PER_ACTION * Mush.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.die_frame = int(self.total_die) % 5

        if (self.x < 200) :
            self.dir = 1
            self.fy = 1
        elif (self.x > 900)  :
            self.dir = -1
            self.fy = 0

        self.x += (self.dir * self.speed)

    def draw(self):
        if self.die == True:
            self.die.clip_draw(0, self.frame_die * 100, 100, 100, self.x, self.y)
        elif self.hit == True:
            self.hit.clip_draw(0, self.frame_hit * 100, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, self.fy* 80, 100, 65, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 30, self.x + 35, self.y + 50

    def handle_event(self, event):
        pass






