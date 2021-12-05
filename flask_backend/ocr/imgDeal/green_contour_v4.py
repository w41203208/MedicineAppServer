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

    rect = cv2.minAreaRect(result) 



    width = int(rect[1][0])
    height = int(rect[1][1])
    angle = rect[2]
    print(angle)

    if width < height:  #計算角度，爲後續做準備
        angle = angle - 90
    print(angle)

    src_pts = cv2.boxPoints(rect)


    dst_pts = np.array([[0, height],
                        [0, 0],
                        [width, 0],
                        [width, height]], dtype="float32")
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(img, M, (width, height))

    if angle<=-90:  #對-90度以上圖片的豎直結果轉正
        warped = cv2.transpose(warped)
        warped = cv2.flip(warped, 0)  # 逆時針轉90度，如果想順時針，則0改爲1
        # warped=warped.transpose

    height = warped.shape[0]
    # 定義圖片的寬度
    width = warped.shape[1]
    # 定義圖片的中心
    center = (int(height/2), int(width/2))

    # 指定旋轉角度
    angle = 270

    # 指定縮放比例
    scale = 1.0


    # 旋轉
    trans = cv2.getRotationMatrix2D(center, angle, scale)
    image2 = cv2.warpAffine(warped, trans, (width, height))

    # 儲存圖片
    cv2.imwrite('image2.jpg', image2)

    return image2
































































