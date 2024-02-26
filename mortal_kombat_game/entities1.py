import os
import sys
import math
import random

import pygame

#  from game1 import FPS
from scripts.utils import *


class PhysicsEntity:

    g = 9.8

    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        #self.air_time = 0
        self.jumpmovement = 0
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.flip_buffer = False
        self.duck = False
        self.duck_rev = False
        self.duck_count = 0
        self.set_action('idle')


    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.duck_rev = False
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1] - self.jumpmovement)
        if self.duck:
            if self.duck_count != 9:
                if self.duck_count == 0:
                    self.pos[1] += 22
                    self.size = (60, 107)
                if self.duck_count == 4:
                    self.pos[1] += 18
                    self.size = (62, 89)
                if self.duck_count == 8:
                    self.pos[1] += 18
                    self.size = (64, 71)
                self.duck_count += 1
        else:
            if self.duck_count != 0:
                self.duck_rev = True
                if self.duck_count == 9:                 
                    self.pos[1] -= 18
                    self.size = (62, 89)
                if self.duck_count == 5:
                    self.pos[1] -= 18
                    self.size = (60, 107)
                if self.duck_count == 1:
                    self.pos[1] -= 22
                    self.size = (63, 129)
                self.duck_count -= 1


        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        if entity_rect.colliderect(self.game.object.rect()):
            if frame_movement[0] > 0:
                entity_rect.right = self.game.object.rect().left
                self.collisions['right'] = True
            if frame_movement[0] < 0:
                entity_rect.left = self.game.object.rect().right
                self.collisions['left'] = True
            self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        if entity_rect.colliderect(self.game.object.rect()):
            if frame_movement[1] > 0:
                entity_rect.bottom = self.game.object.rect().top
                self.collisions['down'] = True
                #self.air_time = 0
            if frame_movement[1] < 0:
                entity_rect.top = self.game.object.rect().bottom
                self.collisions['up'] = True
            self.pos[1] = entity_rect.y
        #else:
            #self.jump = True
            #self.air_time += 1

        #if self.air_time == 0:
            #self.velocity[1] = 0
        #else:
            #self.velocity[1] = int(100 * self.g * (self.air_time ** 2 - (self.air_time - 1) ** 2) / 3 / self.game.FPS ** 2)

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.velocity[1] = min(5, self.velocity[1] + 0.15)
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.flip_buffer = self.flip

        self.animation.update()

    
    #def jump(self):
        #self.jumpmovement = int(5 * (self.air_time + 1) / self.game.FPS)

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.speed = 3
        self.air_time = 0
        self.jumps = 1
    
    def update(self, movement=(0, 0)):
        super().update(movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1



        if self.air_time > 4:
            self.set_action('jump')
        elif self.duck_rev:
            self.set_action('duck_rev')
        elif movement[0] != 0:
            if self.speed == 3:
                self.set_action('walk')
            elif self.speed == 7:   
                self.set_action('run')
        elif self.duck:
            self.set_action('duck')
        else:
            self.set_action('idle')


    def jump(self):
        if self.jumps:
            self.velocity[1] = -5
            self.jumps -= 1
            self.air_time = 5
            return True



















class Object:
    def __init__(self, game, o_type, pos, size):
        self.game = game
        self.type = o_type
        self.pos = list(pos)
        self.size = size


    def rect(self):
        self.object_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.object_coliderect = pygame.rect.Rect((0, 0), (self.size[0], self.size[1]//2))
        self.object_coliderect.midbottom = self.object_rect.midbottom
        return self.object_coliderect
    

    def render(self, surf, offset=(0, 0), asset='ground'):
        surf.blit(self.game.assets[asset], (self.pos[0] - offset[0], self.pos[1] - offset[1]))

