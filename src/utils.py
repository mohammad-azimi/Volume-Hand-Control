from datetime import datetime
from pathlib import Path
import time

import cv2


OUTPUT_DIR = Path("outputs")


class FPSCounter:
    """Simple FPS counter for real-time video processing."""

    def __init__(self):
        self.previous_time = time.time()
        self.fps = 0.0

    def update(self):
        current_time = time.time()
        elapsed = current_time - self.previous_time

        if elapsed > 0:
            self.fps = 1.0 / elapsed

        self.previous_time = current_time
        return self.fps


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def open_camera(camera_index=0, width=640, height=480):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open camera with index {camera_index}. "
            "Try another camera index, for example: --camera 1"
        )

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    return cap


def draw_label(frame, text, position=(20, 40), scale=0.7):
    x, y = position

    cv2.rectangle(
        frame,
        (x - 10, y - 28),
        (x + 430, y + 10),
        (20, 20, 20),
        thickness=-1,
    )

    cv2.putText(
        frame,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    return frame


def draw_fps(frame, fps):
    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    return frame


def save_frame(frame, prefix):
    OUTPUT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = OUTPUT_DIR / f"{prefix}_{timestamp}.png"

    cv2.imwrite(str(path), frame)
    print(f"Saved screenshot: {path}")

    return path
