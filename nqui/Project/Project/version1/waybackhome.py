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
SHARK_SIZE = 236


def center_image(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

# --------------------------------------------------------------------------
# Game objects
# --------------------------------------------------------------------------

# Find object cells
def find_object_cells(x, y, size):
    list_cells = []
    last_cellx = x + size
    last_celly = y + size
    for j in range(y, last_celly):
        for i in range(x + 25, last_cellx - 25):
            list_cells.append((j, i))
    return list_cells


# Window width and height
width, height = 1280, 720

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
coral_image = pyglet.image.load_animation("resources/coral.gif")
seaweed_image = pyglet.image.load_animation("resources/seaweed.gif")
shark_image = pyglet.image.load_animation("resources/shark.gif")
flag_image = pyglet.image.load_animation("resources/flag.gif")
# coral.x = 720 - 368

# Make static objects
coral = pyglet.sprite.Sprite(img=coral_image)
seaweed = pyglet.sprite.Sprite(img=seaweed_image)
shark = pyglet.sprite.Sprite(img=shark_image)
flag = pyglet.sprite.Sprite(img=flag_image, x=width-200, y=random.randint(0, 500))
sharks = pyglet.graphics.Batch()
seaweeds = pyglet.graphics.Batch()

# Global variables
list_shark_cells = []

# HP bar
HP = pyglet.text.Label("1000", font_size=36, x=50, y=height-40)
win = pyglet.text.Label("", font_size=100, x=width/2 - 100, y=height/2 - 100)


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

flag_cells = find_object_cells(flag.x, flag.y, 200)

# HP def check:

# Print seaweed
seaweed_list = []
for i in range(7):
    x,y = i * 100, -10
    seaweed_list.append(pyglet.sprite.Sprite(seaweed_image, x, y, batch=seaweeds))

for m in range(7):
    seaweed_list[m].scale = 0.7

# Distance and print shark
def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

def make_sharks(num):
    global list_shark_cells
    shark_sprites = []
    shark_sprites.append(shark)
    size = [1, 0.7, 0.5]
    (x, y) = (0, 0)
    i = 0
    while len(shark_sprites) < num:
        i += 1
        x = random.randint(1, 10) * random.randint(0, 120)
        y = random.randint(1, 10) * random.randint(0, 60)
        append = True
        for j in range(len(shark_sprites)):
            if distance((x, y), (shark_sprites[j].x, shark_sprites[j].y)) < 250:
                append = False
                break
        if append:
            shark_sprites.append(pyglet.sprite.Sprite(shark_image, x, y, batch=sharks))
        if i == 1000:
            break

    # for m in range(num - 2):
    for m in range(1, len(shark_sprites)):
        a = random.randint(0, 2)
        shark_sprites[m].scale = size[a]
        list_shark_cells += find_object_cells(shark_sprites[m].x,
                                                   shark_sprites[m].y,
                                                   int(SHARK_SIZE * size[a]))
        # shark_sprites[m].scale = size[random.randint(0, 2)]
    return sharks
sharks = make_sharks(100)

# Update
def update(dt):
    global player
    global list_shark_cells
    player_cells = find_object_cells(player.x, player.y, 55)
    # list_shark_cells = set(list_shark_cells)
    intersection_cells = set(player_cells).intersection(list_shark_cells)
    win_cells = set(player_cells).intersection(flag_cells)
    if win_cells:
        win.text = "YOU WIN"
    if intersection_cells:
        HP.text = str(int(HP.text) - 10)
    if keys[key.UP]:
        if (intersection_cells):
            player.y -= PLAYER_WALK_SPEED * 10
            intersection_cells = set(player_cells).intersection(list_shark_cells)
        if player.y + 65 > height:
            player.y -= PLAYER_WALK_SPEED
        else:
            player = pyglet.sprite.Sprite(img=walk_back_img, x=player.x, y=player.y)
            player.scale = PLAYER_SCALE
            player.y += PLAYER_WALK_SPEED
    if keys[key.DOWN]:
        if (intersection_cells):
            player.y += PLAYER_WALK_SPEED * 10
            intersection_cells = set(player_cells).intersection(list_shark_cells)
        if player.y < 0:
            player.y += PLAYER_WALK_SPEED
        else:
            player = pyglet.sprite.Sprite(img=walk_front_img, x=player.x, y=player.y)
            player.scale = PLAYER_SCALE
            player.y -= PLAYER_WALK_SPEED
    if keys[key.RIGHT]:
        if (intersection_cells):
            player.x -= PLAYER_WALK_SPEED * 10
            intersection_cells = set(player_cells).intersection(list_shark_cells)
        if player.x + 65 > width:
            player.x -= PLAYER_WALK_SPEED
        else:
            player = pyglet.sprite.Sprite(img=walk_right_img, x=player.x, y=player.y)
            player.scale = PLAYER_SCALE
            player.x += PLAYER_WALK_SPEED
    if keys[key.LEFT]:
        if (intersection_cells):
            player.x += PLAYER_WALK_SPEED * 10
            intersection_cells = set(player_cells).intersection(list_shark_cells)
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
    flag.draw()
    HP.draw()
    coral.draw()
    seaweeds.draw()
    sharks.draw()
    player.draw()
    win.draw()

# @game_window.event
# def on_key_press(symbol, modifiers):


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()
