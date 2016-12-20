import random
from pico2d import *
from player import *



class Mush:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.8
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4
    FRAMES_PER_DIE = 3

    image = None
    die = None
    hit = None
    # sound
    hit_sound = None
    die_sound = None

    def __init__(self):
        self.x, self.y = random.randint(130, 850), 110
        self.frame = 0
        self.dir = -1
        self.fy = 0
        #
        self.hp = 6
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

        if Mush.image == None:
            Mush.image = load_image('resource/mush_run.png')
        if Mush.die == None:
            Mush.die = load_image('resource/mush_die.png')
        if Mush.hit == None:
            Mush.hit = load_image('resource/mush_hit.png')
            # sound
        if Mush.hit_sound == None:
            Mush.hit_sound = load_wav("sound/hit.wav")
            Mush.hit_sound.set_volume(32)
        if Mush.die_sound == None:
            Mush.die_sound = load_wav("sound/yang_death.wav")
            Mush.die_sound.set_volume(32)

    def update(self, frame_time):
        global player
        player = Player()
        player.x, player.y = player.get_xy()

        self.life_time += frame_time
        self.speed = Mush.RUN_SPEED_PPS * frame_time
        self.total_frames += Mush.FRAMES_PER_ACTION * Mush.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.die_frame = int(self.total_die) % 3

        if self.s_die == True:
            self.d_time += frame_time
            self.total_die += Mush.FRAMES_PER_DIE * Mush.ACTION_PER_TIME * frame_time
            if self.d_time >= 0.8:
                self.life_flag = False
                self.d_time = 0
        if self.s_hit == True:
            self.h_time += frame_time
            if self.h_time >= 0.3:
                self.h_time = 0
                self.s_hit = False

        if (self.x < 180) :
            self.dir = 1
            self.fy = 1
        elif (self.x > 900)  :
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
            self.die.clip_draw(self.die_frame * 100, self.frame_die * 65, 100, 65, self.x, self.y)
        elif self.s_hit == True:
            self.hit.clip_draw(0, self.frame_hit * 80, 100, 65, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, self.fy* 80, 100, 65, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 30, self.x + 35, self.y + 30

    def handle_event(self, event):
        pass

###############################################################
class Mushskill:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 30.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_SKILL = 12
    SKILL_PER_TIME = 1.0 / 1.5

    image = None
    skill = None
    # sound
    hit_sound = None
    die_sound = None

    def __init__(self):
        #skill
        self.x = 1200
        self.y = 235
        self.skill_time = 0
        self.skill_frame = 0
        self.b_skill = False
        self.b_skill1 = False
        self.b_patt = False
        self.total_skill = 0.0

        if  Mushskill.skill == None:
            Mushskill.skill = load_image("Resource/summon_skill.png")


    def update(self, frame_time):
        self.skill_frame = int(self.total_skill) % 12


        if self.b_skill1 == True:
            self.total_skill +=  Mushskill.FRAMES_PER_SKILL *  Mushskill.SKILL_PER_TIME* frame_time
            self.skill_time += frame_time
            if self.skill_time >= 1.5:
                self.total_skill = 0
                self.skill_time = 0
                self.b_skill1 = False


    def summonning1(self):
        self.b_skill1 = True

    def draw(self):

        if self.b_skill1 == True:
             self.skill.clip_draw(self.skill_frame * 200, 0,200,278,210,180)
             self.skill.clip_draw(self.skill_frame * 200, 0,200,278,400,180)
             self.skill.clip_draw(self.skill_frame * 200, 0,200,278,740,180)
             self.skill.clip_draw(self.skill_frame * 200, 0,200,278,910,180)


    def get_skill_1(self):
        if self.skill_time >= 0.65:
            return 170, 120 , 240, 220
    def get_skill_2(self):
        if self.skill_time >= 0.65:
            return 360, 120 , 430, 220
    def get_skill_3(self):
        if self.skill_time >= 0.65:
            return 700, 120 , 770, 220
    def get_skill_4(self):
        if self.skill_time >= 0.65:
            return 880, 120 , 950, 220


    def draw_bb(self):
        if self.b_skill1 == True:
            if self.skill_time >= 0.65:
                draw_rectangle(*self.get_skill_1())
                draw_rectangle(*self.get_skill_2())
                draw_rectangle(*self.get_skill_3())
                draw_rectangle(*self.get_skill_4())






