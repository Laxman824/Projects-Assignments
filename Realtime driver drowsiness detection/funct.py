from picamera2 import Picamera2, Preview
import time
from scipy.spatial import distance

import dlib
import cv2
import RPi.GPIO as GPIO

# buzzer setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
BUZZER = 40
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.output(BUZZER, GPIO.LOW)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

facial_recogn_hog = dlib.get_frontal_face_detector()
dlib_facialmap_landmark = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

#declare 2 counter variables for frames and blinking count
BLINK_COUNT = 0
frame_count = 0

# count_sleep = 0
def fun(frame_count, CONSECUTIVE_FRAMES):
    count_sleep = 0
    if frame_count < CONSECUTIVE_FRAMES:
        pass
    else:
        count_sleep += 1
        cv2.putText(frame, "DROWSINESS ALERT!", (270, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        print("Drowsy")

def alarmbuzzer():
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(BUZZER, GPIO.LOW)
def HOG():
    while True:
        # Extract a frame
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = facial_recogn_hog(gray)
        for face in faces:
	    #keypoints_face is the face_landmarks which shows region or landmarks on face.
            keypoints_face = dlib_facialmap_landmark(gray, face)
            leftEye = []
            rightEye = []
            n = 36
            while (n < 42):

                leftEye.append((keypoints_face.part(n).x, keypoints_face.part(n).y))


                cv2.line(frame, (keypoints_face.part(n).x, keypoints_face.part(n).y),(keypoints_face.part(36 if n == 41 else n+1).x, keypoints_face.part(36 if n == 41 else n+1).y), (0, 255, 0), 1)
                n = n + 1
            n2 = 42
            while (n2 < 48):


                rightEye.append((keypoints_face.part(n).x, keypoints_face.part(n).y))
              #  next_point = n + 1
               # if n == 47:
                   # next_point = 42

                cv2.line(frame, (keypoints_face.part(n).x, keypoints_face.part(n).y),(keypoints_face.part(42 if n == 47 else n+1).x, keypoints_face.part(42 if n == 47 else n+1).y), (0, 255, 0), 1)
                n2 = n2 + 1
                y = distance.euclidean(leftEye[1], leftEye[5])

            EARLEFT = (y + distance.euclidean(leftEye[2], leftEye[4])) / (
                        2.0 * distance.euclidean(leftEye[0], leftEye[3]))
            EARRIGHT = (distance.euclidean(rightEye[1], rightEye[5]) + distance.euclidean(rightEye[2], rightEye[4])) / (
                        2.0 * distance.euclidean(rightEye[0], rightEye[3]))
            eye_aspect_ratio = round((EARLEFT + EARRIGHT) / 2, 2)
            if eye_aspect_ratio < 0.26:
                frame_count = frame_count + 1
                fun(frame_count, 30)


                alarmbuzzer()


            print(eye_aspect_ratio)


        cv2.imshow("Are you Sleepy", frame)

        threshold_point = cv2.waitKey(1)
        if threshold_point == 27:
            break


def main():
    HOG()
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()

