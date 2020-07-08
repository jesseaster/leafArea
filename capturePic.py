import cv2
import numpy as np
import os
import math

class CapturePic:
    def __init__(self):
        self.bedWidthcm = 60 # 60 cm
        self.bedHeightcm = 60 # 60 cm
        self.bedAreacm = 3600 # 3600 sq cm
        self.bedCropcm = 2 # Crop inward 2 cm on all sides of the bed

    def capturePic(self):
        camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        # CAP_PROP_EXPOSURE Exposure Time
        # -4       80 ms
        # -5       40 ms
        # -6       20 ms
        camera.set(cv2.CAP_PROP_EXPOSURE,-5)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #width
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024) #height
        return_value, image = camera.read()
        camera.release()
        cv2.destroyAllWindows()

        imageOriginal = image.copy()

        # Convert BGR to gray
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Otsu's thresholding after Gaussian filtering
        blur = cv2.GaussianBlur(gray,(5,5),0)
        #ret3,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        ret3,thresh = cv2.threshold(blur,170,255,cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # OTSU
        if len(contours) != 0:
            # draw in blue the contours that were found
            #cv2.drawContours(image, contours, -1, 255, 3)

            # find the biggest countour (c) by the area
            c = max(contours, key = cv2.contourArea)
            #x,y,w,h = cv2.boundingRect(c)

            # draw the biggest contour (c) in green
            #cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

            rect = cv2.minAreaRect(c)
            rect = cv2.minAreaRect(c)
            # the order of the box points:
            # bottom left, top left, top right, bottom right
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            # get width and height of the detected rectangle
            width = int(rect[1][0])
            height = int(rect[1][1])

            # calculate scan bed area in pixels
            areaPixels = width * height
            print(areaPixels)

            cv2.drawContours(image,[box],0,(0,0,255),2)

            src_pts = box.astype("float32")
            # coordinate of the points in box points after the rectangle has been
            # straightened
            dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")
            # the perspective transformation matrix
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)

            # directly warp the rotated rectangle to get the straightened rectangle
            cropped = cv2.warpPerspective(thresh, M, (width, height))
            croppedNot = cv2.bitwise_not(cropped)

            conversionPixelsToCentimeters = math.sqrt(self.bedAreacm / areaPixels)
            conversionCentimetersToPixels = 1 / conversionPixelsToCentimeters

            conversionSquarePixelsToSquareCentimeters = self.bedAreacm / areaPixels
            conversionSquareCentimetersToSquarePixels = 1 / conversionPixelsToCentimeters

            cropBorderPixels = int(self.bedCropcm * conversionCentimetersToPixels)
            print(conversionPixelsToCentimeters)
            print(height)
            print(cropBorderPixels)
            cropBorder = croppedNot[cropBorderPixels:height - cropBorderPixels * 2,
                           cropBorderPixels:width - cropBorderPixels * 2]
            leafAreaPixels = cv2.countNonZero(cropBorder)

            leafAreaCentimeters = leafAreaPixels * conversionSquarePixelsToSquareCentimeters
            print(leafAreaCentimeters)

        # show the images
        #cv2.imshow("Result", np.hstack([image, output]))
        #cv2.imshow("gray", gray)
        cv2.imwrite("Aimage.png", image)
        cv2.imwrite("Aunmodified.png", imageOriginal)
        cv2.imwrite("Athreshhold.png", thresh)
        cv2.imwrite("Acropped.png", cropped)
        cv2.imwrite("AcropBorder.png", cropBorder)
        #cv2.imshow("adaptive",thresh)
        #cv2.imshow("image", image)

        cv2.waitKey(0)
        im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return im_rgb, leafAreaCentimeters

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

