import random
from pico2d import *
from player import *
player = None


class Finalboss:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 10.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.8
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6
    FRAMES_PER_DIE = 8
    FRAMES_PER_HIT = 6

    image = None
    die = None
    hit = None
    hp = None
    hp_title = None

    def __init__(self):
        self.x, self.y = 1000, 140
        self.frame = 0
        self.dir = 1
        self.fy = 1
        #
        self.life = 5
        self.b_death = False
        self.b_hp = False
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

        if Finalboss.image == None:
            Finalboss.image = load_image('Resource/final_boss_run.png')
        if Finalboss.die == None:
            Finalboss.die = load_image('Resource/final_boss_die.png')
        if Finalboss.hit == None:
            Finalboss.hit = load_image('Resource/final_boss_hit.png')
        if Finalboss.hp_title == None:
            Finalboss.hp_title = load_image('Resource/Hp_Title.png')
        if Finalboss.hp == None:
            Finalboss.hp = load_image('Resource/finalboss_hp.png')

    def update(self, frame_time):
        global player
        player = Player()
        player.x, player.y = player.get_xy()

        self.life_time += frame_time
        self.speed = Finalboss.RUN_SPEED_PPS * frame_time
        self.total_frames += Finalboss.FRAMES_PER_ACTION * Finalboss.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6
        self.die_frame = int(self.total_die) % 8

        if self.s_die == True:
            self.d_time += frame_time
            self.total_die += Finalboss.FRAMES_PER_DIE * Finalboss.ACTION_PER_TIME * frame_time
            if self.d_time >= 0.8:
                self.life_flag = False
                self.d_time = 0
        if self.s_hit == True:
            self.h_time += frame_time
            if self.h_time >= 0.3:
                self.h_time = 0
                self.s_hit = False

        if (self.y < 100):
            self.dir = 1
        elif (self.y > 400):
            self.dir = -1
        if self.s_die == False:
            self.y += (self.dir * self.speed)



    def hurt(self):
        self.s_hit = True
        self.life -= 1

    def death(self):
        self.s_die = True

    def draw(self):
        if self.s_die == True:
            self.die.clip_draw(self.die_frame * 178, 198, 193, 209, self.x, self.y)
        elif self.s_hit == True:
            self.image.clip_draw(self.frame * 193, self.fy * 209, 193, 209, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 193, self.fy* 209, 193, 209, self.x, self.y)
        self.hp_title.clip_draw(0, 0, 244, 35, 1000, 550)
        self.hp.clip_draw(0, 0, self.life * 30, 25, 1000, 550)
    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 80, self.x + 35, self.y + 50

    def handle_event(self, event):
        pass

###############################################################


class Finalbullet:
    PIXEL_PER_METER = (10.0 / 0.3 )         # 10 pixel 30cm
    BULLET_SPEED_KMPH = 15.0                   # km / Hour
    BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
    BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
    BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2
    BULLET_SPEED = 5

    image = None


    def __init__(self,x,y):

        self.x = x
        self.y = y - 20
        self.total_frames = 0
        self.frame = 0

        self.dir = -1
        if Finalbullet.image == None:
            Finalbullet.image = load_image('Resource/final_boss_bullet.png')

    def update(self, frame_time):
        speed = Bullet.BULLET_SPEED_PPS * frame_time
        self.x += (self.dir * speed)
        self.total_frames += Bullet.FRAMES_PER_ACTION * Bullet.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 1


    def draw(self):
        self.image.clip_draw(self.frame * 100, 0,100,100,self.x,self.y)


    def get_bb(self):
        return self.x - 50, self.y - 30, self.x -50, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


