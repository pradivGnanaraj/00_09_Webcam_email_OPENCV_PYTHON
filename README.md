# Motion Detection and Email Notification System

This project implements a motion detection and email notification system using Python and OpenCV. The system captures video from the webcam, detects motion, captures images of detected motion, and sends email notifications using Gmail.

## Main Components

### main.py

This script captures video from the webcam, processes frames to detect motion, and sends email notifications upon detecting motion.

#### Key Features:
- Initializes webcam and captures video stream.
- Applies motion detection algorithm to identify moving objects.
- Captures frames of detected motion and saves them in the "images" folder.
- Initiates email notifications using threading to avoid freezing the main thread.

### emailing.py

This module handles sending email notifications with attached images using the Gmail SMTP server.

#### Key Features:
- Sends email notifications to a specified email address.
- Attaches captured images of detected motion to the email.
- Uses threading to avoid interrupting the main process.

## Setup Instructions

1. Install required libraries:
   ```bash
   pip install opencv-python imghdr
   ```

2. Replace the placeholders in `emailing.py` with your Gmail credentials.

3. Run `main.py` to start the motion detection and email notification system.

## Folder Structure

- `images`: This folder stores the images captured when motion is detected.
- `main.py`: The main script responsible for motion detection and email notifications.
- `emailing.py`: The script handling the sending of email notifications.
```
