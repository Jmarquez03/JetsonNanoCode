import cv2
from threading import Thread
from djitellopy import Tello
import numpy as np
from pyzbar.pyzbar import decode
tello = Tello()
camera = 1
tello.connect()
tello.streamon()
global img
tello.send_command_with_return("setbitrate 5")
tello.send_command_with_return("setfps high")
tello.send_command_with_return("setresolution high")
remainScanning = True

def scan():
    tello.send_command_with_return("downvision " + str(camera))
    # We can use a for loop to scan multiple barcodes at once or bring in a constant feed
    while True:
        img = tello.get_frame_read().frame
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
#need to focus on getting the right scans going on
print(tello.get_battery())
p1 = Thread(target=scan)
p1.start()
tello.takeoff()
for i in range(5):
    tello.move_forward(30)
tello.rotate_counter_clockwise(90)
tello.move_forward(60)
tello.land()
'''for i in range(4):
    tof = tello.send_command_with_return("EXT tof?")
    ex = ''.join(x for x in tof if x.isdigit())
    if int(ex) <= 990:
        tello.send_command_with_return("cw 90")
    else:
        tello.send_command_with_return("forward 50")
tello.land()'''
remainScanning = False
