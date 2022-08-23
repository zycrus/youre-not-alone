import pygame
from support import import_folder

#Player and movement
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.import_character_assets()
        self.x = x
        self.y = y
        self.color = (192,192,192)
        self.velX = 0
        self.velY = 0
        self.speed = 4
        self.direction = pygame.math.Vector2(0, 0)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.is_busy = False

        self.status = 'down'
        self.frame = 0
        self.anim_speed = 0.15
        self.image = self.animations[self.status][self.frame]
        self.rect = self.image.get_rect(topleft = (x, y))

    def import_character_assets(self):
        character_path = 'sprites/horror_player/'
        self.animations = {'up' : [],
                            'down' : [],
                            'side' : []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            
    def move_frame(self):
        self.frame += self.anim_speed
        if self.frame >= len(self.anim):
            self.frame = 0

    def animate(self):
        self.anim = self.animations[self.status]

        image = self.anim[int(self.frame)]
        if self.status == 'side':
            if self.direction.x > 0:
                self.image = image
            elif self.direction.x < 0:
                flipped_image = pygame.transform.flip(image, True, False)
                self.image = flipped_image
        if self.status == 'up' or self.status == 'down':
            self.image = image

        self.rect = self.image.get_rect(center = self.rect.center)

    def get_input(self):
        #Horizontal
        if self.left_pressed and not self.right_pressed:
            self.direction.x = -1
            self.status = 'side'
        elif self.right_pressed and not self.left_pressed:
            self.direction.x = 1
            self.status = 'side'
        else:
            self.direction.x = 0

        #Vertical
        if self.up_pressed and not self.down_pressed:
            self.direction.y = -1
            self.status = 'up'
        elif self.down_pressed and not self.up_pressed:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
    
    def update(self):
        self.get_input()

        #Move player
        self.velX = self.speed * self.direction.x
        self.velY = self.speed * self.direction.y
        
        #Animate frames
        if self.direction != (0, 0):
            self.move_frame()

        self.animate()
        self.rect.x += self.velX
        self.rect.y += self.velY