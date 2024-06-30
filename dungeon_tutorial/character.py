import pygame
from math import sqrt
import constants as const
from utilities import scale_img

class Character():
    def __init__(self, x, y, character_type, character_animations):
        """
        Initializes the Character with a position, animations, and type.
        """
        self.character_type = character_type
        self.flipped_x = True
        self.flipped_y = False
        self.animation_list = character_animations[character_type]
        self.action = const.IDLE_ACTION
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.running = False # Do we need this?
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(x,y))

    def move(self, dx, dy):
        """
        Updates the character's position and running state.
        """
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
        if dx > 0:
            self.flipped_x = True
        elif dx < 0:
            self.flipped_x = False
        # Control diagonal speed
        if dx != 0 and dy != 0:
            dx *= (sqrt(2)/2)
            dy *= (sqrt(2)/2)
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        """
        Updates the character's animation based on its state.
        """
        # Check what action the player is performing
        self.update_action(const.RUN_ACTION if self.running else const.IDLE_ACTION)
        self.update_animation()

    def update_action(self, new_action):
        """
        Changes the character's action and resets the animation frame index.
        """
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_animation(self):
        """
        Updates the character's animation frame.
        """
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > const.ANIMATION_COOLDOWN:
            self.frame_index = (self.frame_index + 1) % len(self.animation_list[self.action])
            self.update_time = pygame.time.get_ticks()
        # Check if the animation has finished
        # if self.frame_index >= len(self.animation_list[self.action]):
        #     self.frame_index = 0

    def draw(self, surface):
        """
        Draws the character on the screen.
        """
        flipped_image = pygame.transform.flip(self.image,self.flipped_x,self.flipped_y)
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, const.RED, self.rect.scale_by(.55,.98), 1)