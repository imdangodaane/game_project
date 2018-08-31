import pyglet


# Global variables
window = pyglet.window.Window(1366, 768)
label = pyglet.text.Label("0", font_size=36, x = window.width/2, y = window.height/2, anchor_x='center', anchor_y='center')
image = pyglet.image.load('images/grassMid.png')
sprite = pyglet.sprite.Sprite(img=image)
sprite.x = -70
sprite.dx = 200.0

def update(dt):
    sprite.x += sprite.dx * dt
    if sprite.x > window.width:
        sprite.x = -70

# Event callbacks
@window.event
def on_draw():
    window.clear()
    label.draw()
    sprite.draw()
 
# Game loop (loop? Why loop?)
def game_loop(_):
    label.text = str(int(label.text) + 1)

pyglet.clock.schedule(game_loop)
pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
