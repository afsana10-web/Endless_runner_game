"""
Game state management - Handles different game states (menu, playing, game over).
Provides a clean way to switch between different screens and modes.
"""

import pygame
from constants import *


class GameState:
    """
    Enum-like class for game states.
    """
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    PAUSED = "paused"


class Button:
    """
    Simple button class for menu interactions.

    Attributes:
        rect: Button rectangle
        text: Button text
        color: Button color
        hover_color: Color when mouse hovers over
        text_color: Text color
    """

    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR):
        """
        Initialize a button.

        Args:
            x, y: Button position
            width, height: Button dimensions
            text: Button text
            color: Button background color
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = BUTTON_HOVER
        self.text_color = WHITE
        self.is_hovered = False

    def draw(self, screen, font):
        """
        Draw the button on the screen.

        Args:
            screen: Pygame surface to draw on
            font: Pygame font for text
        """
        # Choose color based on hover state
        current_color = self.hover_color if self.is_hovered else self.color

        # Draw button background
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=10)

        # Draw text centered on button
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        """
        Check if mouse is hovering over the button.

        Args:
            mouse_pos: Current mouse position (x, y)
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_clicked):
        """
        Check if button was clicked.

        Args:
            mouse_pos: Current mouse position
            mouse_clicked: Whether mouse was clicked

        Returns:
            bool: True if button was clicked
        """
        return self.is_hovered and mouse_clicked


class Menu:
    """
    Main menu screen with title and start button.
    """

    def __init__(self, screen):
        """
        Initialize the menu.

        Args:
            screen: Pygame screen surface
        """
        self.screen = screen
        self.title_font = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.button_font = pygame.font.Font(None, FONT_SIZE_SMALL)

        # Create start button centered on screen
        button_width = 200
        button_height = 60
        button_x = (SCREEN_WIDTH - button_width) // 2
        button_y = 420

        self.start_button = Button(button_x, button_y, button_width,
                                   button_height, "START")

    def handle_events(self, events, mouse_pos):
        """
        Handle menu events.

        Args:
            events: List of pygame events
            mouse_pos: Current mouse position

        Returns:
            str: New game state if button clicked, None otherwise
        """
        self.start_button.check_hover(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_clicked(mouse_pos, True):
                    return GameState.PLAYING
        return None

    def draw(self):
        """Draw the menu screen."""
        self.screen.fill(SKY_BLUE)

        # Draw title
        title_text = self.title_font.render("ENDLESS RUNNER", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Draw instructions
        instructions = [
            "Press SPACE or UP ARROW to jump",
            "Collect coins to change the path!",
            "Avoid obstacles and survive as long as you can"
        ]

        instruction_font = pygame.font.Font(None, 24)
        y_offset = 250
        for instruction in instructions:
            text = instruction_font.render(instruction, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30

        # Draw start button
        self.start_button.draw(self.screen, self.button_font)


class GameOverScreen:
    """
    Game over screen showing final score and restart option.
    """

    def __init__(self, screen):
        """
        Initialize the game over screen.

        Args:
            screen: Pygame screen surface
        """
        self.screen = screen
        self.title_font = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.score_font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.button_font = pygame.font.Font(None, FONT_SIZE_SMALL)

        # Create restart button
        button_width = 200
        button_height = 60
        button_x = (SCREEN_WIDTH - button_width) // 2
        button_y = SCREEN_HEIGHT // 2 + 50

        self.restart_button = Button(button_x, button_y, button_width,
                                     button_height, "RESTART")

        # Create menu button
        menu_button_y = button_y + 80
        self.menu_button = Button(button_x, menu_button_y, button_width,
                                  button_height, "MENU")

    def handle_events(self, events, mouse_pos):
        """
        Handle game over screen events.

        Args:
            events: List of pygame events
            mouse_pos: Current mouse position

        Returns:
            str: New game state if button clicked, None otherwise
        """
        self.restart_button.check_hover(mouse_pos)
        self.menu_button.check_hover(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button.is_clicked(mouse_pos, True):
                    return GameState.PLAYING
                if self.menu_button.is_clicked(mouse_pos, True):
                    return GameState.MENU
        return None

    def draw(self, score, distance):
        """
        Draw the game over screen.

        Args:
            score: Final score (coins collected)
            distance: Distance traveled
        """
        self.screen.fill(SKY_BLUE)

        # Draw "Game Over" title
        title_text = self.title_font.render("GAME OVER", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(title_text, title_rect)

        # Draw score
        score_text = self.score_font.render(f"Coins Collected: {score}", True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(score_text, score_rect)

        # Draw distance
        distance_text = self.score_font.render(f"Distance: {distance}m", True, BLACK)
        distance_rect = distance_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(distance_text, distance_rect)

        # Draw buttons
        self.restart_button.draw(self.screen, self.button_font)
        self.menu_button.draw(self.screen, self.button_font)
