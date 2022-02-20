import cv2
import matplotlib.pyplot as plt
import json
import random
import glob

def check_image_json():
    for _ in range(5):
        temp = random.randint(0,40)
        with open('.././data/aug_json/{}.json'.format(temp),encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        label = []
        points = []

        for i in json_data['shapes']:
            label.append(i['label'])
            points.append(i['points'])

        # 이미지 직접 불러오기
        img = cv2.imread('.././data/aug_img/{}.jpg'.format(temp))

        for i in range(len(label)):
            color_1 = random.randrange(100,255)
            color_2 = random.randrange(100,255)
            color_3 = random.randrange(100,255)
            
            x_min, y_min, x_max, y_max = points[i][0], points[i][1], points[i][2], points[i][3]
            x_min , y_min, x_max, y_max = int(float(x_min)), int(float(y_min)), int(float(x_max)), int(float(y_max))
            
            img = cv2.rectangle(img,(x_min, y_min),(x_max, y_max),(color_1,color_2,color_3),3)
        
        cv2.imshow("image",img)
        cv2.waitKey()

if __name__ == '__main__': 
    check_image_json()