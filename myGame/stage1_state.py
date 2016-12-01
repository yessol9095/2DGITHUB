import random
import json
import os
from pico2d import *
from bullet import *


import game_framework
import title_state
import stage2_state



from player import Player
from sheep import Sheep


player = None
tile = None
background = None
sheeps = None
bullets = None
portal = None



class Portal:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    def __init__(self):
        self.image = load_image('Resource/portal.png')
        self.px = 1300
        self.py = 200
        #
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        #
        self.total_frames = 0
        self.frame = 0
        self.next = None
    def update(self, frame_time):
        self.total_frames += Portal.FRAMES_PER_ACTION * Portal.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 5
        self.left = clamp(0, int(self.set_center_object.x) - self.canvas_width // 2, self.w - self.canvas_width)
    def draw(self):
        sx = self.x - self.left
        self.portal.clip_draw(self.frame * 125, 0, 125, 75, sx + 3775, 185)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - self.left
        return 3745 + sx, 160, 3800 + sx, 185

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
        return 510, 0, 600, 100

    def get_dd(self):
        return 600, 0, 1400, 160

class Background:
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    SCROLL_SPEED_KMPH = 10.0  # Km / Hour
    SCROLL_SPEED_MPM = (SCROLL_SPEED_KMPH * 1000.0 / 60.0)
    SCROLL_SPEED_MPS = (SCROLL_SPEED_MPM / 60.0)
    SCROLL_SPEED_PPS = (SCROLL_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self,w,h):
        self.image = load_image('Resource/Background.png')
        self.speed = 0
        self.left = 0
        self.height = 95
        self.screen_width = w
        self.screen_height = h

    def draw(self):
        x = int(self.left)
        w = min(self.image.w - x, self.screen_width)
        self.image.clip_draw_to_origin(x, 0, w, self.screen_height, 0, 0)
        self.image.clip_draw_to_origin(0, 0, self.screen_width - w, self.screen_height, w, 0)

def create_world():
    global player, tile, background, sheeps, bullets, portal
    portal = Portal()
    player = Player()
    tile = Tile()
    background = Background()
    sheeps = [Sheep() for i in range(10)]
    bullets = list()



def destroy_world():
    global player, background, tile, sheeps, portal

    del(player)
    del(background)
    del(tile)
    del(portal)
    del(sheeps)


def shooting():
    global bullets
    bullets.append(Bullet(player.x,player.y,player.state))

def enter():
    open_canvas(1500,600)
    game_framework.reset_time()
    create_world()

def handle_events(self,frame_time):
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
                game_framework.push_state(stage2_state)
    if event.type == SDL_KEYDOWN:
        if event.key == SDLK_LEFT:
            self.speed -= Background.SCROLL_SPEED_PPS
        elif event.key == SDLK_RIGHT:
            self.speed += Background.SCROLL_SPEED_PPS
    if event.type == SDL_KEYUP:
        if event.key == SDLK_LEFT:
            self.speed += Background.SCROLL_SPEED_PPS
        elif event.key == SDLK_RIGHT:
            self.speed -= Background.SCROLL_SPEED_PPS




def exit():
    destroy_world()
    close_canvas()

def Map_collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if right_a > right_b and bottom_a == 40 : return 1
    if left_a < left_b and bottom_a  == 40  : return 1

    left_b, bottom_b, right_b, top_b = b.get_cc()
    if right_a > right_b  and bottom_a == 110  : return 1
    if right_a < right_b and right_a > left_b + 5 and bottom_a > top_b: return 2
    if right_a < left_b + 5  and bottom_a==110: return 3

    left_b, bottom_b, right_b, top_b = b.get_dd()
    if right_a > right_b  and bottom_a == 160  : return 1
    if right_a < right_b and right_a > left_b + 5 and bottom_a > top_b and left_a < left_b: return 4
    if right_a < left_b + 5  and bottom_a == 160: return 5

def Sheep_collide(a, b):
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

def update(self,frame_time):
    self.left = (self.left + frame_time * self.speed) % self.image.w
    player.update(frame_time)
    if Map_collide(player, tile)==1:
        player.dir = 0
    if Map_collide(player, tile) == 2:
        player.y = player.fy = 110 + 50
    if Map_collide(player, tile) == 3:
        player.y = player.fy = 40 + 50
        player.x -= 3
    if Map_collide(player, tile) == 4:
        player.y = player.fy = 160 + 50
        print(player.y)
        print(player.fy)
    if Map_collide(player, tile) == 5:
        player.y = player.fy = 110 + 50
        player.x -= 3
    for sheep in sheeps:
        sheep.update(frame_time)
    for bullet in bullets:
        bullet.update(frame_time)
    for sheep in sheeps:
        for bullet in bullets:
            if Sheep_collide(bullet, sheep):
                sheep.death()
                bullets.remove(bullet)
            if sheep.life_flag == False:
                sheeps.remove(sheep)
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
    player.draw()
    player.draw_bb()
    for sheep in sheeps:
        sheep.draw()
    for sheep in sheeps:
        sheep.draw_bb()
    for bullet in bullets:
        bullet.draw()
    for bullet in bullets:
        bullet.draw_bb()
    update_canvas()