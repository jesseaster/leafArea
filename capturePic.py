import cv2
import numpy as np
import os
import math
import glob
from matplotlib import pyplot as plt


class CapturePic:
    def __init__(self):
        self.bedWidthcm = 60  # 60 cm
        self.bedHeightcm = 60  # 60 cm
        self.bedAreacm = 3600  # 3600 sq cm

        self.imageWidth = 1280
        self.imageHeight = 1024

        self.bedAreaPixels = 917278  # sq pixels of the bed

        self.conversionSquarePixelsToSquareCentimeters = self.bedAreacm / self.bedAreaPixels

        # CAP_PROP_EXPOSURE Exposure Time
        # -4       80 ms
        # -5       40 ms
        # -6       20 ms
        self.exposureTime = -6

    def getCalibratedImage(self):
        img = self.capturePic()
        rotated_img = self.rotatePic(img)
        crop_img = self.cropPic(rotated_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        return img, crop_img

    def getLeafImageAndArea(self, calibratedImage, img=None):
        if np.all(img) is None:
            img = self.capturePic()
        rotated_img = self.rotatePic(img)
        crop_img = self.cropPic(rotated_img)
        subtracted_img = self.subtractPics(calibratedImage, crop_img)
        green = self.filterGreen(crop_img, subtracted_img)
        leafAreaCentimeters = self.calculateSquareCentimeters(green)
        crop_img_rgb = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        original_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return crop_img_rgb, original_rgb, green, leafAreaCentimeters

    def capturePic(self):
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        camera.set(cv2.CAP_PROP_EXPOSURE, self.exposureTime)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.imageWidth)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.imageHeight)
        return_value, image = camera.read()
        camera.release()
        cv2.destroyAllWindows()
        return image

    def rotatePic(self, image):
        degreesToRotate = 1
        rows, columns, colors = image.shape
        M = cv2.getRotationMatrix2D((columns/2,rows/2),degreesToRotate,1)
        dst = cv2.warpAffine(image,M,(columns,rows))
        return dst

    def cropPic(self, image):
        y = 30
        h = 950
        x = 138
        w = 945
        crop_img = image[y:y+h, x:x+w]
        return crop_img

    def subtractPics(self, calibrated, img):
        cv2.destroyAllWindows()
        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        fgmask = fgbg.apply(calibrated)
        fgmask = fgbg.apply(img)
        return fgmask

    def filterGreen(self, img, mask):
        res = cv2.bitwise_and(img,img, mask = mask)

        ## convert to hsv
        hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)

        ## mask of green (36,25,25) ~ (86, 255,255)
        # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
        mask = cv2.inRange(hsv, (25, 25, 25), (86, 255,255))

        ## slice the green
        imask = mask>0
        green = np.zeros_like(res, np.uint8)
        green[imask] = res[imask]
        ret,thresh1 = cv2.threshold(green,0,255,cv2.THRESH_BINARY)
        green = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)
        return green

    def calculateSquareCentimeters(self, img):
        leafAreaPixels = cv2.countNonZero(img)
        leafAreaCentimeters = leafAreaPixels * self.conversionSquarePixelsToSquareCentimeters
        print(leafAreaCentimeters)
        return leafAreaCentimeters

    def loadPics(self):
        filename = 'C:/Users/Easter/Downloads/8-3-20-20200804T194018Z-001/8-3-20/MsCcHSFeed/08-03-2020.15.783CatID019LeafID1172Original.png'
        calibrated_img = cv2.imread(filename,cv2.IMREAD_COLOR)
        calibrated_img = self.rotatePic(calibrated_img)
        calibrated_img = self.cropPic(calibrated_img)
        cropped_images = glob.glob('C:/Users/Easter/Downloads/8-3-20-20200804T194018Z-001/8-3-20/MsCcHSFeed/*Cropped.png')
        original_images = glob.glob('C:/Users/Easter/Downloads/8-3-20-20200804T194018Z-001/8-3-20/MsCcHSFeed/*Original.png')
        for i in range(len(original_images)):
            print(original_images[i])
            print(i)
            img = cv2.imread(original_images[i],cv2.IMREAD_COLOR)
            old_cropped = cv2.imread(cropped_images[i],cv2.IMREAD_COLOR)
            crop_img_rgb, original_rgb, green, leafAreaCentimeters = self.getLeafImageAndArea(calibrated_img, img)
            pics = [crop_img_rgb, green, old_cropped]
            titles = ['Cropped', 'Green', 'Old']
            self.displayPics(pics, titles)

    def loadPics2(self):
        filename = 'C:/Users/Easter/Downloads/8-3-20-20200804T194018Z-001/8-3-20/MsCcHSFeed/08-03-2020.15.783CatID019LeafID1172Original.png'
        calibrated_img = cv2.imread(filename,cv2.IMREAD_COLOR)
        calibrated_img = self.rotatePic(calibrated_img)
        calibrated_img = self.cropPic(calibrated_img)
        cropped_images = glob.glob('C:/Users/Easter/Downloads/8-3-20-20200804T194018Z-001/8-3-20/MsCcHSFeed/*Cropped.png')
        original_images = glob.glob('C:/Users/Easter/Downloads/8-3-20-20200804T194018Z-001/8-3-20/MsCcHSFeed/*Original.png')
        for i in range(0,len(original_images),5):
            print(original_images[i])
            print(i)
            img0 = cv2.imread(original_images[i+0],cv2.IMREAD_COLOR)
            img1 = cv2.imread(original_images[i+1],cv2.IMREAD_COLOR)
            img2 = cv2.imread(original_images[i+2],cv2.IMREAD_COLOR)
            img3 = cv2.imread(original_images[i+3],cv2.IMREAD_COLOR)
            img4 = cv2.imread(original_images[i+4],cv2.IMREAD_COLOR)

            crop_img_rgb0, original_rgb, green0, leafAreaCentimeters0 = self.getLeafImageAndArea(calibrated_img, img0)
            crop_img_rgb1, original_rgb, green1, leafAreaCentimeters1 = self.getLeafImageAndArea(calibrated_img, img1)
            crop_img_rgb2, original_rgb, green2, leafAreaCentimeters2 = self.getLeafImageAndArea(calibrated_img, img2)
            crop_img_rgb3, original_rgb, green3, leafAreaCentimeters3 = self.getLeafImageAndArea(calibrated_img, img3)
            crop_img_rgb4, original_rgb, green4, leafAreaCentimeters4 = self.getLeafImageAndArea(calibrated_img, img4)

            leafAreaCentimeters0 = round(leafAreaCentimeters0, 2)
            leafAreaCentimeters1 = round(leafAreaCentimeters1, 2)
            leafAreaCentimeters2 = round(leafAreaCentimeters2, 2)
            leafAreaCentimeters3 = round(leafAreaCentimeters3, 2)
            leafAreaCentimeters4 = round(leafAreaCentimeters4, 2)

            cimg0 = cv2.imread(cropped_images[i+0],cv2.IMREAD_COLOR)
            cimg1 = cv2.imread(cropped_images[i+1],cv2.IMREAD_COLOR)
            cimg2 = cv2.imread(cropped_images[i+2],cv2.IMREAD_COLOR)
            cimg3 = cv2.imread(cropped_images[i+3],cv2.IMREAD_COLOR)
            cimg4 = cv2.imread(cropped_images[i+4],cv2.IMREAD_COLOR)

            cimg0 = cv2.cvtColor(cimg0, cv2.COLOR_BGR2GRAY)
            cimg1 = cv2.cvtColor(cimg1, cv2.COLOR_BGR2GRAY)
            cimg2 = cv2.cvtColor(cimg2, cv2.COLOR_BGR2GRAY)
            cimg3 = cv2.cvtColor(cimg3, cv2.COLOR_BGR2GRAY)
            cimg4 = cv2.cvtColor(cimg4, cv2.COLOR_BGR2GRAY)

            leafAreaCentimetersOld0 = round(self.calculateSquareCentimeters(cimg0),2)
            leafAreaCentimetersOld1 = round(self.calculateSquareCentimeters(cimg1),2)
            leafAreaCentimetersOld2 = round(self.calculateSquareCentimeters(cimg2),2)
            leafAreaCentimetersOld3 = round(self.calculateSquareCentimeters(cimg3),2)
            leafAreaCentimetersOld4 = round(self.calculateSquareCentimeters(cimg4),2)

            pics = [crop_img_rgb0, crop_img_rgb1, crop_img_rgb2, crop_img_rgb3, crop_img_rgb4]
            titles = [str(i), str(i+1), str(i+2), str(i+3), str(i+4)]
            pics2 = [green0, green1, green2, green3, green4]
            titles2 = [leafAreaCentimeters0, leafAreaCentimeters1, leafAreaCentimeters2, leafAreaCentimeters3, leafAreaCentimeters4]
            pics3 = [cimg0, cimg1, cimg2, cimg3, cimg4]
            titles3 = [leafAreaCentimetersOld0, leafAreaCentimetersOld1, leafAreaCentimetersOld2, leafAreaCentimetersOld3, leafAreaCentimetersOld4]

            self.displayPics2(pics, titles, pics2, titles2, pics3, titles3)

    def displayPics(self, pics, titles):
        for i in range(len(pics)):
            plt.subplot(1,len(pics),i + 1),plt.imshow(pics[i],'gray')
            plt.title(titles[i]), plt.xticks([]), plt.yticks([])
        plt.show()

    def displayPics2(self, pics, titles, pics2, titles2, pics3, titles3):
        for i in range(len(pics)):
            plt.subplot(3,len(pics),i + 1),plt.imshow(pics[i],'gray')
            plt.title(titles[i]), plt.xticks([]), plt.yticks([])
            plt.subplot(3,len(pics2),i + 1 + len(pics2)),plt.imshow(pics2[i],'gray')
            plt.title(titles2[i]), plt.xticks([]), plt.yticks([])
            plt.subplot(3,len(pics3),i + 1 + len(pics2) + len(pics3)),plt.imshow(pics3[i],'gray')
            plt.title(titles3[i]), plt.xticks([]), plt.yticks([])
        plt.show()

    # Use this function to find your camera's max resolution
    # https://en.wikipedia.org/wiki/List_of_common_resolutions
    def set_res(self, x, y):
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
        print(
            str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) + " " +
            str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        return_value, image = cap.read()
        cap.release()
        cv2.destroyAllWindows()
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), str(
            cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


if __name__ == '__main__':
    cp = CapturePic()
    cp.loadPics2()
    #image = cp.capturePic()

    #cp.set_res(640,	480)   # VGA
    #cp.set_res(800,	600)   # SVGA
    #cp.set_res(1280, 1024) # SXGA
