import easyocr
import cv2

def ocr(img):

    #img = cv2.imread('D:/getdrug/result/img19.jpg')

    #img0 = img[65:150,10:700]
    #img1 = img[50:150,750:980]

    reader= easyocr.Reader(['ch_tra','en'])

    res=reader.readtext(img)

    paper = []
    
    for i in res:
        # print(i)
        word = i[1]
        if i[2] > 0.5:
            paper.append(word)
        

    return paper