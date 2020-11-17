import os
import glob
from PIL import Image, ImageOps
import cv2
import numpy as np
from skimage.segmentation import quickshift
from skimage.segmentation import mark_boundaries
import time
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math
color_map = [[0, 0, 255],
    [0, 255, 0],
    [255, 0, 0],
    [255, 0, 255],
    [0, 255, 255],
    [255, 255, 20],
    [0, 102, 204],
    [50, 150, 150],
    [150, 150, 150],
    [0, 0, 0],
]

ignore_color = [255, 255, 255]
other_color = [0, 0, 0]
palette = [255, 0, 0,
           0, 255, 0,
           0, 0, 255,
           255, 0, 255,
           255, 255, 0,
           20, 255, 255,
           204, 102, 0,
           150, 150, 50,
           150, 150, 150]

for i in range(244):
    palette += other_color
palette += ignore_color
def reverse_prediction(np_image):
    grayscale = np.zeros(np_image.shape[:2])
    r, g, b = cv2.split(np_image)
    for i, color in enumerate(color_map):
        condition = np.logical_and(b == color[0], g == color[1])
        condition = np.logical_and(condition, r == color[2])
        grayscale[condition] = i
    return grayscale.astype('uint8')

def get_contours(mask):
    list_contours = []
    # range(10) ???
    for i in range(8):
        mask_i = mask.copy()
        mask_i[mask != i] = 255
        mask_i[mask == i] = 0
        contours, _ = cv2.findContours(mask_i, 1, 1)
        list_contours += contours

    return list_contours

def get_contours_label(img, list_contours):
    contours_label = []
    cleaned_contours = []
    for contour in list_contours:
        white_img = np.zeros(img.shape, dtype=np.uint8)
        cv2.drawContours(white_img, [contour], -1, 1, -1)
        white_img = white_img * (img + 1)

        unique, counts = np.unique(white_img - 1, return_counts=True)

        if 255 in unique:
            illegal_indexs = np.where(unique > 9)
            unique = np.delete(unique, illegal_indexs)
            counts = np.delete(counts, illegal_indexs)

        if len(unique) == 0:
            continue

        max_class_index = np.argmax(counts)
        contours_label.append(unique[max_class_index])
        cleaned_contours.append(contour)

    return cleaned_contours, np.array(contours_label, dtype=np.uint8)

def remove_illegal_contour(list_contours, contours_label):
    illegal_indexs = np.where(contours_label > 7)
    list_contours = np.delete(list_contours, illegal_indexs)
    contours_label = np.delete(contours_label, illegal_indexs)

    return list_contours, contours_label

if __name__ == '__main__':
    image_name = []
    point_center_all = []
    posision = []
    type_class = []
    list_area_object = []
    ####################################
    # input_images = ['/data/1102_export_features/amp49_vis/2018_04_0001_000023_prediction.png']
    # input_images = glob.glob('amp49_vis/*_image.png')
    # for image_path in input_images:
    #     prediction_path = image_path.replace('_image.png', '_prediction.png')
    #
    #     prediction = Image.open(prediction_path)
    #     prediction_np = np.array(prediction)
    #     mask = reverse_prediction(prediction_np)
    #     height, width = mask.shape
    #
    #     unique, counts = np.unique(mask, return_counts=True)
    #     print(unique)
    #     print(counts)
    #     morm_counts = np.round((counts / (height * width) * 100)) / 100
    #
    #     print(image_path)
    #     print(morm_counts)
    ####################################
    for image_path in glob.glob('amp49_vis/*_image.png'):
        prediction_path = image_path.replace('_image.png', '_prediction.png')
        image = Image.open(image_path)
        image_name.append(prediction_path.split('/')[-1])
        # image = ImageOps.expand(image, border=10, fill=128)
        # image_np = np.array(image).astype('uint8')

        prediction = Image.open(prediction_path)
        width, height = prediction.size
        area_image = width * height
        x_left = width/3
        x_center = 2*width/3
        y_top = height/3
        y_center = 2*height/3
        prediction_np = np.array(prediction)
        mask = reverse_prediction(prediction_np)
        mask = Image.fromarray(mask)
        mask = np.array(ImageOps.expand(mask, border=10, fill=9))
        image_crop = np.array(ImageOps.expand(Image.fromarray(prediction_np), border=10, fill=9))
        list_contours = get_contours(mask)
        list_contours, contours_label = get_contours_label(mask, list_contours)
        list_contours, contours_label = remove_illegal_contour(list_contours, contours_label)
        list_point_center = []
        posision_image = []
        class_list = []
        area_object = []
        for index, contour in enumerate(list_contours):
            rect = cv2.minAreaRect(contour) # basically you can feed this rect into your classifier
            (x, y), (w, h), a = rect # a - angle
            if w < 5 or h < 5:
                continue
            box = cv2.boxPoints(rect)
            print(box)
            box = np.int0(box)
            center_x = (box[0][0]+ box[2][0])/2
            center_y = (box[0][1]+ box[2][1])/2
            if center_x <= x_left:
                type_pos = 'left'
            elif center_x > x_left and center_x <= x_center:
                type_pos = 'center'
            else:
                type_pos = 'right'
            if center_y <= y_top:
                type_pos = type_pos + ' - top'
            elif center_y > y_top and center_y <= y_center:
                type_pos = type_pos + ' - center'
            else:
                type_pos = type_pos + ' - bottom'

            posision_image.append(type_pos)
            Point_center = [center_x, center_y]
            list_point_center.append(Point_center)
            cv2.drawContours(mask, [box], 0, int(contours_label[index]), 1)
            class_list.append(int(contours_label[index]))
            # calc area object

            area_object.append((box.height * box.width)/area_image)
            print(area_object)
            break
        break
            # end area object
        list_area_object.append(area_object)
        type_class.append(class_list)
        posision.append((posision_image))
        point_center_all.append(list_point_center)
        img_mask = Image.fromarray(mask)
        img_mask = ImageOps.crop(img_mask, border=10)
        img_mask.putpalette(palette)
        # img_mask.save('{}_seq_tmp.png'.format(prediction_path.split('_prediction.png')[0]))
    # df = pd.DataFrame()
    # df['Image_name'] = image_name
    # df['Type_class'] = type_class
    # df['Point_center'] = point_center_all
    # df['Posision'] = posision
    # df['Area_per_object'] = list_area_object
    # df.to_csv('locate_area1.csv', index=False)

