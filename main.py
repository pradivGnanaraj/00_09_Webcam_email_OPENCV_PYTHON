import cv2
from emailing import send_email
import glob
import os
from threading import Thread
import time

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


while True:
    status = 0
    check, frame = video.read()

    # converting to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21,21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # making the static video to black and frames to white
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    # removing some noise
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    # Creating contours
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # removing false positives
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            # sending email after the object exists
            status = 1
            # saving the images
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            # preparing the middle images
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        # To avoid freezing, introducing threading

        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True

        clean_thread = Thread(target=clean_folder)
        email_thread.daemon = True
        # Begin Thread 1
        email_thread.start()

    print(status_list)
    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
# Begin thread 2
clean_thread.start()
