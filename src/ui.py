import cv2


def draw_volume_bar(frame, target_volume, current_volume, is_active):
    bar_x1 = 50
    bar_y1 = 150
    bar_x2 = 85
    bar_y2 = 400

    fill_y = int(400 - (target_volume / 100) * 250)

    active_color = (0, 255, 0)
    inactive_color = (255, 0, 0)
    color = active_color if is_active else inactive_color

    cv2.rectangle(frame, (bar_x1, bar_y1), (bar_x2, bar_y2), color, 3)
    cv2.rectangle(frame, (bar_x1, fill_y), (bar_x2, bar_y2), color, cv2.FILLED)

    cv2.putText(
        frame,
        f"Target: {int(target_volume)}%",
        (35, 445),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        color,
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        f"System: {int(current_volume)}%",
        (390, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        color,
        2,
        cv2.LINE_AA,
    )


def draw_status(frame, text, is_active):
    color = (0, 255, 0) if is_active else (0, 180, 255)

    cv2.rectangle(frame, (20, 430), (620, 475), (20, 20, 20), cv2.FILLED)

    cv2.putText(
        frame,
        text,
        (30, 460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2,
        cv2.LINE_AA,
    )
