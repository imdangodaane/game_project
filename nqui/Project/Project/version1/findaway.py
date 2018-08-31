# Import section
import os
import sys
import math
import random

import pyglet
from pyglet.window import key
from pyglet.gl import *
# from pyglet import resource


PLAYER_SCALE = 0.5
PLAYER_WALK_SPEED = 5


def center_image(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

# --------------------------------------------------------------------------
# Game objects
# --------------------------------------------------------------------------

def wrap(value, width):
	if value > width:
		value -= width
	if value < 0:
		value += width
	return value


def to_radians(degrees):
    return math.pi * degrees / 180.0


class WrappingSprite(pyglet.sprite.Sprite):
        dx = 0
        dy = 0

        def __init__(self, img, x, y, batch=None):
            super(WrappingSprite, self).__init__(img, x, y, batch=batch)
            self.collision_radius = self.image.width // COLLISION_RESOLUTION // 2
        def update(self, dt):
            x = self.x + self.dx * dt
            y = self.y + self.dy * dt
            self.x = wrap(x, ARENA_WIDTH)
            self.y = wrap(y, ARENA_HEIGHT)

        def collision_cells(self):
            cellx = int(self.x + 130)
            celly = int(self.y + 130)
            for y in range(y, celly):
                for x in range(x, cellx):
                    yield x, y



# Find object cells
def find_object_cells(x, y, size):
    list_cells = []
    last_cellx = x + size
    last_celly = y + size
    for j in range(y, last_celly):
        for i in range(x, last_cellx):
            list_cells.append((j, i))
    return list_cells


# Window width and height
width, height = 800, 600

# Initial window
game_window = pyglet.window.Window(width, height)

# Handle key press
keys = key.KeyStateHandler()
game_window.push_handlers(keys)

# Load background image
background_img = pyglet.image.load("resources/background.png")
background = pyglet.sprite.Sprite(img=background_img)

# Load image
stand_front_img = pyglet.image.load("resources/stand_front.png")
stand_back_img = pyglet.image.load("resources/stand_back.png")
stand_left_img = pyglet.image.load("resources/stand_left.png")
stand_right_img = pyglet.image.load("resources/stand_right.png")
walk_front_img = pyglet.image.load_animation("resources/walk_front.gif")
walk_back_img = pyglet.image.load_animation("resources/walk_back.gif")
walk_left_img = pyglet.image.load_animation("resources/walk_left.gif")
walk_right_img = pyglet.image.load_animation("resources/walk_right.gif")
# Load enemy
enemy_img = pyglet.image.load_animation("resources/shark.gif")

# HP bar
HP = pyglet.text.Label("1000", font_size=36, x=0, y=550)

# Centered image
image_list = [stand_front_img,
              stand_back_img,
              stand_left_img,
              stand_right_img]
for i in image_list:
    center_image(i)


# Default player
player = pyglet.sprite.Sprite(img=walk_front_img)
player.scale = PLAYER_SCALE

# Default enemy
enemy = pyglet.sprite.Sprite(img=enemy_img)

# HP def check:

# Update
def update(dt):
    global player
    global enemy
    player_cells = find_object_cells(player.x, player.y, 65)
    enemy_cells = find_object_cells(enemy.x, enemy.y, 236)
    intersection_cells = set(player_cells).intersection(enemy_cells)
    if intersection_cells:
        HP.text = str(int(HP.text) - 10)
    if keys[key.UP]:
        if (intersection_cells):
            player.y -= PLAYER_WALK_SPEED * 5
            intersection_cells = set(player_cells).intersection(enemy_cells)
        if player.y + 65 > height:
            player.y -= PLAYER_WALK_SPEED
        else:
            player = pyglet.sprite.Sprite(img=walk_back_img, x=player.x, y=player.y)
            player.scale = PLAYER_SCALE
            player.y += PLAYER_WALK_SPEED
    if keys[key.DOWN]:
        if (intersection_cells):
            player.y += PLAYER_WALK_SPEED * 5
            intersection_cells = set(player_cells).intersection(enemy_cells)
        if player.y < 0:
            player.y += PLAYER_WALK_SPEED
        else:
            player = pyglet.sprite.Sprite(img=walk_front_img, x=player.x, y=player.y)
            player.scale = PLAYER_SCALE
            player.y -= PLAYER_WALK_SPEED
    if keys[key.RIGHT]:
        if (intersection_cells):
            player.x -= PLAYER_WALK_SPEED * 5
            intersection_cells = set(player_cells).intersection(enemy_cells)
        if player.x + 65 > width:
            player.x -= PLAYER_WALK_SPEED
        else:
            player = pyglet.sprite.Sprite(img=walk_right_img, x=player.x, y=player.y)
            player.scale = PLAYER_SCALE
            player.x += PLAYER_WALK_SPEED
    if keys[key.LEFT]:
        if (intersection_cells):
            player.x += PLAYER_WALK_SPEED * 5
            intersection_cells = set(player_cells).intersection(enemy_cells)
        if player.x < 0:
            player.x += PLAYER_WALK_SPEED
        else:
            player = pyglet.sprite.Sprite(img=walk_left_img, x=player.x, y=player.y)
            player.scale = PLAYER_SCALE
            player.x -= PLAYER_WALK_SPEED
    print(intersection_cells)

# Window event
@game_window.event
def on_draw():
    game_window.clear()
    background.draw()
    HP.draw()
    player.draw()
    enemy.draw()
    for shark in sharks:
        shark.draw()

# @game_window.event
# def on_key_press(symbol, modifiers):


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()
