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

        self.action = 'idle'
        self.status = 'down'
        self.frame = 0
        self.anim_speed = 0.1
        self.image = self.animations[self.action][self.status][self.frame]
        self.rect = self.image.get_rect(topleft = (x, y))

        self.collider = PlayerCollider()
        self.collider_width = 15
        self.collider_height = 50
        self.collider_x = self.rect.x + self.rect.width/2 - self.collider_width/2
        self.collider_y = self.rect.y + self.rect.height/2 - self.collider_height

    def import_character_assets(self):
        character_path = 'sprites/ghost_player/'
        self.animations = {'idle': {'up' : [],
                                    'down' : [],
                                    'side' : []},
                            'moving': {'up' : [],
                                    'down' : [],
                                    'side' : []}}

        for action in self.animations.keys():
            for anim in self.animations[action].keys():
                full_path = character_path + action + '/' + anim
                self.animations[action][anim] = import_folder(full_path)
        
        # for animation in self.animations.keys():
        #     full_path = character_path + action + '/' + anim
        #     self.animations[animation] = import_folder(full_path)
            
    def move_frame(self):
        self.anim = self.animations[self.action][self.status]
        self.frame += self.anim_speed
        if self.frame >= len(self.anim):
            self.frame = 0

    def animate(self):
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
        keys = pygame.key.get_pressed()
        #Horizontal
        if self.left_pressed and not self.right_pressed:
            self.direction.x = -1
            
            self.action = 'moving'
            self.status = 'side'
        elif self.right_pressed and not self.left_pressed:
            self.direction.x = 1
            
            self.action = 'moving'
            self.status = 'side'
        else:
            self.action = 'idle'
            self.direction.x = 0

        #Vertical
        if self.up_pressed and not self.down_pressed:
            self.direction.y = -1
            self.status = 'up'
        elif self.down_pressed and not self.up_pressed:
            self.direction.y = 1
            
            self.action = 'moving'
            self.status = 'down'
        else:
            self.action = 'idle'
            self.direction.y = 0

        if keys[ord('e')]:
            self.is_busy = True
        else:
            self.is_busy = False
    
    def update(self, screen):
        self.get_input()

        #Move player
        self.velX = self.speed * self.direction.x
        self.velY = self.speed * self.direction.y
        
        #Animate frames
        # if self.direction != (0, 0):
        self.move_frame()

        self.animate()
        self.rect.x += self.velX
        self.rect.y += self.velY
        self.setup_collider(screen)

        
    def setup_collider(self, screen):
        if self.status == 'up':
            self.collider_width = 15
            self.collider_height = 55
            self.collider_x = self.rect.x + self.rect.width/2 - self.collider_width/2
            self.collider_y = self.rect.y + self.rect.height/2 - self.collider_height

            self.collider.pos = (self.rect.x, self.rect.y - self.rect.height/2)
            self.collider.image = self.collider.image_up
        elif self.status == 'down':
            self.collider_width = 15
            self.collider_height = 55
            self.collider_x = self.rect.x + self.rect.width/2 - self.collider_width/2
            self.collider_y = self.rect.y + self.rect.height/2

            self.collider.pos = (self.rect.x, self.rect.y)
            self.collider.image = self.collider.image_down
        elif self.status == 'side':
            self.collider_width = 55
            self.collider_height = 15
            if self.velX < 0:
                self.collider_x = self.rect.x + self.rect.width/2 - self.collider_width
                self.collider_y = self.rect.y + self.rect.height/2 - self.collider_height/2

                self.collider.pos = (self.rect.x - self.rect.width/2, self.rect.y)
                self.collider.image = self.collider.image_left
            elif self.velX > 0:
                self.collider_x = self.rect.x + self.rect.width/2
                self.collider_y = self.rect.y + self.rect.height/2 - self.collider_height/2

                self.collider.pos = (self.rect.x, self.rect.y)
                self.collider.image = self.collider.image_right
            
        self.collider.update(screen, self.collider_x, self.collider_y, self.collider_width, self.collider_height)
        if self.is_busy:
            screen.blit(self.collider.image, self.collider.pos)

class PlayerCollider(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.length = 40
        self.width = 15
        self.rect = (0, 0, 0, 0)
        self.pos = (0, 0)
        self.image_right = pygame.image.load('sprites/ghost_player/light/light-right.png')
        self.image_left = pygame.image.load('sprites/ghost_player/light/light-left.png')
        
        self.image_up = pygame.image.load('sprites/ghost_player/light/light-up.png')
        self.image_down = pygame.image.load('sprites/ghost_player/light/light-down.png')

    def update(self, screen, x, y, width, height):
        self.rect = (x, y, width, height)