import random
import json
import os
from pico2d import *
from bullet import *
from player import Player

import game_framework
import title_state

player = None
tile = None
bullets = None

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
    global player, tile, background, bullets
    player = Player()
    tile = Tile()
    background = Background()
    bullets = list()
    player.x, player.y = 50, 210
    Player.image = load_image('Resource/moving.png')
    Player.jump = load_image('Resource/jump.png')
    Player.attack = load_image('Resource/attack.png')



def destroy_world():
    global player, background, tile, portal, mushes, skill

    del(skill)
    del(player)
    del(background)
    del(tile)
    del(portal)
    del(mushes)

def shooting():
    global bullets
    Bullet.image = load_image('Resource/bullet.png')
    bullets.append(Bullet(player.x,player.y,player.state))

def enter():
    open_canvas(1500,600)
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
            #if player.next == True and Portal_collide(player, portal):
                #game_framework.change_state(stage1_state)



def exit():
    destroy_world()
    close_canvas()

def Map_collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()

    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a < left_b and bottom_a == 160: return 1
    if left_a + 5 > right_b and bottom_a == 160 : return 2

    left_b, bottom_b, right_b, top_b = b.get_cc()
    if left_a < left_b and bottom_a == 80: return 1
    if left_a + 5 > right_b and bottom_a == 80 : return 3

    left_b, bottom_b, right_b, top_b = b.get_dd()
    if left_a < left_b and bottom_a == 30: return 1
    if right_a > right_b and bottom_a == 30: return 1

def Portal_collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True

def update(frame_time):
    player.update(frame_time)
    skill.update(frame_time)
    if Map_collide(player, tile) == 1:
        player.dir = 0
    if Map_collide(player, tile) == 2:
        player.y = player.fy = 130
        player.x += 3
    if Map_collide(player, tile) == 3:
        player.y = player.fy = 80
        player.x += 3


    for bullet in bullets:
        bullet.update(frame_time)
    for mush in mushes:
        mush.update(frame_time)
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
    update_canvas()