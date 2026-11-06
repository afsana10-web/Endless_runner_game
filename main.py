"""
Main game file - Entry point for the Endless Runner game.
Contains the main game loop and coordinates all game components.

To run: python main.py (requires pygame to be installed)
"""

import pygame
import sys
from constants import *
from player import Player
from obstacle import ObstacleManager
from coin import CoinManager
from game_state import GameState, Menu, GameOverScreen


class Game:
    """
    Main game class that manages the game loop and all game components.

    This class coordinates between the player, obstacles, coins, and game states
    to create a complete endless runner experience.
    """

    def __init__(self):
        """Initialize pygame and create game components."""
        # Initialize pygame
        pygame.init()

        # Create screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Endless Runner")

        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()

        # Game state
        self.state = GameState.MENU

        # UI components
        self.menu = Menu(self.screen)
        self.game_over_screen = GameOverScreen(self.screen)

        # Game components (initialized when game starts)
        self.player = None
        self.obstacle_manager = None
        self.coin_manager = None

        # Game statistics
        self.score = 0
        self.distance = 0
        self.distance_counter = 0

        # Fonts for HUD
        self.hud_font = pygame.font.Font(None, FONT_SIZE_SMALL)

        # Running flag
        self.running = True

    def init_game_components(self):
        """Initialize/reset all game components for a new game."""
        self.player = Player()
        self.obstacle_manager = ObstacleManager()
        self.coin_manager = CoinManager(self.obstacle_manager)
        self.score = 0
        self.distance = 0
        self.distance_counter = 0

    def handle_events(self):
        """
        Handle all pygame events (keyboard, mouse, window close).
        Different events are handled based on current game state.
        """
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            # Window close event
            if event.type == pygame.QUIT:
                self.running = False

            # Handle events based on current state
            if self.state == GameState.MENU:
                new_state = self.menu.handle_events(events, mouse_pos)
                if new_state == GameState.PLAYING:
                    self.init_game_components()
                    self.state = new_state

            elif self.state == GameState.PLAYING:
                # Jump controls
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_UP]:
                        self.player.jump()
                    # Pause game
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.PAUSED

            elif self.state == GameState.PAUSED:
                # Unpause
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.PLAYING

            elif self.state == GameState.GAME_OVER:
                new_state = self.game_over_screen.handle_events(events, mouse_pos)
                if new_state == GameState.PLAYING:
                    self.init_game_components()
                    self.state = new_state
                elif new_state == GameState.MENU:
                    self.state = new_state

    def update(self):
        """
        Update all game components.
        Only updates when in PLAYING state.
        """
        if self.state != GameState.PLAYING:
            return

        # Update player
        self.player.update()

        # Update obstacles
        self.obstacle_manager.update()

        # Update coins
        self.coin_manager.update()

        # Check coin collection
        if self.coin_manager.check_collection(self.player.get_rect()):
            self.score += 1
            # Play a sound effect here if you add sound

        # Check collision with obstacles
        if self.obstacle_manager.check_collision(self.player.get_rect()):
            self.state = GameState.GAME_OVER

        # Update distance traveled
        self.distance_counter += 1
        if self.distance_counter >= FPS:  # Every second
            self.distance += 1
            self.distance_counter = 0

    def draw(self):
        """
        Draw all game components based on current state.
        """
        if self.state == GameState.MENU:
            self.menu.draw()

        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            # Draw sky background
            self.screen.fill(SKY_BLUE)

            # Draw ground
            pygame.draw.rect(self.screen, GROUND_COLOR,
                           (0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT))

            # Draw game objects
            self.obstacle_manager.draw(self.screen)
            self.coin_manager.draw(self.screen)
            self.player.draw(self.screen)

            # Draw HUD (score and distance)
            self.draw_hud()

            # Draw pause overlay if paused
            if self.state == GameState.PAUSED:
                self.draw_pause_overlay()

        elif self.state == GameState.GAME_OVER:
            self.game_over_screen.draw(self.score, self.distance)

        # Update display
        pygame.display.flip()

    def draw_hud(self):
        """Draw the heads-up display showing score and distance."""
        # Score
        score_text = self.hud_font.render(f"Coins: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        # Distance
        distance_text = self.hud_font.render(f"Distance: {self.distance}m",
                                            True, BLACK)
        self.screen.blit(distance_text, (10, 45))

        # Speed indicator
        current_speed = self.obstacle_manager.current_speed
        speed_text = self.hud_font.render(f"Speed: {current_speed:.1f}",
                                         True, BLACK)
        self.screen.blit(speed_text, (10, 80))

    def draw_pause_overlay(self):
        """Draw a semi-transparent overlay when game is paused."""
        # Create semi-transparent surface
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)  # 50% transparency
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Draw "PAUSED" text
        pause_font = pygame.font.Font(None, FONT_SIZE_LARGE)
        pause_text = pause_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2,
                                                 SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)

        # Draw instruction
        instruction_font = pygame.font.Font(None, FONT_SIZE_SMALL)
        instruction_text = instruction_font.render("Press ESC to resume",
                                                  True, WHITE)
        instruction_rect = instruction_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(instruction_text, instruction_rect)

    def run(self):
        """
        Main game loop.
        Handles events, updates game state, and renders everything.
        """
        while self.running:
            # Handle events
            self.handle_events()

            # Update game
            self.update()

            # Draw everything
            self.draw()

            # Control frame rate
            self.clock.tick(FPS)

        # Quit pygame
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
