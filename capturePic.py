import cv2
import numpy as np

class CapturePic:
    def capturePic(cdf):
        camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        #print(camera.get(cv2.CAP_PROP_FPS))
        #camera.set(cv2.CAP_PROP_FPS, 1)
        print(camera.get(cv2.CAP_PROP_FPS))
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #width
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024) #height
        return_value, image = camera.read()
        camera.release()
        cv2.destroyAllWindows()


        cv2.imshow("Image", image)
        cv2.waitKey(0)


        lower = [120, 120, 120]
        upper = [255, 255, 255]

        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

#        cv2.imshow("Image", output)
#        cv2.waitKey(0)

        ret,thresh = cv2.threshold(mask, 40, 255, 0)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        # Image directory 
        #directory = r'C:\Users\Easter\leafArea'
        path = os.getcwd()
        path = path + "\\" + projectName
  

      
        # Change the current directory  
        # to specified directory  
        #os.chdir(directory) 

          
        # Filename 
        filename = 'savedImage2.png'
          
        # Using cv2.imwrite() method 
        # Saving the image 
        cv2.imwrite(filename, image) 

        return output


        if len(contours) != 0:
            # draw in blue the contours that were found
            cv2.drawContours(output, contours, -1, 255, 3)

            # find the biggest countour (c) by the area
            c = max(contours, key = cv2.contourArea)
            x,y,w,h = cv2.boundingRect(c)

            # draw the biggest contour (c) in green
            cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

        # show the images
#        cv2.imshow("Result", np.hstack([image, output]))

#        cv2.waitKey(0)


    # Use this function to find your camera's max resolution
    # https://en.wikipedia.org/wiki/List_of_common_resolutions
    def set_res(cap, x,y):
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
    #image = cp.capturePic()

    cp.set_res(640,	480)   # VGA
    cp.set_res(800,	600)   # SVGA
    cp.set_res(1280, 1024) # SXGA

