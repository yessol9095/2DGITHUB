import random
import json
import os
import temp
from pico2d import *

import game_framework
import stage1_state
import stage2_state
import stage3_state
import start_state
import title_state
from player import Player


init = None
name = "gameover"
image = None
gameover_sound = None
player_hp = 0


def enter():
    global image,character_hp, gameover_sound
    if image == None:
        image = load_image('Resource/gameover.png')
    if init == None:
        player_hp = 0
    gameover_sound = load_music("Sound/gameover.mp3")
    gameover_sound.set_volume(64)
    gameover_sound.play()




def exit():
    global image
    del(image)


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type,event.key) == (SDL_KEYDOWN,SDLK_ESCAPE):
                game_framework.quit()


def draw(frame_time):
    clear_canvas()
    image.draw(750,300)
    update_canvas()


def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass


