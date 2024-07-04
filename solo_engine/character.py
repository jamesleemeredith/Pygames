import pygame
from math import sqrt

class Character():
    def __init__(self, x, y, character_type, character_animations):
        """
        Initializes the Character with a position, animations, and type.
        """
        self.character_type = character_type
        self.alive = True
        self.health = 100
        self.animations = character_animations[character_type]
        self.action = 'idle'
        self.frame_index = 0
        self.flipped_x = True
        self.flipped_y = False
        self.update_time = pygame.time.get_ticks()
        self.image = self.animations[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3.1

    def move(self, dx, dy):
        """
        Updates the character's position, which way the character faces, and the character's running state.
        """
        # Control diagonal speed
        if dx != 0 and dy != 0:
            dx *= (sqrt(2)/2)
            dy *= (sqrt(2)/2)
        self.rect.x += dx
        self.rect.y += dy

        # Flip the character based on the direction
        if dx > 0:
            self.flipped_x = True
        elif dx < 0:
            self.flipped_x = False
        
        # Update action based on movement
        if dx != 0 or dy != 0:
            if self.action != 'shoot':  # Only change to run if not shooting
                self.update_action('run')
        else:
            if self.action != 'shoot':  # Only change to idle if not shooting
                self.update_action('idle')

    def attack(self):
        """
        Changes the character's state to attack.
        """
        self.action = 'shoot'
        self.frame_index = 0  # Reset the frame index to start the attack animation from the beginning

    def update(self):
        # Check if character has died
        if self.health < 100:
            self.update_action('damaged')
        self.update_animation()

    def update_action(self, new_action):
        """
        Updates the character's action and resets the animation frame index.
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
        ANIMATION_COOLDOWN = 100  # Time in milliseconds between frames
        # Check if enough time has passed since the last frame update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            # Reset frame index if we've reached the end of the animation
            if self.frame_index >= len(self.animations[self.action]):
                self.frame_index = 0
                # If the current action is 'shoot', return to 'idle' after completing the animation
                if self.action == 'shoot':
                    self.action = 'idle'

        # Update the image to the current frame
        self.image = self.animations[self.action][self.frame_index]

    def draw(self, surface):
        """
        Draws the character on the screen.
        """
        if self.flipped_x:
            image = pygame.transform.flip(self.image, True, False)
        else:
            image = self.image
        surface.blit(image, self.rect)
        pygame.draw.rect(surface, 'red', self.rect.scale_by(.55,.98), 1)