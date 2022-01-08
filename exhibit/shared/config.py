
class Config:
    """
    Holds general configuration settings in a centralized place.

    This class should generally be used as a singleton.
    Individual instances can be created for test setups.
    """
    sharedInstance = None

    @staticmethod
    def instance():
        if Config.sharedInstance is None:
            Config.sharedInstance = Config()
        return Config.sharedInstance

    def __init__(self):
        self.USE_DEPTH_CAMERA = False

        self.PADDING = 10  # Distance between screen edge and player paddles (px)
        self.MAX_SCORE = 21  # Points one side must win to finish game
        self.WIDTH = 192  # Game window width (px)
        self.HEIGHT = 160  # Game window height (px)
        self.SPEEDUP = 1  # Flat multiplier to game movement speeds
        self.ACTIONS = ["LEFT", "RIGHT", "NONE", "DEPTH"]
        self.GAME_FPS = 60
        self.AI_FRAME_INTERVAL = 3  # AI will publish inference every n frames
        self.AI_FRAME_DELAY = 1  # Game will receive each inference n frames late
        self.BALL_MARKER_SIZE = 4  # Pixel height and width of experimental position markers
        self.CUSTOM = 0
        self.HIT_PRACTICE = 2
        self.CUSTOM_ACTION_SIZE = 3
        self.CUSTOM_STATE_SHAPE = self.HEIGHT // 2, self.WIDTH // 2
        self.CUSTOM_STATE_SIZE = self.HEIGHT // 2 * self.WIDTH // 2
        self.RANDOMIZE_START = True
        self.BALL_DIAMETER = 8
        self.PADDLE_HEIGHT = 3
        self.PADDLE_WIDTH = 20

        # The 0.5 offsets are a sad artifact of using pixel-centered instead of pixel grid aligned coordinates
        self.BOTTOM_PADDLE_Y = self.HEIGHT - 0.5 - self.PADDING
        self.TOP_PADDLE_Y = self.PADDING + 0.5

        self.ENV_TYPE = self.CUSTOM
        self.DEBUG = True
        self.ENABLE_AUDIO = False
        self.VOLLEY_SPEEDUP = 0.2  # Multiplier to ball speed after each paddle hit
        self.AUDIO_DIR = "C:\\dev\\DiscoveryWorld\\exhibit\\game\\resources\\"
        self.BALL_SPEED = 2
        self.BALL_BOUNCE_ANGLES = [-90, -30, -45, -60, -120, -135, -150]  # True to original Atari Pong
        self.BALL_START_ANGLES = [-90]#[210]#[90]
