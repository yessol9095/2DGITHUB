import random
import json
import os
import temp
from pico2d import *
from bullet import *
import gameover
import stage1_state
import stage3_state
import game_framework
import title_state

from player import Player
from mush import Mush
from mush import Mushskill
from skill import Skill

skill = None
player = None
tile = None
mushes = None
mushskills = None
bullets = None
portal = None
background = None
restart = None


class Restart:
    def __init__(self):
        self.image = load_image('Resource/Die.png')
    def draw(self):
        self.image.clip_draw(0, 0, 774, 684, 750, 300)

class Portal:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    def __init__(self):
        self.image = load_image('Resource/portal.png')
        self.px = 1340
        self.py = 60

        self.total_frames = 0
        self.frame = 0
        self.next = None
    def update(self, frame_time):
        self.total_frames += Portal.FRAMES_PER_ACTION * Portal.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 5

    def draw(self):
        self.image.clip_draw(self.frame * 125, 0, 125, 75, self.px, self.py)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.px - 35, self.py - 35, self.px + 35, self.py + 35

class Tile:
    def __init__(self):
        self.image = load_image('Resource/stage2.png')
        self.tx = 750
        self.ty = 300

    def draw(self):
        self.image.clip_draw(0, 0, 1500, 600, self.tx, self.ty)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_cc())
        draw_rectangle(*self.get_dd())

    def get_bb(self):
        return 0, 0, 150, 160

    def get_cc(self):
        return 150, 0, 920, 80

    def get_dd(self):
        return 920, 0, 1500, 30


class Background:
    def __init__(self):
        self.image = load_image('Resource/Background2.png')
        self.bx = 1024
        self.by = 300
    def draw(self):
        self.image.clip_draw(0, 0, 2048, 600, self.bx, self.by)

def create_world():
    global player, tile, background, bullets, portal, mushes, skill, mushskills, restart
    restart = Restart()
    mushes = [Mush() for i in range(5)]
    mushskills = Mushskill()
    skill = Skill()
    portal = Portal()
    player = Player()
    player.life = temp.player_life
    tile = Tile()
    background = Background()
    bullets = list()
    player.x, player.y = 50, 210
    #Player.image = None
    #Player.jump = None
    #Player.attack = None



def destroy_world():
    global player, background, tile, portal, mushes, skill, mushskills

    del(skill)
    del(player)
    del(background)
    del(tile)
    del(portal)
    del(mushes)
    del(mushskills)

def shooting():
    global bullets
    Bullet.image = load_image('Resource/bullet.png')
    bullets.append(Bullet(player.x,player.y,player.state))

def enter():
    clear_canvas()
    game_framework.reset_time()
    create_world()

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)
            if player.b_attack == True:
                shooting()
            if player.next == True and Portal_collide(player, portal):
                temp.player_life = player.life
                game_framework.push_state(stage3_state)



def exit():
    destroy_world()
    close_canvas()

def Map_collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()

    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a < left_b and bottom_a == 160: return 1
    if left_a + 5 > right_b and bottom_a == 160 and right_a > right_b : return 2
    if top_b < bottom_a and left_a < right_b and right_a > right_b: return 4

    left_b, bottom_b, right_b, top_b = b.get_cc()
    if left_a < left_b and bottom_a == 80: return 1
    if left_a > right_b and bottom_a == 80 : return 3
    if top_b < bottom_a and left_a < right_b and right_b < right_a: return 5


    left_b, bottom_b, right_b, top_b = b.get_dd()
    if left_a < left_b and bottom_a == 30: return 1
    if right_a > right_b and bottom_a == 30: return 1

def Mush_collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True

def Portal_collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True
def skill1_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_skill_1()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def skill2_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_skill_2()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def skill3_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_skill_3()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def skill4_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_skill_4()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def update(frame_time):
    global restartimage
    player.update(frame_time)
    if player.life > 0:
        skill.update(frame_time)
        mushskills.update(frame_time)
        if player.b_death == False :
            if mushskills.b_skill1 == True:
                if mushskills.skill_time >= 0.65:
                    if skill1_collide(player, mushskills):
                        player.die()
                    if skill2_collide(player, mushskills):
                        player.die()
                    if skill3_collide(player, mushskills):
                        player.die()
                    if skill4_collide(player, mushskills):
                        player.die()
        if Map_collide(player, tile) == 1:
            player.dir = 0
        if Map_collide(player, tile) == 2:
            player.y = player.fy = 130
            player.x += 3
        if Map_collide(player, tile) == 5:
            player.y = player.fy = 130
            player.x -= 1
        if Map_collide(player, tile) == 3:
            player.y = player.fy = 80
            player.x += 3
        if Map_collide(player, tile) == 4:
            player.y = player.fy = 210
            player.x -= 3



        for mush in mushes:
            mush.update(frame_time)
            if player.b_death == False:
                if Mush_collide(player, mush):
                    player.die()

        for bullet in bullets:
            bullet.update(frame_time)
            for mush in mushes:
                if mush.s_die == False:
                    if Mush_collide(mush, bullet):
                        mush.hurt()
                        if bullets.count(bullet) > 0:
                            bullets.remove(bullet)
                        if mush.hp <= 0:
                            mush.death()
                if mush.life_flag == False:
                    mushes.remove(mush)

        if int(get_time() % 12) == 0:
            mushskills.summonning1()
        if int(get_time() % 12) == 9:
            mushskills.summonning1()

        portal.update(frame_time)
    pass

def pause():
    pass


def resume():
    pass

def draw(frame_time):
    clear_canvas()
    background.draw()
    tile.draw()
    tile.draw_bb()
    portal.draw()
    portal.draw_bb()
    skill.draw()
    skill.draw_bb()
    mushskills.draw()
    mushskills.draw_bb()

    for mush in mushes:
        mush.draw()
    for mush in mushes:
        mush.draw_bb()
    for bullet in bullets:
        bullet.draw()
    for bullet in bullets:
        bullet.draw_bb()
    player.draw()
    player.draw_bb()
    if player.life < 1:
        restart.draw()
    update_canvas()