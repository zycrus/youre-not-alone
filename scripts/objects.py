import pygame
from support import import_folder

class Object(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.type = type
        self.import_character_assets()
        self.origin_pos = pygame.math.Vector2(pos)

        self.shake_speed = 10
        self.secs = 8
        self.timer_max = 60 * 8
        self.timer = 0
        self.fix_timer = 60
        self.glow_alpha = 100

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

    def draw_text(self, screen):
        font = pygame.font.SysFont('arial', 16)
        timer_text = font.render(str(self.timer / 60), False, 'white', None)
        text_rect = timer_text.get_rect()
        text_rect.topright = (480, 20)
        screen.blit(timer_text, text_rect)

    def animate(self):
        anim_speed = (len(self.animations[self.status]) - 1) / self.secs * 60
        if self.frame < len(self.animations[self.status]) - 1:
            self.frame += anim_speed
        if self.timer < self.timer_max and self.status == 'corrupted':
            self.timer += 1
            if self.timer > self.timer_max / 2:
                self.vibrate()
        self.image = self.animations[self.status][self.frame]

    def vibrate(self):
        if self.shake_speed <= 0:
            if self.rect.x == self.origin_pos.x + 5:
                self.rect.x = self.origin_pos.x - 5
            else:
                self.rect.x = self.origin_pos.x + 5
            self.shake_speed = 10
        else:
            self.shake_speed -= 1

    def update(self, screen, player):
        keys = pygame.key.get_pressed()

        if self.rect.colliderect(player.sprite.collider.rect) and self.status == 'corrupted':
            glow = pygame.Surface((self.rect.width + 6, self.rect.height + 6))
            glow.set_alpha(self.glow_alpha)
            glow.fill('purple')
            #screen.blit(glow, (self.rect.x - 3, self.rect.y - 3))            

            if keys[ord('e')]:
                if self.fix_timer > 0:
                    self.fix_timer -= 1
                    self.glow_alpha += 3
                else:
                    self.status = 'normal'
                    self.fix_timer = 60
                    self.glow_alpha = 100

        self.animate()
