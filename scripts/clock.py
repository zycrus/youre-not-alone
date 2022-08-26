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
        self.glow_alpha = 100

        self.fix_timer = 60
        
        self.is_lose = False
        self.is_win = False

        self.status = 'normal'
        self.frame = 0 
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
            self.is_win = True
        if self.status == 'corrupted':
            self.frame = int(self.corrupt_time)
            if self.corrupt_time < len(self.animations['corrupted']) - 1:
                self.corrupt_time += 0.00625
                # (len(self.animations['corrupted']) - 1) / (secs * 60)
            else:
                self.is_lose = True
                
        elif self.status == 'normal':
            self.frame = int(self.time_hour)
        self.image = self.animations[self.status][int(self.frame)]

    def draw_text(self, message):
        font = pygame.font.SysFont('arial', 16)
        timer_text = font.render(message, False, 'white', None)
        text_rect = timer_text.get_rect()
        text_rect.topleft = (20, 50)
        self.screen.blit(timer_text, text_rect)

    def fix_clock(self):
        keys = pygame.key.get_pressed()
        if keys[ord('e')]:
            if self.fix_timer > 0:
                self.fix_timer -= 1
                self.glow_alpha += 3
            else:
                self.status = 'normal'
                self.fix_timer = 60
                self.corrupt_time = 0
                self.corrupt_time = 0
                self.glow_alpha = 100
                
    def update(self, screen, player):
        self.animate()

        if self.rect.colliderect(player.sprite.collider.rect) and self.status == 'corrupted':
            glow = pygame.Surface((self.rect.width + 6, self.rect.height + 6))
            glow.set_alpha(self.glow_alpha)
            glow.fill('purple')
            #screen.blit(glow, (self.rect.x - 3, self.rect.y - 3))        
            self.fix_clock()
            
