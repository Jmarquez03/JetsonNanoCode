from djitellopy import Tello
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from yolo import YOLO
import time
from threading import Thread
######################################################################
width = 640  # WIDTH OF THE IMAGE
height = 480  # HEIGHT OF THE IMAGE
deadZone =100
######################################################################
mpad = 1
global startCounter

# CONNECT TO TELLO
me = Tello()
me.connect()
me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0

camera = 0
mpad = 1
print(me.get_battery())

me.streamoff()
me.streamon()
########################

frameWidth = width
frameHeight = height
global imgContour
global dir;
global detected_values
global threadender
global gababool
detected_values = []


#this will check the file for the qr code
def startCheck():
    with open('QRCodes.txt', 'r') as file:
        for line in file:
            detected_values.append(line)
            if len(detected_values) > 0:
                startCounter = 0


def check(search_string):
    with open('QRCodes.txt', 'r') as file:
        for line in file:
            if line.strip() == search_string:
                detected_values.append(search_string)
                return True
    return False


def write(x, y):
    with open('Coordinates.txt', 'w') as file:
        coordinate_tuple = (x, y)
        file.write("{}\n".format(coordinate_tuple))


def yolo(img):
    # detection
    global dir
    _yolo = YOLO()
    b, c, i = _yolo.detect(img)
    imgbox = _yolo.draw_boxes(img, b, i)
    if (b[0] < int(frameWidth / 2) - deadZone):
        cv2.putText(imgContour, " CCW ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
        cv2.rectangle(imgContour, (0, int(frameHeight / 2 - deadZone)),
                      (int(frameWidth / 2) - deadZone, int(frameHeight / 2) + deadZone), (0, 0, 255), cv2.FILLED)
        dir = 1
    elif (b[0] > int(frameWidth / 2) + deadZone):
        cv2.putText(imgContour, " CW ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
        cv2.rectangle(imgContour, (int(frameWidth / 2 + deadZone), int(frameHeight / 2 - deadZone)),
                      (frameWidth, int(frameHeight / 2) + deadZone), (0, 0, 255), cv2.FILLED)
        dir = 2
    elif (b[1] < int(frameHeight / 2) - deadZone):
        cv2.putText(imgContour, "Forward", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
        cv2.rectangle(imgContour, (int(frameWidth / 2 - deadZone), 0),
                      (int(frameWidth / 2 + deadZone), int(frameHeight / 2) - deadZone), (0, 0, 255), cv2.FILLED)
        dir = 3
    elif (b[1] > int(frameHeight / 2) + deadZone):
        cv2.putText(imgContour, "Scan QR code ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
        cv2.rectangle(imgContour, (int(frameWidth / 2 - deadZone), int(frameHeight / 2) + deadZone),
                      (int(frameWidth / 2 + deadZone), frameHeight), (0, 0, 255), cv2.FILLED)
        dir = 4
    elif (b[0] < int(frameWidth / 2) - deadZone) and (b[0] > int(frameWidth / 2) + deadZone) and (b[1] < int(frameHeight / 2) - deadZone) and (b[1] > int(frameHeight / 2) + deadZone):
        dir = 4
    else:
        dir = 5
    # publish image
    return imgbox


def display(img):
    cv2.line(img,(int(frameWidth/2)-deadZone,0),(int(frameWidth/2)-deadZone,frameHeight),(255,255,0),3)
    cv2.line(img,(int(frameWidth/2)+deadZone,0),(int(frameWidth/2)+deadZone,frameHeight),(255,255,0),3)
    cv2.circle(img,(int(frameWidth/2),int(frameHeight/2)),5,(0,0,255),5)
    cv2.line(img, (0,int(frameHeight / 2) - deadZone), (frameWidth,int(frameHeight / 2) - deadZone), (255, 255, 0), 3)
    cv2.line(img, (0, int(frameHeight / 2) + deadZone), (frameWidth, int(frameHeight / 2) + deadZone), (255, 255, 0), 3)


def scan(img):
    me.send_command_with_return("downvision 1")
    # We can use a for loop to scan multiple barcodes at once or bring in a constant feed
    gabababool = True
    while gabababool:
        cv2.resize(img, (360, 240))
        for barcode in decode(img):
            # We can change the information in the barcode into a string
            myData = barcode.data.decode('utf-8')
            # print out the data on the QR or bar code
            print(myData)
            # Creating the array which will allow us to determine the points around the QR code
            #pts = np.array([barcode.polygon], np.int32)
            #pts = pts.reshape((-1, 1, 2))
            # function for the polygon which will surround the code
            #cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            # Displaying the contents of the QR code on the screen above the Qr code in real time
            # We use rect since we don't want the text to be positioned at a weird angle
            #pts2 = barcode.rect
            #cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
            gabababool = False
            while me.get_mission_pad_distance_x() == -100:
                me.rotate_clockwise(45)
            write(((me.get_mission_pad_distance_x() * -1), me.get_mission_pad_distance_y() * -1))
            me.send_command_with_return("downvision 0")
            break
        # Display the image and refresh every millisecond
        #cv2.imshow('Result', img)
        cv2.waitKey(1)

    # GET THE IMAGE FROM TELLO
frame_read = me.get_frame_read()
myFrame = frame_read.frame
img = cv2.resize(myFrame, (width, height))
imgContour = yolo(img)
display(imgContour)

################ FLIGHT
startCounter = 1
while startCounter == 1:
    startCheck()
if startCounter == 0:
    time.sleep(15)
    me.takeoff()
    startCounter = 1
while True:
    if dir == 1:
        me.yaw_velocity = -60
    elif dir == 2:
        me.yaw_velocity = 60
    elif dir == 3:
        me.for_back_velocity = 60
    elif dir == 4:
        me.enable_mission_pads()
        p1 = Thread(target=scan(img))
        p1.start()
        me.move_up(60)
        while gababool == True:
            me.move_forward(30)
            iteration = 0
            iteration += 1
            if iteration > 3:
                break
        if gababool == False:
            me.send_command_with_return("mdirection 2")
            me.send_command_with_return("go 0 0 50 m" + str(mpad))
            me.land()
        me.disable_mission_pad()
    else:
       me.left_right_velocity = 0; me.for_back_velocity = 0;me.up_down_velocity = 0; me.yaw_velocity = 0
       me.rotate_clockwise(15)

   # SEND VELOCITY VALUES TO TELLO
    if me.send_rc_control:
        me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)
    print(dir)
    for value in detected_values:
        if value == "Done":
            me.enable_mission_pads()
            me.send_command_with_return("mdirection 2")
            me.send_command_with_return("go 0 0 50 m" + str(mpad))
            me.land()
            me.emergency()
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break

# cap.release()
cv2.destroyAllWindows()
