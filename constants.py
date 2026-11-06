"""
Game constants and configuration settings.
All game-wide settings are defined here for easy modification.
"""

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (101, 67, 33)
PLAYER_COLOR = (255, 100, 100)
OBSTACLE_COLOR = (50, 50, 50)
COIN_COLOR = (255, 215, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)

# Player settings
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_X = 100  # Fixed X position for the player
GRAVITY = 0.8
JUMP_STRENGTH = -15

# Ground settings
GROUND_HEIGHT = 100
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT

# Obstacle settings
OBSTACLE_MIN_WIDTH = 30
OBSTACLE_MAX_WIDTH = 50
OBSTACLE_MIN_HEIGHT = 40
OBSTACLE_MAX_HEIGHT = 80
OBSTACLE_SPEED = 6
OBSTACLE_MIN_GAP = 300  # Minimum distance between obstacles
OBSTACLE_MAX_GAP = 500  # Maximum distance between obstacles

# Coin settings
COIN_RADIUS = 15
COIN_SPEED = OBSTACLE_SPEED  # Same speed as obstacles
COIN_HEIGHT_MIN = GROUND_Y - 150  # Minimum height above ground (high, requires jumping)
COIN_HEIGHT_MAX = GROUND_Y - 50   # Maximum height above ground
COIN_HEIGHT_LOW_MIN = GROUND_Y - 40  # Low coins reachable without jumping
COIN_HEIGHT_LOW_MAX = GROUND_Y - 10  # Low coins near ground level
COIN_SPAWN_MIN_X_OFFSET = 50  # Minimum distance from last obstacle
COIN_SPAWN_MAX_X_OFFSET = 300  # Maximum distance from last obstacle

# Game mechanics
INITIAL_OBSTACLE_COUNT = 3
COINS_TO_SPAWN_OBSTACLE = 1  # Spawn new obstacle every coin collected
DIFFICULTY_INCREASE_RATE = 0.1  # Speed increase per coin

# Font settings
FONT_SIZE_LARGE = 72
FONT_SIZE_MEDIUM = 48
FONT_SIZE_SMALL = 32
