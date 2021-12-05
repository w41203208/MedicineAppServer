import pytesseract
import cv2

def ocr(img):
    pytesseract.pytesseract.tesseract_cmd = r"D:/Tesseract-OCR/tesseract.exe"
    #要下載


    #img0 = img[65:150,10:700]
    #img1 = img[50:150,750:980]

    #gray=cv2.cvtColor(img ,cv2.COLOR_BGR2GRAY)
    #灰階
    #adaptive_threshold=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 85, 13)
    #二接化

    cv2.imshow('detect Image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(pytesseract.image_to_string(img, lang='chi_tra'))
