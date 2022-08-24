import pygame, sys
import random
from settings import *
from key_handler import key_handle
from enemy import Enemy
from player import Player
from objects import Object
from clock import WallClock

pygame.init()

# Setup pygame
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("You're not alone")
icon = pygame.image.load('sprites/ghost_player/idle/down/sprite_0.png')
pygame.display.set_icon(icon) 
bg = pygame.image.load('sprites/floor.png')

clock = pygame.time.Clock()

#Player Initialization
player = pygame.sprite.GroupSingle()
player_sprite = Player(screen_width/2 - 16, screen_height/2 - 16)
player.add(player_sprite)

#Enemy
enemies = pygame.sprite.Group()

#Objects
objects = pygame.sprite.Group()
bed = Object((350, 200), 'bed')
cabinet = Object((350, 30), 'cabinet')
cabinet2 = Object((285, 30), 'cabinet')
wallclock = WallClock((100, 100), screen)
objects.add(bed)
objects.add(cabinet)
objects.add(cabinet2)
objects.add(wallclock)

corrupt_timer = 60
def random_corrupt():
    sprite = random.choice(objects.sprites())

    if sprite.status == 'normal':
        sprite.status = 'corrupted'


#Spawn Enemy
spawn_timer = 120
death_timer = 0
death_timer_max = 300
def SpawnEnemy():
    x = random.randrange(10, screen_width - 42)
    y = random.randrange(10, screen_height - 42)

    enemy = Enemy(x, y)
    enemies.add(enemy)
#Timer for spawning enemies
def DrawText():
    font = pygame.font.SysFont('arial', 16)
    timer_text = font.render('Press E to Light up', False, 'white', None)
    text_rect = timer_text.get_rect()
    text_rect.topleft = (20, 20)
    screen.blit(timer_text, text_rect)

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        key_handle(event, player_sprite)
        
    #Character sample
    screen.blit(bg, (0, 0))

    objects.update(screen, player)
    objects.draw(screen)

    enemies.update(player, enemies, screen)
    enemies.draw(screen)

    player.update(screen)
    player.draw(screen)

    if spawn_timer > 0:
        spawn_timer -= 1
    else:
        #SpawnEnemy()
        spawn_timer = random.randrange(120, 600)

    if corrupt_timer > 0:
        corrupt_timer -= 1
    else:
        random_corrupt()
        corrupt_timer = random.randrange(120, 600)

    DrawText() 

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)