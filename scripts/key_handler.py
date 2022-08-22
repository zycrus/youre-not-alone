import pygame

def key_handle(event, player):
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