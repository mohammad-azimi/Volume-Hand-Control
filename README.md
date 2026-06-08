# Gesture Volume Control

A real-time computer vision project that lets you control the Windows system volume using hand gestures.

This project uses a webcam, OpenCV, MediaPipe hand tracking, and Pycaw to map the distance between the thumb and index finger to the system volume level.

## Overview

Gesture Volume Control is an interactive computer vision application built with Python.

The application detects hand landmarks in real time, calculates the distance between the thumb and index finger, converts that distance into a volume percentage, and applies the value to the Windows system volume.

The project was originally created as a learning exercise and has been refactored into a cleaner, portfolio-ready structure.

## Features

- Real-time hand tracking
- Gesture-based system volume control
- Thumb and index finger distance measurement
- Pinky-finger lock mechanism to prevent accidental volume changes
- Live volume bar visualization
- FPS display
- Screenshot saving
- Mock mode for testing without changing system volume
- Clean modular Python structure
- Beginner-friendly code organization

## How It Works

1. The webcam captures a live video stream.
2. MediaPipe detects hand landmarks.
3. The app tracks the thumb tip and index finger tip.
4. The distance between those two fingers is mapped to a volume percentage.
5. When the pinky finger is down, the selected volume is applied.
6. When the pinky finger is up, the selected volume is only previewed.

## Project Structure

```text
Volume-Hand-Control/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── hand_tracker.py
│   ├── ui.py
│   ├── utils.py
│   └── volume_controller.py
│
├── legacy/
│   ├── VolumeHandControl.py
│   └── HandTrackingModule.py
│
└── outputs/
    └── saved screenshots
```

## Technologies Used

- Python
- OpenCV
- MediaPipe
- Pycaw
- NumPy
- Comtypes

## Installation

Clone the repository:

```bash
git clone https://github.com/mohammad-azimi/Volume-Hand-Control.git
cd Volume-Hand-Control
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

Run with another camera index:

```bash
python main.py --camera 1
```

Run in mock mode without changing system volume:

```bash
python main.py --mock-volume
```

Disable mirrored webcam view:

```bash
python main.py --no-mirror
```

## Controls

Inside the OpenCV window:

- Press `q` to quit
- Press `s` to save a screenshot

## Gesture Controls

- Move your thumb and index finger closer to lower the volume.
- Move your thumb and index finger farther apart to increase the volume.
- Lower your pinky finger to apply the selected volume.
- Raise your pinky finger to pause volume changes.

## Notes

- System volume control works on Windows.
- On other operating systems, use mock mode to test the computer vision interface.
- Good lighting improves hand tracking accuracy.
- Keep one hand clearly visible in front of the webcam.

## What I Learned

Through this project, I practiced:

- Real-time computer vision with OpenCV
- Hand landmark detection with MediaPipe
- Gesture-based interaction design
- Mapping visual measurements to system actions
- Windows audio control with Pycaw
- Structuring Python code into reusable modules
- Improving a learning project into a portfolio-ready repository

## Roadmap

Planned improvements:

- Add demo screenshots and GIF previews
- Add calibration mode
- Add mute/unmute gesture
- Add left-hand/right-hand settings
- Add a small graphical settings panel
- Add tests for helper functions
- Improve packaging and installation flow

## Credits

This project was inspired by beginner-friendly hand tracking and computer vision tutorials, especially Murtaza's Workshop.

## Author

Mohammad Azimi

- GitHub: [mohammad-azimi](https://github.com/mohammad-azimi)
- Portfolio: [mohammad-azimi.github.io](https://mohammad-azimi.github.io/)
=======
Volume Hand Control

Overview

Welcome to the Volume Hand Control project! This innovative application utilizes hand tracking to control volume levels in real-time, offering an intuitive interface for users. By leveraging advanced techniques in computer vision and machine learning, this project transforms your hand gestures into commands, allowing for seamless interaction with audio devices.

Features

Hand Tracking: Accurately detects and tracks hand landmarks using MediaPipe, ensuring responsiveness and precision.

Gesture Recognition: Customize your hand gestures to control volume levels, making it user-friendly and adaptable to individual preferences.

Real-Time Feedback: The application provides instant visual feedback, displaying hand positions and volume levels on-screen.

Easy Integration: Designed to be easily integrated into existing audio applications or devices.

Technologies Used

Python: The primary programming language for this project.

OpenCV: Utilized for image processing and real-time video capture.

MediaPipe: A powerful library for hand tracking and landmark detection.

Mathematics: Employed for calculating distances between hand landmarks.

Getting Started

To run the Volume Hand Control application:

1. Navigate to the project directory:

cd Volume-Hand-Control

2. Install the required libraries:

pip install opencv-python mediapipe

3. Run the application:

python VolumeHandControl.py

Inspiration

This project was developed with the invaluable guidance of https://www.youtube.com/c/MurtazasWorkshop, a fantastic resource for learning about robotics and AI. Their tutorials and insights have greatly influenced the development of this application.
>>>>>>> 65d80db3f411d32d23bc873e4978526fbc2ef1ab
