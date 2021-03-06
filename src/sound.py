import pygame, config

class SoundManager:
    _instance = None
    THEME_PATH = "res/audio/theme.mp3"
    BOUNCE_PATH = "res/audio/bounce.wav"
    BREAK_PATH = "res/audio/break.wav"
    HIT_WALL_PATH = "res/audio/hit_wall.wav"
    SCENE_TRANS_PATH = "res/audio/scene_trans.wav"
    WIN_PATH = "res/audio/win.wav"
    LOSE_PATH = "res/audio/lose.wav"
    LOSE_LIFE_PATH = "res/audio/lose_life.wav"

    def __init__(self):
        pygame.mixer.music.load(SoundManager.THEME_PATH)
        pygame.mixer.music.set_volume(0.5)
        self.bounce_effect = pygame.mixer.Sound(SoundManager.BOUNCE_PATH)
        self.break_effect = pygame.mixer.Sound(SoundManager.BREAK_PATH)
        self.hit_wall_effect = pygame.mixer.Sound(SoundManager.HIT_WALL_PATH)
        self.hit_wall_effect.set_volume(0.5)
        self.scene_trans_effect = pygame.mixer.Sound(SoundManager.SCENE_TRANS_PATH)
        self.win_effect = pygame.mixer.Sound(SoundManager.WIN_PATH)
        self.lose_effect = pygame.mixer.Sound(SoundManager.LOSE_PATH)
        self.lose_life_effect = pygame.mixer.Sound(SoundManager.LOSE_LIFE_PATH)

    def instance():
        if SoundManager._instance is None:
            SoundManager._instance = SoundManager()
        return SoundManager._instance

    def onToggleMusic(self):
        if config.ENABLE_MUSIC:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    def playTheme(self):
        if config.ENABLE_MUSIC:
            pygame.mixer.music.play(-1)

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

    def playLoseLifeEffect(self):
        if config.ENABLE_SFX:
            self.lose_life_effect.play()