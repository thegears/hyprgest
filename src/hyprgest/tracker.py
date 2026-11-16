import time

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from hyprgest.models import Finger, FingerType, Hand, Point


class Tracker:
    def __init__(self, model_path: str = "assets/hand_landmarker.task"):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
        )
        self._landmarker = vision.HandLandmarker.create_from_options(options)

    def get_hand(self, frame: np.ndarray) -> Hand | None:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp_ms = int(time.monotonic() * 1000)
        result = self._landmarker.detect_for_video(mp_image, timestamp_ms)

        if result.hand_landmarks:
            hand = result.hand_landmarks[0]

            def to_point(idx: int) -> Point:
                lm = hand[idx]
                return Point(lm.x, lm.y, lm.z)

            return Hand(
                thumb=Finger(FingerType.THUMB, tip=to_point(4), pip=to_point(3)),
                index=Finger(FingerType.INDEX, tip=to_point(8), pip=to_point(6)),
                middle=Finger(FingerType.MIDDLE, tip=to_point(12), pip=to_point(10)),
                ring=Finger(FingerType.RING, tip=to_point(16), pip=to_point(14)),
                pinky=Finger(FingerType.PINKY, tip=to_point(20), pip=to_point(18)),
                palm=to_point(9),
            )
        return None
