from dataclasses import dataclass
from enum import Enum, auto


@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float
    z: float


@dataclass(frozen=True, slots=True)
class Hand:
    thumb: Finger
    index: Finger
    middle: Finger
    ring: Finger
    pinky: Finger
    palm: Point

    @property
    def is_closed(self) -> bool:
        fingers = (self.thumb, self.index, self.middle, self.ring, self.pinky)
        return not any(f.is_opened for f in fingers)


@dataclass(frozen=True, slots=True)
class Finger:
    kind: FingerType
    tip: Point
    pip: Point

    @property
    def is_opened(self) -> bool:
        if self.kind == FingerType.THUMB:
            return self.tip.x < self.pip.x
        return self.tip.y < self.pip.y


class FingerType(Enum):
    THUMB = auto()
    INDEX = auto()
    MIDDLE = auto()
    RING = auto()
    PINKY = auto()


class Gesture(Enum):
    SWIPE_LEFT = auto()
    SWIPE_RIGHT = auto()
