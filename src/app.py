import argparse

import cv2
import numpy as np

from src.hand_tracker import HandTracker
from src.ui import draw_status, draw_volume_bar
from src.utils import FPSCounter, clamp, draw_fps, draw_label, open_camera, save_frame
from src.volume_controller import SystemVolumeController


def parse_args():
    parser = argparse.ArgumentParser(
        description="Gesture Volume Control - control Windows volume with hand gestures."
    )

    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Camera index. Default: 0",
    )

    parser.add_argument(
        "--width",
        type=int,
        default=640,
        help="Camera width. Default: 640",
    )

    parser.add_argument(
        "--height",
        type=int,
        default=480,
        help="Camera height. Default: 480",
    )

    parser.add_argument(
        "--min-distance",
        type=int,
        default=35,
        help="Thumb-index distance mapped to 0 percent volume.",
    )

    parser.add_argument(
        "--max-distance",
        type=int,
        default=220,
        help="Thumb-index distance mapped to 100 percent volume.",
    )

    parser.add_argument(
        "--smoothing",
        type=int,
        default=5,
        help="Volume step size. Default: 5",
    )

    parser.add_argument(
        "--mock-volume",
        action="store_true",
        help="Run the demo without changing system volume.",
    )

    parser.add_argument(
        "--no-mirror",
        action="store_true",
        help="Disable mirrored webcam view.",
    )

    return parser.parse_args()


def run(args):
    cap = open_camera(args.camera, args.width, args.height)

    tracker = HandTracker(
        max_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.7,
    )

    volume_controller = SystemVolumeController(mock=args.mock_volume)
    fps_counter = FPSCounter()

    window_name = "Gesture Volume Control"

    print("\nGesture Volume Control")
    print(volume_controller.message)
    print("Controls:")
    print("  q  - quit")
    print("  s  - save screenshot")
    print("\nGesture:")
    print("  Move thumb and index finger closer/farther to choose volume.")
    print("  Lower your pinky finger to apply the volume.\n")

    target_volume = volume_controller.get_volume_percent()

    while True:
        success, frame = cap.read()

        if not success:
            print("Failed to read frame from camera.")
            break

        if not args.no_mirror:
            frame = cv2.flip(frame, 1)

        frame = tracker.find_hands(frame, draw=True)
        landmarks, bbox = tracker.find_landmarks(frame, draw=False)

        is_active = False
        status = "Show one hand to start volume control."

        if landmarks:
            hand_area = ((bbox[2] - bbox[0]) * (bbox[3] - bbox[1])) // 100

            if 150 < hand_area < 1600:
                length, frame, line_info = tracker.find_distance(4, 8, frame, draw=True)

                target_volume = np.interp(
                    length,
                    [args.min_distance, args.max_distance],
                    [0, 100],
                )

                target_volume = clamp(target_volume, 0, 100)

                if args.smoothing > 0:
                    target_volume = args.smoothing * round(target_volume / args.smoothing)

                fingers = tracker.fingers_up()
                pinky_is_down = len(fingers) >= 5 and fingers[4] == 0

                if pinky_is_down:
                    volume_controller.set_volume_percent(target_volume)
                    is_active = True
                    status = "Volume applied. Raise pinky to pause changes."

                    cv2.circle(
                        frame,
                        (line_info[4], line_info[5]),
                        15,
                        (0, 255, 0),
                        cv2.FILLED,
                    )
                else:
                    status = "Lower pinky finger to apply selected volume."

            else:
                status = "Adjust your hand distance from the camera."

        current_volume = volume_controller.get_volume_percent()

        draw_label(frame, "Gesture Volume Control")
        draw_fps(frame, fps_counter.update())
        draw_volume_bar(frame, target_volume, current_volume, is_active)
        draw_status(frame, status, is_active)

        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            save_frame(frame, "gesture_volume_control")

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    args = parse_args()
    run(args)
