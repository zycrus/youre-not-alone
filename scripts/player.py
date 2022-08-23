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

        self.collider = PlayerCollider()
        self.collider_width = 15
        self.collider_height = 50
        self.collider_x = self.rect.x + self.rect.width/2 - self.collider_width/2
        self.collider_y = self.rect.y + self.rect.height/2 - self.collider_height

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
    
    def update(self, screen):
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
        self.setup_collider(screen)

        
    def setup_collider(self, screen):
        if self.status == 'up':
            self.collider_width = 15
            self.collider_height = 50
            self.collider_x = self.rect.x + self.rect.width/2 - self.collider_width/2
            self.collider_y = self.rect.y + self.rect.height/2 - self.collider_height
        elif self.status == 'down':
            self.collider_width = 15
            self.collider_height = 50
            self.collider_x = self.rect.x + self.rect.width/2 - self.collider_width/2
            self.collider_y = self.rect.y + self.rect.height/2
        elif self.status == 'side':
            self.collider_width = 50
            self.collider_height = 15
            if self.velX < 0:
                self.collider_x = self.rect.x + self.rect.width/2 - self.collider_width
                self.collider_y = self.rect.y + self.rect.height/2 - self.collider_height/2
            elif self.velX > 0:
                self.collider_x = self.rect.x + self.rect.width/2
                self.collider_y = self.rect.y + self.rect.height/2 - self.collider_height/2
            
        self.collider.update(screen, self.collider_x, self.collider_y, self.collider_width, self.collider_height)

class PlayerCollider(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.length = 40
        self.width = 15
        self.rect = (0, 0, 0, 0)

    def update(self, screen, x, y, width, height):
        self.rect = (x, y, width, height)