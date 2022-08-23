import pygame
from support import import_folder

class Object(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.type = type
        self.import_character_assets()
        self.origin_pos = pygame.math.Vector2(pos)

        self.shake_speed = 0
        self.timer = 60

        self.status = 'normal'
        self.frame = 0
        self.image = self.animations['normal'][self.frame]
        self.rect = self.image.get_rect(topleft = pos)

    def import_character_assets(self):
        character_path = 'sprites/objects/' + self.type + '/'
        self.animations = {'normal' : [],
                            'corrupted' : []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def vibrate(self):
        if self.status == 'corrupted':
            shake_amount = 1
            shake = shake_amount
            if self.shake_speed < 2:
                shake = shake_amount
                self.shake_speed += 1
            elif self.shake_speed < 4:
                shake = -shake_amount
                self.shake_speed += 1
            else:
                self.shake_speed = 0
            self.rect.x = self.origin_pos.x + shake

    def DrawText(self, screen):
        font = pygame.font.SysFont('arial', 16)
        timer_text = font.render(str(self.timer / 60), False, 'white', None)
        text_rect = timer_text.get_rect()
        text_rect.topright = (480, 20)
        screen.blit(timer_text, text_rect)

    def update(self, screen):
        self.vibrate()
        self.DrawText(screen)

        if self.timer > 0:
            self.timer -= 1
        else:
            self.status = 'corrupted'
