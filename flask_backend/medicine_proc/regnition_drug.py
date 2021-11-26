import numpy as np
import os
import cv2
import pprint
import time


dirname = os.path.dirname(__file__)
filePath = os.path.join(dirname, 'returnText')
#影像辨識功能
def detect(image):
    LABELS = open(filePath+"/drug.names").read().strip().split("\n")
    net = cv2.dnn.readNet(filePath+'/yolov4-drug.cfg', filePath+'/yolov4-drug_last_v2.weights')
    layer = net.getUnconnectedOutLayersNames()

    (H, W) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(layer)

    boxes = []
    confidences = []
    classIDs = []
    result = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > 0.3:#可以更改信心指數

                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
    if len(idxs) > 0:
        for i in idxs.flatten():
            result.append(LABELS[classIDs[i]])

    dict = {}
    output_result = {}
    for key in result:
        dict[key] = dict.get(key, 0) + 1

    for i in range(len(dict)):
        output_result[i] = {'drug_name':list(dict.keys())[i],'drug_quality': list(dict.values())[i]}

    return output_result

#=================================================================

#攝影機讀取區塊
def excute(cap):
    print('cap is opened')
    if cap:
        ret, frame = cap.read()

        print(frame)

        return detect(frame)



# imgPath = os.path.join(dirname, 'returnText/img')
# # 指定要查詢的路徑及圖片
# def excute():
#     time.sleep(5)
#     pic = 'combine000.jpg'
#     img = cv2.imread(imgPath+'/'+pic)
#     #pprint.pprint(detect(img))
#     return detect(img)