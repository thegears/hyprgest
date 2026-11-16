from hyprgest.camera import frame_stream
from hyprgest.gesture import GestureDetector
from hyprgest.ipc import execute_gesture
from hyprgest.tracker import Tracker


def main() -> None:
    tracker = Tracker()
    detector = GestureDetector()

    for frame in frame_stream():
        hand = tracker.get_hand(frame)
        if hand is None:
            continue

        gesture = detector.detect(hand)

        if gesture is None:
            continue

        execute_gesture(gesture)
