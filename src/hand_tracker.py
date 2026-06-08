import math

import cv2
import mediapipe as mp


class HandTracker:
    """MediaPipe-based hand tracking helper."""

    def __init__(
        self,
        static_image_mode=False,
        max_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.7,
    ):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

        self.results = None
        self.landmarks = []
        self.handedness = None
        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hands(self, frame, draw=True):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)

        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                )

        return frame

    def find_landmarks(self, frame, hand_index=0, draw=True):
        self.landmarks = []
        self.handedness = None

        if not self.results or not self.results.multi_hand_landmarks:
            return [], (0, 0, 0, 0)

        if hand_index >= len(self.results.multi_hand_landmarks):
            return [], (0, 0, 0, 0)

        hand_landmarks = self.results.multi_hand_landmarks[hand_index]

        if self.results.multi_handedness:
            classification = self.results.multi_handedness[hand_index].classification[0]
            self.handedness = classification.label

        height, width, _ = frame.shape
        x_values = []
        y_values = []

        for landmark_id, landmark in enumerate(hand_landmarks.landmark):
            x = int(landmark.x * width)
            y = int(landmark.y * height)

            x_values.append(x)
            y_values.append(y)
            self.landmarks.append([landmark_id, x, y])

            if draw:
                cv2.circle(frame, (x, y), 5, (255, 0, 255), cv2.FILLED)

        if not x_values:
            return self.landmarks, (0, 0, 0, 0)

        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)
        bbox = (x_min, y_min, x_max, y_max)

        if draw:
            cv2.rectangle(
                frame,
                (x_min - 20, y_min - 20),
                (x_max + 20, y_max + 20),
                (0, 255, 0),
                2,
            )

        return self.landmarks, bbox

    def fingers_up(self):
        if len(self.landmarks) < 21:
            return []

        fingers = []

        # Thumb logic depends on hand side.
        if self.handedness == "Left":
            thumb_is_up = self.landmarks[4][1] > self.landmarks[3][1]
        else:
            thumb_is_up = self.landmarks[4][1] < self.landmarks[3][1]

        fingers.append(1 if thumb_is_up else 0)

        # Other fingers are checked using y-position.
        for finger_id in range(1, 5):
            tip_id = self.tip_ids[finger_id]
            pip_id = tip_id - 2

            finger_is_up = self.landmarks[tip_id][2] < self.landmarks[pip_id][2]
            fingers.append(1 if finger_is_up else 0)

        return fingers

    def find_distance(self, point_1, point_2, frame, draw=True):
        if len(self.landmarks) <= max(point_1, point_2):
            return 0, frame, [0, 0, 0, 0, 0, 0]

        x1, y1 = self.landmarks[point_1][1], self.landmarks[point_1][2]
        x2, y2 = self.landmarks[point_2][1], self.landmarks[point_2][2]

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        if draw:
            cv2.circle(frame, (x1, y1), 12, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 12, (255, 0, 255), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(frame, (center_x, center_y), 12, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        line_info = [x1, y1, x2, y2, center_x, center_y]

        return length, frame, line_info
