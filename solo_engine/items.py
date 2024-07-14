import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.animations = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        