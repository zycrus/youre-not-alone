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
        self.fix_timer = 60

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

    def draw_text(self, screen):
        font = pygame.font.SysFont('arial', 16)
        timer_text = font.render(str(self.timer / 60), False, 'white', None)
        text_rect = timer_text.get_rect()
        text_rect.topright = (480, 20)
        screen.blit(timer_text, text_rect)

    def update(self, screen, player):
        self.vibrate()
        self.draw_text(screen)
        keys = pygame.key.get_pressed()

        if self.rect.colliderect(player.sprite.collider.rect) and self.status == 'corrupted':
            pygame.draw.rect(screen, 'purple', (self.rect.x - 3, self.rect.y - 3, self.rect.width + 6, self.rect.height + 6))

            if keys[ord('e')]:
                if self.fix_timer > 0:
                    self.fix_timer -= 1
                else:
                    self.status = 'normal'
                    self.fix_timer = 60
