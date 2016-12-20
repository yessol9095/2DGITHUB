import random
import json
import os
import temp
from pico2d import *
from bullet import *
from player import Player
from finalboss import Finalbullet
from finalboss import Finalboss
import gameover
import game_framework
import title_state


finalboss = None
player = None
bullets = None
finalbullet = None
final_sound = None
restart = None


class Restart:
    def __init__(self):
        self.image = load_image('Resource/Die.png')
    def draw(self):
        self.image.clip_draw(0, 0, 774, 684, 750, 300)


class Background:
    def __init__(self):
        self.image = load_image('Resource/Stage3.png')
        self.bx = 700
        self.by = 300
    def draw(self):
        self.image.clip_draw(0, 0, 1500, 600, self.bx, self.by)

class Sky:
    def __init__(self):
        self.image = load_image('Resource/Background2.png')
        self.bx = 750
        self.by = 300
    def draw(self):
        self.image.clip_draw(0, 0, 1500, 600, self.bx, self.by)

def create_world():
    global player, background, bullets, sky, finalboss, final_sound, finalbullets,restart
    restart = Restart()
    player = Player()
    background = Background()
    sky = Sky()
    bullets = list()
    finalbullets = list()
    finalboss = Finalboss()
    player.x, player.y = 50, 80
    player.life = temp.player_life
    final_sound = load_music("Sound/final_stage.mp3")
    final_sound.set_volume(64)
    final_sound.repeat_play()
    Player.jump_sound = None
    Player.shoot_sound = None
    Player.image = None
    Player.jump = None
    Player.attack = None
    Player.hp_title = None
    Player.hp = None

def destroy_world():
    global player, background,sky,finalboss
    del(finalboss)
    del(player)
    del(background)
    del(sky)


def shooting():
    global bullets
    Bullet.image = load_image('Resource/bullet.png')
    bullets.append(Bullet(player.x,player.y,player.state))

def final_shooting():
    global finalbullets
    Finalbullet.image = load_image('Resource/final_boss_bullet.png')
    finalbullets.append(Finalbullet(finalboss.x, finalboss.y))

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

def Boss_collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True

def update(frame_time):
    global restartimage
    player.update(frame_time)
    if player.life > 0:
        finalboss.update(frame_time)
        for bullet in bullets:
            bullet.update(frame_time)
        for finalbullet in finalbullets:
            finalbullet.update(frame_time)
            if Boss_collide(player,finalbullet):
                player.die()
        if player.b_death == False:
            if Boss_collide(player, finalboss):
                    player.die()
            if finalboss.s_die == False:
                for bullet in bullets:
                    if Boss_collide(finalboss, bullet):
                        finalboss.hurt()
                        if bullets.count(bullet) > 0:
                            bullets.remove(bullet)
                        if finalboss.life <= 0:
                            finalboss.death()
                    if finalboss.life_flag == False:
                        finalboss.remove(finalboss)
        if finalboss.life_flag != False:
            if int(get_time() % 8) == 0:
                final_shooting()
        if finalboss.life < 1:
            delay(0.1)
            game_framework.push_state(gameover)
    pass

def pause():
    pass


def resume():
    pass

def draw(frame_time):
    clear_canvas()
    sky.draw()
    background.draw()
    if finalboss.life_flag != False:
        finalboss.draw()
    finalboss.draw_bb()
    if finalboss.life_flag != False:
        for finalbullet in finalbullets:
            finalbullet.draw()
    for finalbullet in finalbullets:
        finalbullet.draw_bb()
    for bullet in bullets:
        bullet.draw()
    for bullet in bullets:
        bullet.draw_bb()
    player.draw()
    player.draw_bb()
    if player.life < 1:
        restart.draw()
    update_canvas()