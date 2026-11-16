from collections.abc import Iterator

import cv2
import numpy as np


def frame_stream(camera: int = 0) -> Iterator[np.ndarray]:
    cap = cv2.VideoCapture(camera)

    try:
        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                break

            yield frame

    finally:
        cap.release()
