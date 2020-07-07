import cv2
import numpy as np
import os
import math

class CapturePic:
    # calculate scan bed area in pixels
    def calculateArea(self, box):
        print(box)
        x1 = box[0][0]
        y1 = box[0][1]
        x2 = box[1][0]
        y2 = box[1][1]
        x3 = box[2][0]
        y3 = box[2][1]
        print("1 " + str(x1) + ", " + str(y1))
        print("2 " + str(x2) + ", " + str(y2))
        print("3 " + str(x3) + ", " + str(y3))
        a1 = abs(x1 - x2)
        b1 = abs(y1-y2)
        c1 = math.sqrt(a1*a1 + b1*b1)
        print("rectangle side length")
        print(c1)
        a2 = abs(x2 - x3)
        b2 = abs(y2-y3)
        c2 = math.sqrt(a2*a2 + b2*b2)
        print(c2)
        area = c1 * c2
        return area

    def capturePic(self):
        camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #width
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024) #height
        return_value, image = camera.read()
        camera.release()
        cv2.destroyAllWindows()

        image2 = image

        # Convert BGR to gray
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Otsu's thresholding after Gaussian filtering
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(th3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # OTSU
        if len(contours) != 0:
            # draw in blue the contours that were found
            #cv2.drawContours(image, contours, -1, 255, 3)

            # find the biggest countour (c) by the area
            c = max(contours, key = cv2.contourArea)
            print(c)
            #x,y,w,h = cv2.boundingRect(c)

            # draw the biggest contour (c) in green
            #cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            area = self.calculateArea(box)
            print(area)
            boxInt = np.int0(box)
            cv2.drawContours(image,[boxInt],0,(0,0,255),2)

        # show the images
        #cv2.imshow("Result", np.hstack([image, output]))
        #cv2.imshow("gray", gray)
        cv2.imwrite("OTSU.png", image)
        cv2.imwrite("OTSU0.png", th3)
        #cv2.imshow("thresh", thresh)
        #cv2.imshow("adaptive",th3)
        #cv2.imshow("image", image)

        #cv2.waitKey(0)
        im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return im_rgb

    # Use this function to find your camera's max resolution
    # https://en.wikipedia.org/wiki/List_of_common_resolutions
    def set_res(self, x,y):
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
        print(str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) + " " + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        return_value, image = cap.read()
        cap.release()
        cv2.destroyAllWindows()
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

if __name__ == '__main__':
    cp = CapturePic()
    image = cp.capturePic()

    #cp.set_res(640,	480)   # VGA
    #cp.set_res(800,	600)   # SVGA
    #cp.set_res(1280, 1024) # SXGA

