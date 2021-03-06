import pygame, config

class SoundManager:
    _instance = None
    THEME_PATH = "res/theme.mp3"
    BOUNCE_PATH = "res/bounce.wav"
    BREAK_PATH = "res/break.wav"
    HIT_WALL_PATH = "res/hit_wall.wav"
    SCENE_TRANS_PATH = "res/scene_trans.wav"
    WIN_PATH = "res/win.wav"
    LOSE_PATH = "res/lose.wav"

    def __init__(self):
        self.theme_music = pygame.mixer.Sound(SoundManager.THEME_PATH)
        self.bounce_effect = pygame.mixer.Sound(SoundManager.BOUNCE_PATH)
        self.break_effect = pygame.mixer.Sound(SoundManager.BREAK_PATH)
        self.hit_wall_effect = pygame.mixer.Sound(SoundManager.HIT_WALL_PATH)
        self.scene_trans_effect = pygame.mixer.Sound(SoundManager.SCENE_TRANS_PATH)
        self.win_effect = pygame.mixer.Sound(SoundManager.WIN_PATH)
        self.lose_effect = pygame.mixer.Sound(SoundManager.LOSE_PATH)

    def instance():
        if SoundManager._instance is None:
            SoundManager._instance = SoundManager()
        return SoundManager._instance

    def onToggleMusic(self):
        if config.ENABLE_MUSIC:
            self.theme_music.play(-1)
        else:
            self.theme_music.stop()

    def playTheme(self):
        if config.ENABLE_MUSIC:
            self.theme_music.play()

    def playCollideWithBorderEffect(self):
        if config.ENABLE_SFX:
            self.hit_wall_effect.play()

    def playCollideWithPieceEffect(self):
        if config.ENABLE_SFX:
            self.break_effect.play()

    def playCollideWithBarEffect(self):
        if config.ENABLE_SFX:
            self.bounce_effect.play()

    def playSceneTransitionEffect(self):
        if config.ENABLE_SFX:
            self.scene_trans_effect.play()

    def playWinEffect(self):
        if config.ENABLE_SFX:
            self.win_effect.play()

    def playLoseEffect(self):
        if config.ENABLE_SFX:
            self.lose_effect.play()