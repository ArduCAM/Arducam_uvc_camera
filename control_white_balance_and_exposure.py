import cv2
import time
import subprocess

"""
    Use keyboard control:
        q: exit the program
        a/d: Increase and decrease white balance value
        z/c: Increase and decrease exposure value
"""

WIDTH = 1920
HEIGHT = 1080
white_balance_temperature_value=5000
exposure_value = 500
exposure_step=50
white_balance_temperature_step=500
device=0


def sh(cmd):
    """ Execute shell commands """
    subprocess.check_call(cmd, shell=True)

# Open camera
cap = cv2.VideoCapture(device)

# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(width,height)
if width == WIDTH and height == HEIGHT:
    print("The width and height are set successfully.")

sh("v4l2-ctl -c white_balance_automatic=0 -d {}".format(device))
sh("v4l2-ctl -c white_balance_temperature={} -d {}".format(white_balance_temperature_value, device))

cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cap.set(cv2.CAP_PROP_EXPOSURE, 500)


# Display image
while(True):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('a'):
        if white_balance_temperature_value < 6500:
            white_balance_temperature_value += white_balance_temperature_step
            # sh("v4l2-ctl -l")
        print(white_balance_temperature_value)
        sh("v4l2-ctl -c white_balance_temperature={} -d {}".format(white_balance_temperature_value, device))
        sh("v4l2-ctl -l -d {} | grep white_balance_temperature".format(device))
    elif key == ord('d'):
        if white_balance_temperature_value > 2800:
            white_balance_temperature_value -= white_balance_temperature_step
        print(white_balance_temperature_value)
        sh("v4l2-ctl -c white_balance_temperature={} -d {}".format(white_balance_temperature_value, device))
        sh("v4l2-ctl -l -d {} | grep white_balance_temperature".format(device))
    elif key == ord('z'):
        if exposure_value < 5000:
            exposure_value += exposure_step
        print(exposure_value)
        sh("v4l2-ctl -c exposure_time_absolute={} -d {}".format(exposure_value, device))
        sh("v4l2-ctl -l -d {} | grep exposure_time_absolute".format(device))
    elif key == ord('c'):
        if exposure_value > 0:
            exposure_value -= exposure_step
        print(exposure_value)
        sh("v4l2-ctl -c exposure_time_absolute={} -d {}".format(exposure_value, device))
        sh("v4l2-ctl -l -d {} | grep exposure_time_absolute".format(device))

