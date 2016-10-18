import random
import json
import os

from pico2d import *

import game_framework
import title_state



name = "MainState"

player = None
background = None
tile = None

class Tile:
    def __init__(self):
        self.image = load_image('tile.png')
        self.tx = 400
        self.ty = 300

    def draw(self):
        self.image.clip_draw(0, 0, 800,600, self.tx, self.ty)

class Background:
    def __init__(self):
        self.image = load_image('Background.png')
        self.bx = 1125
        self.by = 300
    def draw(self):
        self.image.clip_draw(0, 0, 2250, 658, self.bx, self.by)

class Player:
    image = None
    jump = None
    b_jump = False
    right = True
    left = False

    def __init__(self):
        self.x, self.y = 90, 195
        self.fy =  0
        self.frame = 0
        self.image = load_image('Walking.png')

        # jump
        self.up_check = 3
        self.j_time = 0
        self.b_jump = False
        self.frame_jump = 0

        if Player.image == None:
            Player.image = load_image('Walking.png')
        if Player.jump == None:
            Player.jump = load_image('jump.png')

    def update(self):
        if self.right == True:
            self.x += 10
            self.fy = 0
            self.right = False
        elif self.left == True:
            self.x -= 10
            self.fy = 90
            self.left = False
        if self.b_jump == True:
            self.j_time += 0.5
            self.y -= -15 + (0.98 * self.j_time * self.j_time) / 2
            if self.y <= 195:
                self.j_time = 0
                self.b_jump = False
                self.y = 195

        delay(0.04)
    def draw(self):
        if self.b_jump == True:
            self.jump.clip_draw(0, self.frame_jump * 100, 100, 100, self.x, self.y)
        else :
            self.image.clip_draw(self.frame * 94 , self.fy, 94, 90, self.x, self.y)

    def handle_events(self,event):
        if event.type == SDL_KEYDOWN:
            self.frame = (self.frame + 1) % 3
            if event.key == SDLK_UP:
                self.b_jump = True
            elif event.key == SDLK_RIGHT:
                self.right = True
            elif event.key == SDLK_LEFT:
                self.left = True



def enter():
    global background ,player, tile
    tile = Tile()
    background = Background()
    player = Player()
    running = True

def exit():
    global background, Player
    del(background)
    del(player)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            exit()
        else:
           player.handle_events(event)


def update():
    player.update()


def draw():
    clear_canvas()
    background.draw()
    tile.draw()
    player.draw()
    update_canvas()





