from .imgDeal.get_drug import imgDeal
from .ocr.esaytest import ocr
import cv2
import os


def run():
    dirname = os.path.dirname(__file__)
    filePath = os.path.join(dirname, 'img')

    cap = cv2.VideoCapture(2)        #開啟攝像頭

    if(cap):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        cv2.imwrite(filePath+"/test.png", frame)   #儲存路徑
        

    cap.release()
    
    img = cv2.imread(filePath+"/test.png" )
    result = imgDeal(img)
    cv2.imwrite(filePath+"/result.png", result)
    result = result[78:123]
    cv2.imwrite(filePath+"/result1.png", result)
    paper = []
    paper = ocr(result)
    if len(paper) > 1:
        run()
    result = {}
    result[0] = {"p_medicineName" :[{"name":paper[0],"predict":1}],"p_medicineNum":7}
    return result







# paper = run()
# print(paper)
#print(cleanData(paper))
