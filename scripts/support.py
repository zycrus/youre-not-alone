from os import walk
import pygame

def import_folder(path):
    surface_list = []

    for dir, idk, img_files in walk(path):
        print(img_files)
        for img in img_files:
            full_path = path + "/" + img
            image_surface = pygame.image.load(full_path)
            surface_list.append(image_surface)

    return surface_list