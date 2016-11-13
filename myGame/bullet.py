from pico2d import*
from bullet import *

class Bullet:
    PIXEL_PER_METER = (10.0 / 0.3 )         # 10 pixel 30cm
    BULLET_SPEED_KMPH = 60.0                   # km / Hour
    BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
    BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
    BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2
    BULLET_SPEED = 5

    image = None

    R_STAND, R_WALK, L_STAND, L_WALK = 0, 1, 2, 3

    def __init__(self,x,y,state):

        self.x = x
        self.y = y - 20
        self.total_frames = 0
        self.frame = 0
        self.state = state
        if self.state in (self.R_STAND,self.R_WALK):
            self.dir = 1
        elif self.state in(self.L_STAND,self.L_WALK):
            self.dir = -1
        if Bullet.image == None:
            Bullet.image = load_image('Resource/bullet.png')

    def update(self, frame_time):
        speed = Bullet.BULLET_SPEED_PPS * frame_time
        self.x += (self.dir * speed)
        self.total_frames += Bullet.FRAMES_PER_ACTION * Bullet.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 2


    def draw(self):
        if self.state in (self.R_STAND,self.R_WALK):
            self.image.clip_draw(self.frame * 100, 0,100,20,self.x,self.y)
        elif self.state in(self.L_STAND,self.L_WALK):
            self.image.clip_draw(self.frame * 100, 20,100,20,self.x,self.y)

    def get_bb(self):
        if self.state in (self.R_STAND,self.R_WALK):
            return self.x + 30, self.y - 5, self.x + 45, self.y + 5
        if self.state in(self.L_STAND,self.L_WALK):
            return self.x - 30, self.y - 5, self.x - 45, self.y + 5

    def draw_bb(self):
            draw_rectangle(*self.get_bb())






