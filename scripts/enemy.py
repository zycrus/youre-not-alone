import pygame
from settings import *
from support import import_folder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.import_assets()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.image.fill('red')
        self.color = 'red'
        self.timer = 90
        self.timer_max = 90

        self.frame = 0
        self.popup_anim_speed = 60

    def import_assets(self):
        sprite_path = 'sprites/popup_anim'
        self.popup_anim = import_folder(sprite_path)

    def draw_popup(self, screen):
        self.ui_press_e = self.popup_anim[self.frame]
        self.ui_press_e.get_rect(midbottom = self.rect.midbottom)
        screen.blit(self.ui_press_e, (self.rect.centerx - self.ui_press_e.get_width()/2, self.rect.top - self.ui_press_e.get_height() - 3))

    def clean(self, screen):
        hud_width = 250
        hud_height = 15
        hud_progress = hud_width * (1 - (self.timer/self.timer_max))
        hud_color = 'cyan'
        pygame.draw.rect(screen, 'gray', ((screen_width - hud_width)/2, screen_height - hud_height - 20, hud_width , hud_height))
        pygame.draw.rect(screen, hud_color, ((screen_width - hud_width)/2, screen_height - hud_height - 20, hud_progress , hud_height))

    def update(self, player, enemies, screen):
        keys = pygame.key.get_pressed()
        if self.rect.colliderect(player.sprite.rect):
            self.draw_popup(screen)
            
            self.clean(screen)
            if keys[ord('e')]:
                self.frame = 1
                if self.timer > 0:
                    self.timer -= 1
                else:
                    enemies.remove(self)
            else:
                if self.popup_anim_speed > 0:
                    self.popup_anim_speed -= 10
                else:
                    if self.frame == 0:
                        self.frame = 1
                    elif self.frame == 1:
                        self.frame = 0
                    self.popup_anim_speed = 60