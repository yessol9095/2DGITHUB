import game_framework
import player
import stage1_state
import stage2_state

from pico2d import *

init = None
player_life = 5
player_skill = 0

def enter():
    global player_life, player_skill
    if init == None:
        player_life = 5
        player_skill = 0


def exit():
    pass


def handle_events():
    pass


def draw():
    pass


def update():
    pass


def pause():
    pass


def resume():
    pass
