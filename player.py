"""
Player class - Handles the player character's movement and rendering.
The player runs automatically and can jump to avoid obstacles.
"""

import pygame
from constants import *


class Player:
    """
    Represents the player character in the endless runner.

    Attributes:
        x: X-coordinate (fixed position)
        y: Y-coordinate (changes with jumping)
        width: Player width
        height: Player height
        velocity_y: Vertical velocity for jumping physics
        is_jumping: Whether player is currently in the air
    """

    def __init__(self):
        """Initialize the player at the starting position."""
        self.x = PLAYER_X
        self.y = GROUND_Y - PLAYER_HEIGHT
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False

    def jump(self):
        """
        Make the player jump if they're on the ground.
        Applies initial upward velocity.
        """
        if not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True

    def update(self):
        """
        Update player position based on physics.
        Applies gravity and handles ground collision.
        """
        # Apply gravity to vertical velocity
        self.velocity_y += GRAVITY

        # Update vertical position
        self.y += self.velocity_y

        # Ground collision detection
        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.velocity_y = 0
            self.is_jumping = False

    def draw(self, screen):
        """
        Draw the player on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, PLAYER_COLOR,
                        (self.x, self.y, self.width, self.height))

        # Draw eyes to make it look like a character
        eye_size = 5
        left_eye_x = self.x + self.width // 3
        right_eye_x = self.x + 2 * self.width // 3
        eye_y = self.y + self.height // 3

        pygame.draw.circle(screen, BLACK, (int(left_eye_x), int(eye_y)), eye_size)
        pygame.draw.circle(screen, BLACK, (int(right_eye_x), int(eye_y)), eye_size)

    def get_rect(self):
        """
        Get the player's collision rectangle.

        Returns:
            pygame.Rect: Rectangle for collision detection
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
