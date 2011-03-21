import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import math

import pyglet
from pyglet import image, font
from pyglet.gl import *
from pyglet.window import key, Window

import cocos
from cocos.director import director
from cocos.actions import *
from cocos.director import director
from cocos.layer import Layer 
from cocos.scene import Scene
from cocos.sprite import Sprite

from collision import does_collide, add_collision_map

WIDTH = 1024
HEIGHT = 768

PLANE_X = WIDTH / 2 - 54
PLANE_Y = HEIGHT / 2 + 35

class DataTheGame(cocos.layer.Layer):
    is_event_handler = True
    dx = 0
    dy = 0
    keys = set()
    
    def __init__(self, director):
        self.director = director
        super(DataTheGame, self ).__init__()
        self.add_level()
        self.add_plane()
        self.schedule_interval(self.update, 0.02)
            
    def update(self, dt):
        if does_collide(self.plane):
            self.plane.do(MoveTo((PLANE_X,PLANE_Y), 0))
            self.dx = 0
            self.dy = 0
            return
            
        if key.LEFT in self.keys and not key.RIGHT in self.keys:
            self.plane.do(Rotate(-10, 0))
        elif key.RIGHT in self.keys:
            self.plane.do(Rotate(10, 0))
        if key.SPACE in self.keys:
            rot = math.radians(self.plane.rotation + 270)
            self.dx += math.cos(rot) / 200
            self.dy += -math.sin(rot) / 200
        else:
            self.dx *= 0.98
            self.dy *= 0.98
        self.dy -= 0.001
        self.plane.do(MoveBy((self.dx * 40, self.dy * 40), 0))
    
    def add_level(self):
        self.level = Sprite(pyglet.resource.image('gfx/level1.png'), 
                            anchor=(0,0))
        self.add(self.level)
        add_collision_map(Sprite(pyglet.resource.image(
                         'gfx/level1_collisionmap.png'), anchor=(0,0)), 'level')
        
    def add_plane(self):
        self.plane = Sprite(pyglet.resource.image('gfx/plane.png'), 
                            anchor=(5,6))
        self.plane.position = PLANE_X, PLANE_Y
        self.add(self.plane)
        add_collision_map(self.plane, 'plane')
        
    def on_key_press(self, key, modifiers): self.keys.add(key)
    def on_key_release(self, key, modifiers): self.keys.remove(key)
    
if __name__ == "__main__":
    director.init(width=WIDTH, height=HEIGHT, fullscreen=True)
    director.run(cocos.scene.Scene(DataTheGame(director)))
