# Import section
import os
import sys
import math
import random

import pyglet
from pyglet.window import key
from pyglet.gl import *
# from pyglet import resource

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
	rotation_speed = 0

	def __init__(self, img, x, y, batch=None):
		super(WrappingSprite, self).__init__(img, x, y, batch=batch)
		self.collision_radius = self.image.width // COLLISION_RESOLUTION // 2

	def update(self, dt):
		x = self.x + self.dx * dt
		y = self.y + self.dy * dt

		self.x = wrap(x, ARENA_WIDTH)
		self.y = wrap(y, ARENA_HEIGHT)


# Window width and height
width, height = 800, 600

# Initial window
game_window = pyglet.window.Window(width, height)

# Handle key press
keys = key.KeyStateHandler()
game_window.push_handlers(keys)

# Load background image
background_img = pyglet.image.load("background.png")
background = pyglet.sprite.Sprite(img=background_img)

# Load image
player_image = pyglet.image.load("player.png")
player = pyglet.sprite.Sprite(img=player_image)
player.scale = 0.5

# Centered image

center_image(player)

# Update
def update(dt):
    if keys[key.UP]:
        player.y += 5
    if keys[key.DOWN]:
         player.y -= 5
    if keys[key.RIGHT]:
         # player = pyglet.sprite.Sprite(img=player_right_image, x=player.x, y=player.y)
         player.x += 5
    if keys[key.LEFT]:
         # player = pyglet.sprite.Sprite(img=player_left_image, x=player.x, y= player.y)
         player.x -= 5

# Window event
@game_window.event
def on_draw():
    game_window.clear()
    background.draw()
    player.draw()

# @game_window.event
# def on_key_press(symbol, modifiers):


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()
