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
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0, 1, 2, 3
    jump = None
    b_jump = False

    def __init__(self):
        self.x, self.y = 90, 195
        self.fy =  0
        self.frame = 0
        self.state = self.RIGHT_STAND
        self.image = load_image('Walking.png')

        # jump
        self.up_check = 3
        self.j_time = 0
        self.b_jump = False
        self.frame_jump = 0

        if self.image == None:
            self.image = load_image('Walking.png')
        if self.jump == None:
            self.jump = load_image('jump.png')

    def handle_events(self, event):
        if event.key ==  SDLK_UP:
            self.b_jump = True
            if self.state in (self.RIGHT_STAND,self.RIGHT_RUN,):
                self.frame_jump = 0
            elif self.state in (self.LEFT_STAND,self.LEFT_RUN,):
                self.frame_jump = 1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.LEFT_RUN, self.RIGHT_STAND,self.LEFT_STAND):
                self.state = self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_RUN, self.LEFT_STAND, self.RIGHT_STAND):
                self.state = self.LEFT_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN,):
                self.state = self.LEFT_STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN,):
                self.state = self.RIGHT_STAND
        pass
    def update(self):
        if self.state == self.RIGHT_RUN:
            self.frame = (self.frame + 1) % 3
            self.x += 10
            self.fy = 0
        elif self.state == self.LEFT_RUN:
            self.frame = (self.frame + 1) % 3
            self.x -= 10
            self.fy = 90
        elif self.b_jump == True:
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
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            exit()
        else:
           player.handle_events(event)
        pass

def update():
    player.update()


def draw():
    clear_canvas()
    background.draw()
    tile.draw()
    player.draw()
    update_canvas()





