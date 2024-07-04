import pygame
from math import degrees, atan2

class Weapon:
    def __init__(self, image):
        self.original_image = image
        self.flipped_image = pygame.transform.flip(self.original_image, True, False)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.flipped_x = True
        self.angle = 0

    def update(self, player):
        self.flipped_x = player.flipped_x

        # Update the weapon's position based on the player's position
        if self.flipped_x:
            self.rect.center = player.rect.midright
        else:
            self.rect.center = player.rect.midleft

        # Calculate the angle between the weapon and the mouse position
        mouse_pos = pygame.mouse.get_pos()
        x_dist = mouse_pos[0] - self.rect.centerx
        y_dist = mouse_pos[1] - self.rect.centery

        # Clamp the angle to within 90 degrees up or down depending on the direction
        if self.flipped_x:
            angle = degrees(atan2(y_dist, x_dist))
            clamped_angle = max(-90, min(90, angle))
            self.image = pygame.transform.rotate(self.flipped_image, -clamped_angle)
        else:
            angle = degrees(atan2(-y_dist, -x_dist))
            clamped_angle = max(-90, min(90, angle))
            self.image = pygame.transform.rotate(self.original_image, -clamped_angle)

        # Update the rect to match the rotated image
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)