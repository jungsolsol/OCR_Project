from imgaug import augmentables
import imgaug.augmenters as iaa
import cv2
import glob
import json
import random
import matplotlib.pyplot as plt
from numpy.lib.function_base import interp
from numpy.lib.type_check import imag
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import os
from tqdm import tqdm

class Augmentation:
    def __init__(self,img_path,json_path):
        self.img_path = img_path
        self.json_path = json_path
        
        # 이미지 크기 및 json에서 label 값과 bounding box 좌표값을 따로 저장할 공간입니다.
        self.images = None
        self.label_all = None
        self.bounding_box = None

    def load_dataset(self):
        try:
            images_path = glob.glob(self.img_path)
            bounding_box_path = glob.glob(self.json_path)
        except:
            print('glob library 의 input 형식을 받아야합니다.')
            return None

        images = []
        for img_path in images_path:
            img = cv2.imread(img_path)
            images.append(img)

        bounding_box = []
        label_all = []
        for path in bounding_box_path:
            with open(path, encoding='utf-8') as json_file:
                json_data = json.load(json_file)
            
            temp = []
            temp_txt = []
            for i in json_data['shapes']:
                points = i['points']
                label = i['label']
                
                temp.append(BoundingBox(x1=points[0][0], y1= points[0][1], x2 = points[1][0], y2 = points[1][1]))
                temp_txt.append(label)

            label_all.append(temp_txt)
            bounding_box.append(temp)
        
        self.images = images
        self.label_all = label_all
        self.bounding_box = bounding_box
    

    def resizes(self):
        # 2. images resize
        resized_images = []
        resized_bounding_box = []
        for i in tqdm(range(len(self.bounding_box))):
        # 박스 좌표값 담아두기
            bbs = BoundingBoxesOnImage([
            x for x in self.bounding_box[i]], shape = self.images[i].shape
            )
            # augmentation resize 정리
            augmentation_resize = iaa.Sequential([
                iaa.Resize({"height":1500,"width":1000},interpolation="cubic")
            ])
            image_aug, bbs_aug = augmentation_resize(image=self.images[i], bounding_boxes=bbs)

            # resize 된 이미지 다시 담아주기
            resized_images.append(image_aug)

            # 박스 좌표값 다시 담기
            temp = []
            for i in bbs_aug:
                temp.append(BoundingBox(x1=i[0][0], y1= i[0][1], x2 = i[1][0], y2 = i[1][1]))
            resized_bounding_box.append(temp)

        self.images = resized_images
        self.bounding_box = resized_bounding_box

    # 3. image augmentation
    def augmentation(self):

        for cnt in tqdm(range(100000)):
            for i in range(len(self.bounding_box)):
                # 박스 좌표값 담아두기
                bbs = BoundingBoxesOnImage([
                    x for x in self.bounding_box[i]], shape = self.images[i].shape
                )
                # augmentation resize 정리
                augmentation_resize = iaa.Sequential([
                    iaa.Affine(translate_percent={"x":(-0.5,0.5),"y":(-0.5,0.5)},rotate=(-2,2),scale=(0.5,2)),
                    iaa.Multiply((0.8, 1.3)),
                    iaa.LinearContrast((0.8,1.2)),
                    iaa.GaussianBlur((0.0,3.0)),
                    # iaa.Sometimes(0.5,
                    #     iaa.GaussianBlur((0.0,3.0))
                    # )
                ])

                image_aug, bbs_aug = augmentation_resize(image=self.images[i], bounding_boxes=bbs)

                json_data = {}
                json_data['type'] = 'text'  
                json_data['shapes'] = []
                for j in range(len(self.label_all[i])):
                    if (bbs_aug[j][0][0] > 0) and (bbs_aug[j][0][1] > 0) and (bbs_aug[j][1][0] > 0) and (bbs_aug[j][1][1] > 0):
                        json_data['shapes'].append({'label': "{}".format(self.label_all[i][j]), 
                                                    'points': [str(bbs_aug[j][0][0]),
                                                                    str(bbs_aug[j][0][1]),
                                                                    str(bbs_aug[j][1][0]),
                                                                    str(bbs_aug[j][1][1])]
                                                                    })
                    

            os.makedirs('../data/aug_img', exist_ok=True)
            os.makedirs('../data/aug_json', exist_ok=True)

            cv2.imwrite('.././data/aug_img/{}.jpg'.format(cnt), image_aug)
            with open(".././data/aug_json/{}.json".format(cnt), "w") as f: 
                json.dump(json_data, f)



    
if __name__ == '__main__': 
    temp = Augmentation('.././data/image/*.jpg','.././data/json/*.json')
    print('이미지와 json 파일을 불러오는 중입니다.')
    temp.load_dataset()
    print('이미지, json 불러오기 성공')
    print('*' * 30)
    print('이미지 크기 조절 중입니다. json 에 있는 좌표값도 함께 수정 중입니다.')
    temp.resizes()
    print('이미지, json 크기 조절 성공')
    print('*' * 30)
    print('data augmentation 중 입니다. json 에 있는 좌표값도 함께 수정 중입니다.')
    temp.augmentation()
    print('data augmentation 성공')
    print('*' * 30)
    del temp