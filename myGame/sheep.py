import random

from pico2d import *

class Sheep:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 30.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.8
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3
    FRAMES_PER_DIE = 5

    image = None
    die = None
    hit = None
    # sound
    hit_sound = None
    die_sound = None

    def __init__(self):
        self.x, self.y = random.randint(900, 1300), 200
        self.frame = 0
        self.dir = -1
        self.fy = 0
        #
        self.hp = 5
        self.life_time = 0.0
        self.total_frames = 0.0
        self.life_flag = True
        #
        self.d_time = 0
        self.s_die = False
        self.frame_die = 0
        self.die_frame = 0
        self.total_die = 0.0
        #
        self.s_hit = False
        self.frame_hit = 0
        self.h_time = 0

        if Sheep.image == None:
            Sheep.image = load_image('Resource/sheep_run.png')
        if Sheep.die == None:
            Sheep.die = load_image('Resource/sheep_die.png')
        if Sheep.hit == None:
            Sheep.hit = load_image('Resource/sheep_hit.png')
        # sound
        if Sheep.hit_sound == None:
            Sheep.hit_sound = load_wav("Sound/hit.wav")
            Sheep.hit_sound.set_volume(32)
        if Sheep.die_sound == None:
            Sheep.die_sound = load_wav("Sound/yang_death.wav")
            Sheep.die_sound.set_volume(32)


    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.life_time += frame_time
        self.speed = Sheep.RUN_SPEED_PPS * frame_time
        self.total_frames += Sheep.FRAMES_PER_ACTION * Sheep.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3
        self.die_frame = int(self.total_die) % 5
        if self.s_die == True:
            self.d_time += frame_time
            self.total_die += Sheep.FRAMES_PER_DIE * Sheep.ACTION_PER_TIME * frame_time
            if self.d_time >= 0.6:
                self.life_flag = False
                self.d_time = 0
        if self.s_hit == True:
            self.h_time += frame_time
            if self.h_time >= 0.3:
                self.h_time = 0
                self.s_hit = False

        if (self.x < 650):
            self.dir = 1
            self.fy = 1
        elif (self.x > 1300):
            self.dir = -1
            self.fy = 0
        if self.s_die == False:
            self.x += (self.dir * self.speed)

    def hurt(self):
        self.s_hit = True
        self.hp -= 1
        self.hit_sound.play()

    def death(self):
        self.s_die = True
        self.die_sound.play()
    def draw(self):
        if self.s_die == True:
            self.die.clip_draw(self.die_frame * 100, self.frame_die * 65 ,100, 65, self.x,self.y)
        elif self.s_hit == True:
            self.hit.clip_draw(0, self.fy * 65, 100, 65, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, self.fy* 65, 100, 65, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 30, self.x + 35, self.y + 50

    def handle_event(self, event):
        pass

    def reset(self):
        image = None
        die = None
        hit = None
        # sound
        hit_sound = None
        die_sound = None







