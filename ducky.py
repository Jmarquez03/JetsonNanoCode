from djitellopy import Tello
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from yolo import YOLO
######################################################################
width = 640  # WIDTH OF THE IMAGE
height = 480  # HEIGHT OF THE IMAGE
deadZone =100
######################################################################

startCounter =0

# CONNECT TO TELLO
me = Tello()
me.connect()
me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0

camera = 0

print(me.get_battery())

me.streamoff()
me.streamon()
########################

frameWidth = width
frameHeight = height
# cap = cv2.VideoCapture(1)
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)
# cap.set(10,200)
global imgContour
global dir;
def empty(a):
    pass
#cv2.namedWindow("Parameters")
#cv2.resizeWindow("Parameters",640,240)
#cv2.createTrackbar("Threshold1","Parameters",166,255,empty)
#cv2.createTrackbar("Threshold2","Parameters",171,255,empty)
#cv2.createTrackbar("Area","Parameters",1750,30000,empty)



global imgContour
global dir;
def empty(a):
    pass


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
    else:
        dir = 5
    # publish image
    return imgbox

'''def getContours(img,imgContour):
    global dir
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #print(len(approx))
            x , y , w, h = cv2.boundingRect(approx)
            cx = int(x + (w / 2))  # CENTER X OF THE OBJECT
            cy = int(y + (h / 2))  # CENTER X OF THE OBJECT

            if (cx <int(frameWidth/2)-deadZone):
                cv2.putText(imgContour, " CCW " , (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(0,int(frameHeight/2-deadZone)),(int(frameWidth/2)-deadZone,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
                dir = 1
            elif (cx > int(frameWidth / 2) + deadZone):
                cv2.putText(imgContour, " CW ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2+deadZone),int(frameHeight/2-deadZone)),(frameWidth,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
                dir = 2
            elif (cy < int(frameHeight / 2) - deadZone):
                cv2.putText(imgContour, "Forward", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),0),(int(frameWidth/2+deadZone),int(frameHeight/2)-deadZone),(0,0,255),cv2.FILLED)
                dir = 3
            elif (cy > int(frameHeight / 2) + deadZone):
                cv2.putText(imgContour, "Scan QR code ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),int(frameHeight/2)+deadZone),(int(frameWidth/2+deadZone),frameHeight),(0,0,255),cv2.FILLED)
                dir = 4
            else:
                dir = 5

            cv2.line(imgContour, (int(frameWidth/2),int(frameHeight/2)), (cx,cy),(0, 0, 255), 3)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
        else: dir = 0
'''
def display(img):
    cv2.line(img,(int(frameWidth/2)-deadZone,0),(int(frameWidth/2)-deadZone,frameHeight),(255,255,0),3)
    cv2.line(img,(int(frameWidth/2)+deadZone,0),(int(frameWidth/2)+deadZone,frameHeight),(255,255,0),3)
    cv2.circle(img,(int(frameWidth/2),int(frameHeight/2)),5,(0,0,255),5)
    cv2.line(img, (0,int(frameHeight / 2) - deadZone), (frameWidth,int(frameHeight / 2) - deadZone), (255, 255, 0), 3)
    cv2.line(img, (0, int(frameHeight / 2) + deadZone), (frameWidth, int(frameHeight / 2) + deadZone), (255, 255, 0), 3)


def scan(img):
    me.send_command_with_return("downvision " + str(camera))
    # We can use a for loop to scan multiple barcodes at once or bring in a constant feed
    while True:
        cv2.resize(img, (360, 240))
        for barcode in decode(img):
            # We can change the information in the barcode into a string
            myData = barcode.data.decode('utf-8')
            # print out the data on the QR or bar code
            print(myData)
            # Creating the array which will allow us to determine the points around the QR code
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            # function for the polygon which will surround the code
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            # Displaying the contents of the QR code on the screen above the Qr code in real time
            # We use rect since we don't want the text to be positioned at a weird angle
            pts2 = barcode.rect
            cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
        '''if camera == 0:
            camera = 1

        else:
            camera = 0'''
        # Display the image and refresh every millisecond
        cv2.imshow('Result', img)
        cv2.waitKey(1)
while True:

    # GET THE IMAGE FROM TELLO
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))
    imgContour = yolo(img)
    #imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    '''h_min = cv2.getTrackbarPos("HUE Min","HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")'''


    #lower = np.array([h_min,s_min,v_min])
    #upper = np.array([h_max,s_max,v_max])
    #mask = cv2.inRange(imgHsv,lower,upper)
    #result = cv2.bitwise_and(img,img, mask = mask)
    #mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    #imgBlur = cv2.GaussianBlur(result, (7, 7), 1)
    #imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    #threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    #threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    #imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    #kernel = np.ones((5, 5))
    #imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    #getContours(imgDil, imgContour)
    display(imgContour)


    ################# FLIGHT
    if startCounter == 0:
       me.takeoff()
       startCounter = 1


    if dir == 1:
       me.yaw_velocity = -60
    elif dir == 2:
       me.yaw_velocity = 60
    elif dir == 3:
       me.for_back_velocity = 60
    elif dir == 4:
       me.scan(img)
    else:
       me.left_right_velocity = 0; me.for_back_velocity = 0;me.up_down_velocity = 0; me.yaw_velocity = 0
   # SEND VELOCITY VALUES TO TELLO
    if me.send_rc_control:
       me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)
    print(dir)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break

# cap.release()
cv2.destroyAllWindows()