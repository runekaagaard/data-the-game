from ctypes import *
import math
import sys

import pyglet
from cocos.sprite import Sprite

sprites = {}

def add_collision_map(sprite, name):
    sprites[name] = {}
    sprites[name]['sprite'] = sprite
    sprites[name]['texture'] = sprites[name]['sprite']._texture
    sprites[name]['width'] = sprites[name]['texture'].width 
    sprites[name]['width_half'] = math.floor(sprites[name]['texture'].width / 2)
    sprites[name]['height'] = sprites[name]['texture'].height
    sprites[name]['height_half'] = math.floor(sprites[name]['texture'].height 
                                                                            / 2)
    sprites[name]['alpha'] = sprites[name]['texture'].get_image_data().get_data(
                                                    'A', sprites[name]['width'])
    sprites[name]['c_ubyte'] = cast(sprites[name]['alpha'], POINTER(c_ubyte))
    
def does_collide(plane):
    for i in range(0, sprites['plane']['width']):
        for j in range(0, sprites['plane']['height']):
            if sprites['plane']['c_ubyte'][i + j * sprites['plane']['width']]:
                p = plane.point_to_world((i - sprites['plane']['width_half'],
                                          j - sprites['plane']['height_half']))
                if sprites['level']['c_ubyte'][int(p[0]) + int(p[1]) \
                                                   * sprites['level']['width']]:
                    return True
    return False
