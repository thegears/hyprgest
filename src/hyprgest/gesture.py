import time
from collections import deque

from hyprgest.models import Gesture, Hand


class GestureDetector:
    def __init__(
        self,
        history_len: int = 8,
        threshold: float = 0.25,
        cooldown: float = 0.6,
    ) -> None:
        self._x_history: deque[float] = deque(maxlen=history_len)
        self._history_len = history_len
        self._threshold = threshold
        self._cooldown = cooldown
        self._last_trigger = 0.0

    def detect(self, hand: Hand | None) -> Gesture | None:
        if hand is None:
            self._x_history.clear()
            return None

        now = time.monotonic()
        if now - self._last_trigger < self._cooldown:
            return None

        if hand.is_closed:
            self._x_history.clear()
            return None

        self._x_history.append(hand.palm.x)

        if len(self._x_history) < self._history_len:
            return None

        delta_x = self._x_history[-1] - self._x_history[0]

        if abs(delta_x) > self._threshold:
            self._x_history.clear()
            self._last_trigger = now
            return Gesture.SWIPE_RIGHT if delta_x < 0 else Gesture.SWIPE_LEFT

        return None
