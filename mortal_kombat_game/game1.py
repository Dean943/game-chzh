import os
import sys
import math
import random

import pygame

from entities1 import *
from scripts.utils import *




class Game:
    def __init__(self):
        pygame.init()
        self.FPS = 60
        pygame.display.set_caption('MORTAL KOMBAT')
        self.screen = pygame.display.set_mode((1280, 720))
        #self.display = pygame.Surface((960, 540))
        self.display = pygame.Surface((640, 360))
        icon = pygame.image.load(BASE_IMG_PATH + 'Mortal-Kombat-Logo.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        self.assets = {
            'player': load_image_transparent('entities/player.png'),
            'icon': load_image('Mortal-Kombat-Logo.png'),
            'backgrounds': load_images_transparent('backgrounds'),
            'ground': load_image_transparent('tiles/parallax.png'),
            'bg': load_image_transparent('tiles/bg.png'),
            'p_2': load_image_transparent('tiles/p_2.gif'),
            'player/idle': Animation(load_images_transparent('entities/player/idle'), img_dur=10),
            'player/walk': Animation(load_images_transparent('entities/player/walk'), img_dur=4),
            'player/run': Animation(load_images_transparent('entities/player/run'), img_dur=3),
            'player/jump': Animation(load_images_transparent('entities/player/jump')),
            'player/duck': Animation(load_images_transparent('entities/player/duck'), img_dur=4, loop=False),
            'player/duck_rev': Animation(load_images_transparent('entities/player/duck_rev'), img_dur=4, loop=False)
        }
        
        #self.ground = load_image_transparent('tiles/parallax.png')
        #self.ground_rect = self.ground.get_rect(bottomleft = (0, 540))
        #self.ground_coliderect = pygame.rect.Rect((0, 0), (self.ground.get_width(), self.ground.get_height()//2))
        #self.ground_coliderect.midbottom = self.ground_rect.midbottom

        self.player = Player(self, (300, 390), (63, 129))
        self.object = Object(self,'ground', (0, 498), (1200, 42))
        self.prop = Object(self,'prop', (0, 422), (1003, 76))


        self.scroll = [0, 0]


        self.bird_eye_view = False

        self.font = pygame.font.Font('mortal_kombat_game\data\CloisterBlack.ttf', 100)
        self.play = self.font.render('play', True, (0, 0, 0))
        self.customization = self.font.render('customization', True, (0, 0, 0))
        self.settings = self.font.render('settings', True, (0, 0, 0))
        self.exit_game = self.font.render('exit game', True, (0, 0, 0))
        self.play_rect = self.play.get_rect(midleft = (50, 144))
        self.customization_rect = self.customization.get_rect(midleft = (50, 288))
        self.settings_rect = self.settings.get_rect(midleft = (50, 432))
        self.exit_game_rect = self.exit_game.get_rect(midleft = (50, 576))



    def main(self):
        background_img = random.choice(self.assets['backgrounds'])
        while True:


            self.screen.fill((0, 0, 0))
            self.screen.blit(background_img, (0, 0))
            self.screen.blit(self.play, self.play_rect)
            self.screen.blit(self.customization, self.customization_rect)
            self.screen.blit(self.settings, self.settings_rect)
            self.screen.blit(self.exit_game, self.exit_game_rect)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    x, y = pygame.mouse.get_pos()

                    if pygame.Rect.collidepoint(self.play_rect, x, y):
                        self.play = self.font.render('play', True, (255, 255, 255))
                    else:
                        self.play = self.font.render('play', True, (0, 0, 0))

                    if pygame.Rect.collidepoint(self.customization_rect, x, y):
                        self.customization = self.font.render('customization', True, (255, 255, 255))
                    else:
                        self.customization = self.font.render('customization', True, (0, 0, 0))

                    if pygame.Rect.collidepoint(self.settings_rect, x, y):
                        self.settings = self.font.render('settings', True, (255, 255, 255))
                    else:
                        self.settings = self.font.render('settings', True, (0, 0, 0))

                    if pygame.Rect.collidepoint(self.exit_game_rect, x, y):
                        self.exit_game = self.font.render('exit game', True, (255, 255, 255))
                    else:
                        self.exit_game = self.font.render('exit game', True, (0, 0, 0))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    if pygame.Rect.collidepoint(self.play_rect, x, y):
                        Game().run()
                    if pygame.Rect.collidepoint(self.customization_rect, x, y):
                        self.customization = self.font.render('customization', True, (255, 255, 255))
                    else:
                        self.customization = self.font.render('customization', True, (0, 0, 0))

                    if pygame.Rect.collidepoint(self.settings_rect, x, y):
                        self.settings = self.font.render('settings', True, (255, 255, 255))
                    else:
                        self.settings = self.font.render('settings', True, (0, 0, 0))

                    if pygame.Rect.collidepoint(self.exit_game_rect, x, y):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()
            self.clock.tick(self.FPS)


    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            self.display.blit(pygame.transform.rotozoom(self.assets['bg'], 0, 1.7), (0, 0))
            self.display.blit(pygame.transform.rotozoom(self.assets['bg'], 0, 1.7), (0, 100))
            self.display.blit(pygame.transform.flip(pygame.transform.rotozoom(self.assets['bg'], 0, 1.7), False, True), (0, 314))
            if self.bird_eye_view:
                self.display.blit(pygame.transform.rotozoom(self.assets['bg'], 0, 2.55), (0, 0))
                self.display.blit(pygame.transform.rotozoom(self.assets['bg'], 0, 2.55), (0, 100))
                self.display.blit(pygame.transform.rotozoom(self.assets['bg'], 0, 2.55), (0, 175))
                self.display.blit(pygame.transform.flip(pygame.transform.rotozoom(self.assets['bg'], 0, 2.55), False, True), (0, 495))
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 10
            self.scroll[1] += (self.player.rect().y + 150 - self.display.get_height() - self.scroll[1]) / 25
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # self.display.blit(self.ground, self.ground_rect)
            self.object.render(self.display, offset = render_scroll)
            self.prop.render(self.display, offset = render_scroll, asset='p_2')
            self.player.update((self.player.speed*(self.movement[1] - self.movement[0]), 0))
            self.player.render(self.display, offset = render_scroll)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        self.player.speed = 7
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if not self.player.duck or self.player.duck_rev:
                            self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if not self.player.duck or self.player.duck_rev:
                            self.movement[1] = True
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.jump()
                        self.player.speed = 2
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.duck = True
                        self.movement[0] = False
                        self.movement[1] = False
                    
                    
                    if event.key == pygame.K_o:
                        self.main()
                    if event.key == pygame.K_v:
                        self.display = pygame.Surface((960, 540))
                        self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0])
                        self.scroll[1] += (self.player.rect().y + 150 - self.display.get_height() - self.scroll[1])
                        self.bird_eye_view = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT:
                        self.player.speed = 3
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.speed = 3
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.duck = False
                    if event.key == pygame.K_v:
                        self.display = pygame.Surface((640, 360))
                        self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0])
                        self.scroll[1] += (self.player.rect().y + 150 - self.display.get_height() - self.scroll[1])
                        self.bird_eye_view = False
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(self.FPS)


#Game().main()
Game().run()





