"""
Obstacle class - Represents obstacles that the player must avoid.
Obstacles move from right to left and have random sizes.
"""

import pygame
import random
from constants import *


class Obstacle:
    """
    Represents an obstacle in the game.

    Attributes:
        x: X-coordinate
        y: Y-coordinate (always on ground)
        width: Obstacle width
        height: Obstacle height
        speed: Movement speed
    """

    def __init__(self, x, speed=OBSTACLE_SPEED):
        """
        Initialize an obstacle at a given x position.

        Args:
            x: Starting x-coordinate
            speed: Movement speed (can increase over time)
        """
        self.width = random.randint(OBSTACLE_MIN_WIDTH, OBSTACLE_MAX_WIDTH)
        self.height = random.randint(OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT)
        self.x = x
        self.y = GROUND_Y - self.height
        self.speed = speed

    def update(self):
        """Move the obstacle to the left."""
        self.x -= self.speed

    def draw(self, screen):
        """
        Draw the obstacle on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, OBSTACLE_COLOR,
                        (self.x, self.y, self.width, self.height))

        # Add some detail to make it look more interesting
        highlight_width = 3
        pygame.draw.rect(screen, (80, 80, 80),
                        (self.x, self.y, highlight_width, self.height))

    def get_rect(self):
        """
        Get the obstacle's collision rectangle.

        Returns:
            pygame.Rect: Rectangle for collision detection
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_off_screen(self):
        """
        Check if the obstacle has moved completely off screen.

        Returns:
            bool: True if off screen, False otherwise
        """
        return self.x + self.width < 0


class ObstacleManager:
    """
    Manages all obstacles in the game.
    Handles spawning, updating, and removing obstacles.
    """

    def __init__(self):
        """Initialize the obstacle manager with starting obstacles."""
        self.obstacles = []
        self.current_speed = OBSTACLE_SPEED
        self.last_obstacle_x = SCREEN_WIDTH

        # Create initial obstacles
        for i in range(INITIAL_OBSTACLE_COUNT):
            x = SCREEN_WIDTH + i * 400
            self.obstacles.append(Obstacle(x, self.current_speed))
            self.last_obstacle_x = x

    def spawn_obstacle(self):
        """
        Spawn a new obstacle at a random distance from the last one.
        This creates dynamic, unpredictable gameplay.
        """
        gap = random.randint(OBSTACLE_MIN_GAP, OBSTACLE_MAX_GAP)
        new_x = self.last_obstacle_x + gap
        self.obstacles.append(Obstacle(new_x, self.current_speed))
        self.last_obstacle_x = new_x

    def increase_difficulty(self):
        """
        Increase game difficulty by increasing obstacle speed.
        Called when player collects coins.
        """
        self.current_speed += DIFFICULTY_INCREASE_RATE
        # Update speed for all existing obstacles
        for obstacle in self.obstacles:
            obstacle.speed = self.current_speed

    def update(self):
        """Update all obstacles and remove off-screen ones."""
        for obstacle in self.obstacles:
            obstacle.update()

        # Remove obstacles that are off screen
        self.obstacles = [obs for obs in self.obstacles if not obs.is_off_screen()]

        # Spawn new obstacle if needed
        if len(self.obstacles) < INITIAL_OBSTACLE_COUNT:
            self.spawn_obstacle()

    def draw(self, screen):
        """
        Draw all obstacles.

        Args:
            screen: Pygame surface to draw on
        """
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def check_collision(self, player_rect):
        """
        Check if any obstacle collides with the player.

        Args:
            player_rect: Player's collision rectangle

        Returns:
            bool: True if collision detected, False otherwise
        """
        for obstacle in self.obstacles:
            if obstacle.get_rect().colliderect(player_rect):
                return True
        return False

    def reset(self):
        """Reset obstacle manager to initial state."""
        self.__init__()
