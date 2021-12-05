from imgDeal import get_drug
from ocr import esaytest
import cv2


def run():
    result = ''
    #for i in range():
    img = cv2.imread('./img/16.jpg' )
    result = get_drug.imgDeal(img)

    cv2.imwrite('./result/img16.jpg', result)
    img = cv2.imread('./result/img16.jpg')

    paper = esaytest.ocr(img)


    print("-------------------------------------------");return paper





paper = run()
print(paper)
#print(cleanData(paper))
