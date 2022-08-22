import pygame, sys
from random import randrange
from settings import *
from key_handler import key_handle
from enemy import Enemy
from player import Player

pygame.init()

# Setup pygame
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("You're not alone")
clock = pygame.time.Clock()

#Player Initialization
player = pygame.sprite.GroupSingle()
player_sprite = Player(screen_width/2 - 16, screen_height/2 - 16)
player.add(player_sprite)

#Enemy
enemies = pygame.sprite.Group()

#Spawn Enemy
spawn_timer = 200
death_timer = 0
death_timer_max = 300
def SpawnEnemy():
    x = randrange(10, screen_width - 42)
    y = randrange(10, screen_height - 42)

    enemy = Enemy(x, y)
    enemies.add(enemy)
#Timer for spawning enemies
def DrawText():
    font = pygame.font.SysFont('arial', 16)
    timer_text = font.render(str(spawn_timer // 60), False, 'white', None)
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
    screen.fill(((0,0,0)))

    enemies.update(player, enemies, screen)
    enemies.draw(screen)
    player_sprite.update()
    player_sprite.draw(screen)

    if spawn_timer > 0:
        spawn_timer -= 1
    else:
        SpawnEnemy()
        spawn_timer = randrange(120, 600)

    DrawText() 

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)