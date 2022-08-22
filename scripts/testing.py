import pygame, sys
from support import import_folder

pygame.init()

# Setup pygame
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("You're not alone")
clock = pygame.time.Clock()

#Player Initialization
player = pygame.sprite.GroupSingle()
player_sprite = Player(screen_width/2 - 16, screen_height/2 - 16)
player.add(player_sprite)



class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init()
        self.import_character_assets()

    def import_character_assets(self):
        character_path = 'sprites/horror_player/'
        self.animations = {'up' : [],
                            'down' : [],
                            'side' : []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)