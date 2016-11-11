import game_framework
import title_state
from pico2d import *


name = "StartState"
image = None
logo_time = 0.0


def enter():
    global image
    open_canvas(1500, 600)
    game_framework.reset_time()
    image = load_image('Resource/kpu_credit.png')


def exit():
    global image
    del(image)

def update(frame_time):
    global logo_time

    if (logo_time > 1.0):
        logo_time = 0
       #  game_framework.quit()
        game_framework.push_state(title_state)
    delay(0.01)
    logo_time += 0.01


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(1500, 600)
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    pass


def pause(): pass


def resume(): pass




