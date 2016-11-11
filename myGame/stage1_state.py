import random
import json
import os

from pico2d import *

import game_framework
import title_state
from player import Player
from sheep import Sheep
from bullet import Bullet

player = None
tile = None
background = None
sheeps = None
bullets = None

class Tile:
    def __init__(self):
        self.image = load_image('Resource/stage1.png')
        self.tx = 750
        self.ty = 300

    def draw(self):
        self.image.clip_draw(0, 0, 1500, 600, self.tx, self.ty)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_cc())
        draw_rectangle(*self.get_dd())

    def get_bb(self):
        return 0, 0, 510, 35

    def get_cc(self):
        return 600, 0, 1500, 160

    def get_dd(self):
        return 510, 0, 600, 100

class Background:
    def __init__(self):
        self.image = load_image('Resource/Background.png')
        self.bx = 1024
        self.by = 300
    def draw(self):
        self.image.clip_draw(0, 0, 2048, 600, self.bx, self.by)

def create_world():
    global player, tile, background, sheeps, bullets
    player = Player()
    tile = Tile()
    background = Background()
    sheeps = [Sheep() for i in range(10)]
    bullets = [Bullet() for i in range(10)]



def destroy_world():
    global player, background, tile, sheeps, bullets

    del(player)
    del(background)
    del(tile)
    del(sheeps)
    del(bullets)



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


def exit():
    destroy_world()
    close_canvas()

def Map_collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if right_a > right_b : return 1
    if left_a < left_b : return 1
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    left_b, bottom_b, right_b, top_b = b.get_cc()
    if right_a < right_b and left_a > left_b and bottom_a >= top_b: return 2
    if left_a < left_b : return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return 2
    left_b, bottom_b, right_b, top_b = b.get_dd()
    if right_a > right_b : return 1
    if left_a < left_b : return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def update(frame_time):
    player.update(frame_time)
    if Map_collide(player, tile)==1:
        player.dir = 0
    if Map_collide(player, tile) == 2:
        player.y = player.fy = 40
    for sheep in sheeps:
        sheep.update(frame_time)
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
    player.draw()
    player.draw_bb()
    for sheep in sheeps:
        sheep.draw()
    for sheep in sheeps:
        sheep.draw_bb()
    for bullet in bullets:
        bullet.draw()
    update_canvas()