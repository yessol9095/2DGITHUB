import random

from pico2d import *
from bullet import Bullet

bullet = None

class Player:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    image = None
    jump = None
    attack = None
    death = None
    hp_title= None
    hp = None
    death_screen = None
    #sound
    # sound
    jump_sound = None
    shoot_sound = None
    die_sound = None

    R_STAND, R_WALK, L_STAND, L_WALK = 0, 1, 2, 3

    def __init__(self):
        self.x, self.y = 100, 90
        self.frame = 0
        self.fy = 90
        #
        self.life = 5
        self.b_death = False
        self.b_hp = False
        #
        self.py = 0
        self.life_time = 0.0
        self.total_frames = 0.0
        self.dir = 0
        self.state = self.R_STAND
        #JUMP
        self.up_check = 3
        self.j_time = 0
        self.b_jump = False
        self.frame_jump = 0
        # attack
        self.a_time = 0
        self.b_attack = False
        self.frame_attack = 0
        # portal
        self.next = False
        if Player.image == None:
            Player.image = load_image('Resource/moving.png')
        if Player.jump == None:
            Player.jump = load_image('Resource/jump.png')
        if Player.attack == None:
            Player.attack = load_image('Resource/attack.png')
        if Player.hp_title == None:
            Player.hp_title = load_image('Resource/Hp_Title.png')
        if Player.hp == None:
            Player.hp = load_image('Resource/Hp.png')
        if Player.death == None:
            Player.death = load_image("Resource/Death.png")
        #sound
        if Player.jump_sound == None:
            Player.jump_sound = load_wav("sound/jump.wav")
            Player.jump_sound.set_volume(62)
        if Player.shoot_sound == None:
            Player.shoot_sound = load_wav("sound/shoot.wav")
            Player.shoot_sound.set_volume(32)
        if Player.die_sound == None:
            Player.die_sound = load_wav("sound/character_die.wav")
            Player.die_sound.set_volume(32)


    def set_background(self, bg):
        self.bg = bg

    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.life_time += frame_time
        self.speed = Player.RUN_SPEED_PPS * frame_time
        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += (self.dir * self.speed)

        #jump
        if self.b_jump == True:
            self.j_time += 0.1
            self.y -= -13 + (0.98 * self.j_time * self.j_time) / 2
            if self.y <= self.fy:
                self.j_time = 0
                self.b_jump = False
                self.y = self.fy
            else: # 중력 적용
                self.y += -9 + (0.98) / 2
                # attack
        if self.b_attack == True:
            self.a_time += frame_time
            if self.a_time >= 0.5:
                self.a_time = 0
                self.b_attack = False
        #if self.life < 0 :
            #self.b_death = True
            #self.die_sound.play()

    def die(self):
        if self.b_hp == False:
            self.life -= 1
            self.b_hp = True
        #self.b_death = True

    def draw(self):

        if self.b_jump == True:
            self.jump.clip_draw(0, self.frame_jump * 100, 100, 100, self.x, self.y)
        elif self.b_attack == True:
            self.attack.clip_draw(0, self.frame_attack * 100, 100, 100,self.x, self.y)
        elif self.b_death == True:
            self.death.clip_draw(0, 0, 101, 47, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, self.state * 125, 100, 100, self.x, self.y)
        self.hp_title.clip_draw(0, 0, 244, 35, 150, 550 )
        self.hp.clip_draw(0, 0 , self.life * 30, 25, 150, 550)

    def place(self):
        return self.x, self.y

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 25, self.y + 50

    def get_xy(self):
        return self.x, self.y

    def handle_event(self, event):
        global bullet
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.R_STAND, self.L_STAND, self.R_WALK):
                self.state = self.L_WALK
                self.dir = -1
                self.frame_attack = 1
                self.frame_jump = 1
                self.b_hp = False
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.R_STAND, self.L_STAND, self.L_WALK):
                self.state = self.R_WALK
                self.dir = 1
                self.frame_attack = 0
                self.frame_jump = 0
                self.b_hp = False
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.L_WALK,):
                self.state = self.L_STAND
                self.dir = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.R_WALK,):
                self.state = self.R_STAND
                self.dir = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            self.b_jump = True
            self.jump_sound.play()
            self.b_hp = False
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
            self.b_attack = True
            self.shoot_sound.play()
            self.b_hp = False
            if self.life < 1:
                self.life = 5
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_x):
            self.b_attack = False
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            self.next = True









