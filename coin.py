"""
Coin class - Represents collectible coins that trigger dynamic path changes.
Coins float at various heights and move with the obstacles.
"""

import pygame
import random
from constants import *


class Coin:
    """
    Represents a collectible coin in the game.

    Attributes:
        x: X-coordinate
        y: Y-coordinate (random height above ground)
        radius: Coin radius
        speed: Movement speed
        collected: Whether the coin has been collected
    """

    def __init__(self, x, speed=COIN_SPEED):
        """
        Initialize a coin at a given x position.

        Args:
            x: Starting x-coordinate
            speed: Movement speed (matches obstacle speed)
        """
        self.x = x
        self.y = random.randint(COIN_HEIGHT_MAX, COIN_HEIGHT_MIN)
        self.radius = COIN_RADIUS
        self.speed = speed
        self.collected = False
        # Animation for visual effect
        self.angle = 0

    def update(self):
        """Move the coin to the left and update animation."""
        if not self.collected:
            self.x -= self.speed
            self.angle += 5  # Rotation effect

    def draw(self, screen):
        """
        Draw the coin on the screen with a glowing effect.

        Args:
            screen: Pygame surface to draw on
        """
        if not self.collected:
            # Draw outer glow
            pygame.draw.circle(screen, (255, 255, 150),
                             (int(self.x), int(self.y)), self.radius + 3)
            # Draw main coin
            pygame.draw.circle(screen, COIN_COLOR,
                             (int(self.x), int(self.y)), self.radius)
            # Draw inner highlight
            pygame.draw.circle(screen, (255, 255, 200),
                             (int(self.x - 3), int(self.y - 3)), self.radius // 3)

    def get_rect(self):
        """
        Get the coin's collision rectangle.

        Returns:
            pygame.Rect: Rectangle for collision detection
        """
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)

    def is_off_screen(self):
        """
        Check if the coin has moved completely off screen.

        Returns:
            bool: True if off screen, False otherwise
        """
        return self.x + self.radius < 0


class CoinManager:
    """
    Manages all coins in the game.
    Handles spawning, collecting, and triggering path changes.
    """

    def __init__(self, obstacle_manager):
        """
        Initialize the coin manager.

        Args:
            obstacle_manager: Reference to obstacle manager for triggering changes
        """
        self.coins = []
        self.obstacle_manager = obstacle_manager
        self.current_speed = COIN_SPEED
        self.coins_collected = 0
        self.spawn_timer = 0
        self.spawn_interval = 180  # Frames between coin spawns

    def spawn_coin(self):
        """
        Spawn a new coin at a random position between obstacles.
        Coins can be at high positions (require jumping) or low positions (reachable).
        """
        # Find the rightmost obstacle position
        if self.obstacle_manager.obstacles:
            last_obstacle = max(self.obstacle_manager.obstacles, 
                              key=lambda obs: obs.x + obs.width)
            coin_x = last_obstacle.x + last_obstacle.width + random.randint(
                COIN_SPAWN_MIN_X_OFFSET, COIN_SPAWN_MAX_X_OFFSET)
        else:
            # Fallback if no obstacles exist
            coin_x = SCREEN_WIDTH + random.randint(100, 300)
        
        # Randomly decide if this coin is high (requires jump) or low (reachable)
        if random.random() < 0.5:  # 50% chance of reachable coin
            # Low coin - reachable without jumping
            coin_y = random.randint(COIN_HEIGHT_LOW_MIN, COIN_HEIGHT_LOW_MAX)
        else:
            # High coin - requires jumping
            coin_y = random.randint(COIN_HEIGHT_MIN, COIN_HEIGHT_MAX)
        
        coin = Coin(coin_x, self.current_speed)
        coin.y = coin_y
        self.coins.append(coin)

    def update(self):
        """Update all coins and handle spawning."""
        # Update existing coins
        for coin in self.coins:
            coin.update()

        # Remove off-screen or collected coins
        self.coins = [coin for coin in self.coins
                     if not coin.is_off_screen() and not coin.collected]

        # Spawn new coins periodically
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_coin()
            self.spawn_timer = 0

    def draw(self, screen):
        """
        Draw all coins.

        Args:
            screen: Pygame surface to draw on
        """
        for coin in self.coins:
            coin.draw(screen)

    def check_collection(self, player_rect):
        """
        Check if player collected any coins and trigger path changes.

        Args:
            player_rect: Player's collision rectangle

        Returns:
            bool: True if a coin was collected, False otherwise
        """
        for coin in self.coins:
            if not coin.collected and coin.get_rect().colliderect(player_rect):
                coin.collected = True
                self.coins_collected += 1

                # DYNAMIC PATH CHANGE: Trigger when coin is collected
                self.trigger_path_change()
                return True
        return False

    def trigger_path_change(self):
        """
        Trigger dynamic path changes when a coin is collected.
        This makes the game unpredictable and exciting!
        """
        # Increase difficulty
        self.obstacle_manager.increase_difficulty()
        self.current_speed = self.obstacle_manager.current_speed

        # Update all existing coins to match new speed
        for coin in self.coins:
            coin.speed = self.current_speed

        # Spawn a new obstacle to increase challenge
        self.obstacle_manager.spawn_obstacle()

        # Occasionally spawn an extra coin for bonus opportunities
        if random.random() < 0.3:  # 30% chance
            self.spawn_coin()

    def increase_difficulty(self):
        """Increase coin speed to match obstacle speed."""
        self.current_speed = self.obstacle_manager.current_speed
        for coin in self.coins:
            coin.speed = self.current_speed

    def reset(self):
        """Reset coin manager to initial state."""
        self.coins = []
        self.current_speed = COIN_SPEED
        self.coins_collected = 0
        self.spawn_timer = 0
