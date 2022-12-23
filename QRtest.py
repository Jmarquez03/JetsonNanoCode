import cv2
import numpy as np
from pyzbar.pyzbar import decode

# enable video from the webcam
cap = cv2.VideoCapture(0)
"""Width and height of the window that displays the webcam footage
    cap.set(id (3 = width, 4 = height), pixels) """
cap.set(3, 640)
cap.set(4, 480)

while True:
    # If the program is capable or gathering info from the webcam, we read the image
    success, img = cap.read()
    # We can use a for loop to scan multiple barcodes at once or bring in a constant feed
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
    # Display the image and refresh every millisecond
    cv2.imshow('Result',  img)
    cv2.waitKey(1)
