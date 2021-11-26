import cv2
import numpy as np

def getDrug(img):
    scale_percent = 40 
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img1 = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    # contour detect
    img2 = img.copy()
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 100, 300)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  
    cv2.drawContours(img2, contours, -1, (0, 255, 0), 7)

    contours_max = 0
    contours_index = 0
    for i in range(0, len(contours)):

        if cv2.contourArea(contours[i]) > contours_max:
            contours_max = cv2.contourArea(contours[i])
            contours_index = i

    # green detect
    img1 = img.copy()
    def green_detect(img1):
        hsv_img = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 15, 15]) 
        upper_green = np.array([80, 255, 255])
        green_mask = cv2.inRange(hsv_img, lower_green, upper_green)
        contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        return contours

    first = green_detect(img1)
    for i in range(0, len(first)):

        if cv2.contourArea(first[i]) > 60:
            cv2.drawContours(img1, first[i], -1, (0, 255, 0), 5)

    second = green_detect(img1)
    for i in range(0, len(second)):

        if cv2.contourArea(second[i]) > 1000:
            cv2.drawContours(img1, second[i], -1, (0, 255, 0), 5)

    third = green_detect(img1)
    for i in range(0, len(third)):

        if cv2.contourArea(third[i]) > 200:
            cv2.drawContours(img1, third[i], -1, (0, 255, 0), 1)

    max = 0
    index = 0
    for i in range(0, len(third)):

        if cv2.contourArea(third[i]) > max:
            max = cv2.contourArea(third[i])
            index = i

    if cv2.contourArea(third[index]) < cv2.contourArea(contours[contours_index]):
        result = contours[contours_index]
    else:
        result = third[index]
    (x, y, w, h) = cv2.boundingRect(result)
    # cv2.rectangle(img,(x,y),(x+w, y+h),(255,0,0),2, cv2.LINE_AA)

    img_result = img[y:y+h,x:x+w]
    img_final = img_result.copy()

    def getMed():
        img_med = img_final[220:375]
        # 
        return img_med

    def geteffect():
        img_effect = img_final[205:280]
        cv2.imshow("img_effect", img_effect)


    def getWord():
        hsv_img = cv2.cvtColor(img_final, cv2.COLOR_BGR2HSV)
        lower_green = np.array([50, 15, 15]) 
        upper_green = np.array([70, 255, 255])
        green_mask = cv2.inRange(hsv_img, lower_green, upper_green)
        five, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for i in range(0, len(five)):

            if cv2.contourArea(five[i]) > 150 :

                (x, y, w, h) = cv2.boundingRect(five[i])
                cv2.rectangle(img_final,(x,y),(x+w, y+h),(255,0,0),2, cv2.LINE_AA)

    scale_percent = 60 
    width = int(img_final.shape[1] * scale_percent / 100)
    height = int(img_final.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img_final, dim, interpolation = cv2.INTER_AREA)
    return getMed()

































































