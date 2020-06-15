import cv2
import numpy as np
img = cv2.imread('grid.jpg')
height = img.shape[0]
width = img.shape[1]
print("width " + str(width))
cv2.imshow("Image", img)
cv2.waitKey(0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(img,50,150,apertureSize = 3)

cv2.imwrite('edges-50-150.jpg',edges)
(thresh, blackAndWhiteImage) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
blackAndWhiteImage = cv2.bitwise_not(blackAndWhiteImage)
minLineLength=370
minLineLengthTest=[0]
blur = cv2.GaussianBlur(gray, (5,5), 0)
threshTest = [3,5,7,9,11]
rhoTest = [.01,.2,.4,.6,.8,1,1.2,4]
maxLineGapTest = [10]
for m in maxLineGapTest:
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    lines = cv2.HoughLinesP(image=blackAndWhiteImage,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=minLineLength,maxLineGap=m)

    a,b,c = lines.shape
    for i in range(a):
        cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 1)
        cv2.imwrite('houghlines5.jpg',img)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    print(i)
numH=-1
numV=-1
hoizontalLineSpacing = 0
verticalLineSpacing = 0

for line in lines:
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[0][2]
    y2 = line[0][3]
    xdiff= x2 - x1
    ydiff = y2 -y1
    slope = ydiff/xdiff
    
    if slope == float("inf") or slope == -1*float("inf"):
        xSlope = xdiff/ydiff
        b = x1 - xSlope*y1
        print('x = y * ' + str(xSlope) + ' + ' + str(b))
        numV = numV + 1
        verticalLineSpacing = verticalLineSpacing + b
        
    else:
        c = y1 - slope*x1
        print('y = x * ' + str(slope) + ' + ' + str(c))
        numH = numH + 1
        hoizontalLineSpacing = hoizontalLineSpacing + c

hoizontalLineSpacing = hoizontalLineSpacing/((numH * (numH + 1) ) /2)
verticalLineSpacing = verticalLineSpacing/((numV * (numV + 1) ) /2)

print("Horizontal Lines = " + str(numH))
print("Vertical Lines = " + str(numV))

print("Horizontal Line Spacing = " + str(hoizontalLineSpacing))
print("Vertical Line Spacing = " + str(verticalLineSpacing))

print("Horizontal Error Percent = " + str(((hoizontalLineSpacing -19.1)/19.1)*100))
print("Vertical Error Percent = " + str(((verticalLineSpacing -19.1)/19.1)*100))

