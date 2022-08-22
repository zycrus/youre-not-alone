from distutils.spawn import spawn
import pygame, sys
from random import randrange

pygame.init()

# Setup pygame
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("You're not alone")
clock = pygame.time.Clock()


#Player and movement
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.color = (192,192,192)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
    
    def update(self):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed
        
        self.x += self.velX
        self.y += self.velY

        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)

#Player Initialization
player = Player(screen_width/2, screen_height/2)

#Enemy
enemies = pygame.sprite.Group()
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.image.fill('red')
        self.color = 'red'

    def update(self):
        if self.rect.colliderect(player.rect):
            enemies.remove(self)

#Spawn Enemy
spawn_timer = 200
def SpawnEnemy():
    x = randrange(10, screen_width - 42)
    y = randrange(10, screen_height - 42)

    enemy = Enemy(x, y)
    enemies.add(enemy)
#Timer for spawning enemies
def DrawTimer():
    font = pygame.font.SysFont('arial', 32)
    timer_text = font.render(str(spawn_timer // 60), False, 'white', None)
    text_rect = timer_text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2)
    screen.blit(timer_text, text_rect)

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.left_pressed = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.right_pressed = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.up_pressed = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.down_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.left_pressed = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.right_pressed = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.up_pressed = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.down_pressed = False
        
    #Character sample
    screen.fill(((0,0,0)))
    enemies.update()
    enemies.draw(screen)
    player.draw(screen)
    player.update()
    if spawn_timer > 0:
        spawn_timer -= 1
    else:
        SpawnEnemy()
        spawn_timer = randrange(120, 600)
    DrawTimer() 
    pygame.display.flip()

    pygame.display.update()
    clock.tick(60)