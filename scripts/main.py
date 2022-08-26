import pygame, sys
import random
from pygame import mixer
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
bg = pygame.image.load('sprites/floor2.png')
border = pygame.image.load('sprites/border.png')
title_screen = pygame.image.load('sprites/title_screen.png')
tutorial_screen = pygame.image.load('sprites/tutorial_screen.png')
lose_screen = pygame.image.load('sprites/lose_screen.png')
win_screen = pygame.image.load('sprites/win_screen.png')

clock = pygame.time.Clock()

event_states = ['menu', 'tutorial', 'main-game', 'lose', 'win']
current_state = event_states[0]

# - - - - - - - - - - - - - - - - - - - - - - - - - -
#Background Music
mixer.music.load('BGM and Sound Effects/bgm.wav')
mixer.music.play(-1)


#Player Initialization
player = pygame.sprite.GroupSingle()
player_sprite = Player(screen_width/2 - 16, screen_height/2 - 16)
player.add(player_sprite)

#Enemy
enemies = pygame.sprite.Group()

# Room objects
objects = pygame.sprite.Group()

wall_clock = WallClock((200, 15), screen)
def setup_room(wall_clock):
    wall_clock = WallClock((200, 15), screen)
    room_layout = [
        Object((370, 100), 'bed'),
        Object((300, 150), 'carpet-side'),
        Object((30, 30), 'cabinet'),
        Object((100, 30), 'cabinet'),
        Object((50, 320), 'carpet'),
        Object((50, 400), 'table'),
        wall_clock
        ]

    for o in room_layout:
        objects.add(o)
# - - - - - - - - - - - - - - - - - - - - - - - - - -

corrupt_timer_max = 600
corrupt_timer = 300
def random_corrupt(timer):
    sprite = random.choice(objects.sprites())
    if sprite.status == 'normal':
        sprite.status = 'corrupted'
    timer -= 10

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
def draw_text(text, size, pos):
    font = pygame.font.SysFont('arial', size)
    timer_text = font.render(text, False, 'white', None)
    text_rect = timer_text.get_rect()
    text_rect.center = pos
    screen.blit(timer_text, text_rect)

paused = False
#Game Loop
while True:
    for event in pygame.event.get():
        key_handle(event, player_sprite)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE and current_state == event_states[2]:
                mixer.music.unpause() 
                draw_text("PAUSED", 50, (250, 250))
                pygame.display.update()
                paused = not paused
            if event.key == pygame.K_SPACE:
                if current_state == event_states[0]:
                    current_state = event_states[1]
                elif current_state == event_states[1]:
                    current_state = event_states[2]
                    setup_room(wall_clock)
                elif current_state == event_states[3]:
                    current_state = event_states[0]
                    objects.empty()
                    print(objects.sprites())
                elif current_state == event_states[4]:
                    current_state = event_states[0]
                    objects.empty()
                
        
    if paused:
        mixer.music.pause() 
        continue

    if current_state == event_states[0]:
        screen.blit(title_screen, (0, 0))
    elif current_state == event_states[1]:
        screen.blit(tutorial_screen, (0, 0))
    elif current_state == event_states[2]:
        screen.blit(bg, (0, 0))

        # Objects
        objects.update(screen, player)
        objects.draw(screen)

        # Character
        player.update(screen)
        player.draw(screen)

        screen.blit(border, (0, 0))

        if spawn_timer > 0:
            spawn_timer -= 1
        else:
            #SpawnEnemy()
            spawn_timer = random.randrange(120, corrupt_timer_max)

        if corrupt_timer > 0:
            corrupt_timer -= 1
        else:
            random_corrupt(corrupt_timer_max)
            corrupt_timer = random.randrange(120, corrupt_timer_max)

        for sprite in objects.sprites():
            if sprite.is_lose == True:
                lost_sound = mixer.Sound('BGM and Sound Effects/lost.wav')
                lost_sound.play()            
                current_state = event_states[3]
        if wall_clock.is_win == True:
            win_sound = mixer.Sound('BGM and Sound Effects/win.mp3')
            win_sound.play()
            current_state = event_states[4]
            

        draw_text("Press E to Light Up", 16, (90, 15)) 
    elif current_state == event_states[3]:
        screen.blit(lose_screen, (0, 0))
    elif current_state == event_states[4]:
        screen.blit(win_screen, (0, 0))

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)