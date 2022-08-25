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

event_states = ['menu', 'tutorial', 'main-game']
current_state = event_states[2]

# - - - - - - - - - - - - - - - - - - - - - - - - - -

#Player Initialization
player = pygame.sprite.GroupSingle()
player_sprite = Player(screen_width/2 - 16, screen_height/2 - 16)
player.add(player_sprite)

#Enemy
enemies = pygame.sprite.Group()

# Room objects
objects = pygame.sprite.Group()

room_layout = [
    Object((370, 100), 'bed'),
    Object((300, 150), 'carpet-side'),
    Object((30, 30), 'cabinet'),
    Object((100, 30), 'cabinet'),
    Object((50, 320), 'carpet'),
    Object((50, 400), 'table'),
    WallClock((200, 35), screen)
    ]

for o in room_layout:
    objects.add(o)
# - - - - - - - - - - - - - - - - - - - - - - - - - -

corrupt_timer = 300
def random_corrupt():
    sprite = random.choice(objects.sprites())

    if sprite.status == 'normal':
        sprite.status = 'corrupted'

#Spawn Enemy
spawn_timer = 120
death_timer = 0
death_timer_max = 300
def spawn_enemy():
    x = random.randrange(10, screen_width - 42)
    y = random.randrange(10, screen_height - 42)

    enemy = Enemy(x, y)
    enemies.add(enemy)


#Timer for spawning enemies
def draw_text():
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
        
    
    screen.blit(bg, (0, 0))

    # Objects
    objects.update(screen, player)
    objects.draw(screen)

    # Character
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

    draw_text() 

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)