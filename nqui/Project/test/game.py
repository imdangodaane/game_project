import pyglet
from pyglet.window import key
from pyglet.window import mouse


window = pyglet.window.Window(800, 600)
label = pyglet.text.Label('Hello world',
                           font_name='Times New Roman',
                           font_size=36,
                           x=window.width/2, y=window.height/2,
                           anchor_x='center', anchor_y='center')
image = pyglet.resource.image('kitten.png')


@window.event
def on_draw():
    label.draw()
    image.blit(0, 0)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print('The "A" key was pressed.')
        image.blit(window.width/4, window.height/4)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print('The left mouse button was pressed.')
        window.clear()


pyglet.app.run()
