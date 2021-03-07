import pygame, math

class Buff:
    POSITIVE = 1
    NEGATIVE = -1
    groups = [
        ["LongerBuff"]
    ]

    def __init__(self, type, time, rate):
        self.type = type
        self.time = time
        self.rate = rate

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def draw(self, screen):
        pass

    def renew(self):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass

class BiggerBuff(Buff):
    _instance = None

    def __init__(self):
        super().__init__(Buff.POSITIVE, 10, 0.1)

class SmallerBuff(Buff):
    _instance = None

    def __init__(self):
        super().__init__(Buff.NEGATIVE, 10, 0.1)

class LongerBuff(Buff):
    _instance = None

    def __init__(self):
        super().__init__(Buff.POSITIVE, 10, 0.1)

class ShorterBuff(Buff):
    _instance = None
    
    def __init__(self):
        super().__init__(Buff.NEGATIVE, 10, 0.1)

class StrongerBuff(Buff):
    _instance = None

    def __init__(self):
        super().__init__(Buff.POSITIVE, 10, 0.1)

class DenserBuff(Buff):
    _instance = None

    def __init__(self):
        super().__init__(Buff.POSITIVE, 10, 0.1)