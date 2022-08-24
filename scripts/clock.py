import pygame
from support import import_folder

class WallClock(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__()
        self.import_character_assets()
        self.origin_pos = pygame.math.Vector2(pos)
        self.screen = screen

        self.time_hour = 0
        self.time_speed = 0.001 

        self.corrupt_time = 0

        self.fix_timer = 60

        self.status = 'corrupted'
        self.frame = 0 
        print(self.animations)
        self.image = self.animations['normal'][self.frame]
        self.rect = self.image.get_rect(topleft = pos)

    def import_character_assets(self):
        character_path = 'sprites/objects/wallclock/'
        self.animations = {'normal' : [],
                            'corrupted' : []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        if self.time_hour < len(self.animations['normal']) - 1:
            self.time_hour += self.time_speed
        else:
            self.draw_text('you win')
        if self.status == 'corrupted':
            self.frame = int(self.corrupt_time)
            if self.corrupt_time < len(self.animations['corrupted']) - 1:
                self.corrupt_time += 0.00625
            else:
                self.draw_text('u ded')
                
        elif self.status == 'normal':
            self.frame = int(self.time_hour)
        self.image = self.animations[self.status][self.frame]

    def draw_text(self, message):
        font = pygame.font.SysFont('arial', 16)
        timer_text = font.render(message, False, 'white', None)
        text_rect = timer_text.get_rect()
        text_rect.topleft = (20, 50)
        self.screen.blit(timer_text, text_rect)

    def update(self, screen, player):
        self.animate()
        keys = pygame.key.get_pressed()

        if self.rect.colliderect(player.sprite.collider.rect) and self.status == 'corrupted':
            pygame.draw.rect(screen, 'purple', (self.rect.x - 3, self.rect.y - 3, self.rect.width + 6, self.rect.height + 6))

            if keys[ord('e')]:
                if self.fix_timer > 0:
                    self.fix_timer -= 1
                else:
                    self.status = 'normal'
                    self.fix_timer = 60
                    self.corrupt_time = 0