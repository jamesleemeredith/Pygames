import pygame

class Weapon():
    def __init__(self, image):
        self.image = image
        self.flipped_image = pygame.transform.flip(self.image, True, False)
        self.flipped_x = True
        self.rect = self.image.get_rect()
        # self.angle = 0
        # self.image = pygame.transform.rotate(self.original_image, self.angle)

    def update(self, player):
        self.flipped_x = player.flipped_x
        if self.flipped_x:
            self.rect.center = player.rect.midright
        else:
            self.rect.center = player.rect.midleft

    def draw(self, surface):
        if self.flipped_x:
            surface.blit(self.flipped_image, self.rect)
        else:
            surface.blit(self.image, self.rect)