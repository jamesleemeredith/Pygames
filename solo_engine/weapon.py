import pygame
import math
import random
import constants as const

class Weapon:
    def __init__(self, image, arrow_image):
        self.original_image = image
        self.flipped_image = pygame.transform.flip(self.original_image, True, False)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.flipped_x = True
        self.angle = 0
        self.offset_x = 20
        self.arrow_image = arrow_image
        self.arrow_flipped_image = pygame.transform.flip(arrow_image, True, False)
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        shoot_cooldown = 500
        arrow = None
        self.flipped_x = player.flipped_x

        # Update the weapon's position based on the player's position
        if self.flipped_x:
            base_x, base_y = player.rect.midright
            self.rect.center = (base_x - self.offset_x, base_y)
        else:
            base_x, base_y = player.rect.midleft
            self.rect.center = (base_x + self.offset_x, base_y)

        # Calculate the angle between the weapon and the mouse position
        mouse_pos = pygame.mouse.get_pos()
        x_dist = mouse_pos[0] - self.rect.centerx
        y_dist = mouse_pos[1] - self.rect.centery

        # Clamp the angle to within 90 degrees up or down depending on the direction
        if self.flipped_x:
            angle = math.degrees(math.atan2(y_dist, x_dist))
            clamped_angle = max(-90, min(90, angle))
            self.image = pygame.transform.rotate(self.flipped_image, -clamped_angle)
        else:
            angle = math.degrees(math.atan2(-y_dist, -x_dist))
            clamped_angle = max(-90, min(90, angle))
            self.image = pygame.transform.rotate(self.original_image, -clamped_angle)

        # Update the rect to match the rotated image
        self.rect = self.image.get_rect(center=self.rect.center)

        # Check for mouse clicks
        if pygame.mouse.get_pressed()[0] and not self.fired and (pygame.time.get_ticks() - self.last_shot > shoot_cooldown):
            if self.flipped_x:
                arrow = Arrow(self.arrow_flipped_image,self.rect.centerx,self.rect.centery, -clamped_angle, True)
            else:
                arrow = Arrow(self.arrow_image,self.rect.centerx,self.rect.centery, clamped_angle, False)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()

        # Reset mouse click
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False
        return arrow
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle, flipped_x):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.damage = 10
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle) if flipped_x else pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.flipped_x = True
        # Calculate the speed based on the angle
        if flipped_x:
            self.speed = 10
            self.dx = math.cos(math.radians(self.angle)) * self.speed
            self.dy = -(math.sin(math.radians(self.angle)) * self.speed)
        else:            
            self.speed = 10
            self.dx = -(math.cos(math.radians(self.angle)) * self.speed)
            self.dy = -(math.sin(math.radians(self.angle)) * self.speed)


    def update(self, enemy_list):
        # Reposition the arrow based on speed
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Check if arrow has gone off screen
        if self.rect.right < 0 or self.rect.left > const.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > const.SCREEN_HEIGHT:
            self.kill()
        
        # Check collision between arrow and enemies
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect):
                enemy.health -= (self.damage + random.randint(-5,5)) 
                self.kill()
                if enemy.health <= 0:
                    enemy.health = 0
                    enemy_list.remove(enemy)
                break


    def draw(self, surface):
        surface.blit(self.image, self.rect)