import os
import glob
from PIL import Image, ImageOps
import cv2
import numpy as np
from skimage.segmentation import quickshift
from skimage.segmentation import mark_boundaries
import time

color_map = [[0, 0, 255],
    [0, 255, 0],
    [255, 0, 0],
    [255, 0, 255],
    [0, 255, 255],
    [225, 255, 20],
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

def get_contours(img):
    list_contours = []
    list_labels = []
    for i in np.unique(img):
        mask_i = img.copy()
        mask_i[img != i] = 255
        mask_i[img == i] = 0

        cv2.imwrite('sample_{}.png'.format(i), mask_i)

        contours, _ = cv2.findContours(mask_i, 1, 1)

        white_img = np.zeros(mask_i.shape, dtype=np.uint8) + 9
        for contour in contours:
            cv2.drawContours(white_img, [contour], 0, int(i), 2)
        white_img = Image.fromarray(white_img)
        white_img.putpalette(palette)
        white_img.save('sample_ct_{}.png'.format(i))

        list_contours += contours
        list_labels += ([i] * len(contours))

    return list_contours, list_labels

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
    input_images = ['/data/1102_export_features/amp49_vis/2018_05_0002_000117_prediction.png']
    # input_images = glob.glob('amp49_vis/*_image.png')
    for image_path in input_images:
        prediction_path = image_path.replace('_image.png', '_prediction.png')

        image = Image.open(image_path)
        image = ImageOps.expand(image, border=10, fill=128)
        image_np = np.array(image).astype('uint8')

        prediction = Image.open(prediction_path) 
        width, height = prediction.size
        
        prediction_np = np.array(prediction) 
        mask = reverse_prediction(prediction_np)
        mask = Image.fromarray(mask)

        padded_mask = ImageOps.expand(mask, border=10, fill=9)
        padded_mask.putpalette(palette)
        padded_mask.save('padded_mask.png')
        mask = np.array(padded_mask)

        list_contours, list_labels = get_contours(mask)
        white_img = np.zeros(mask.shape, dtype=np.uint8) + 9
        for index, contour in enumerate(list_contours):
            if int(list_labels[index]) < 8:
                cv2.drawContours(white_img, [contour], 0, int(list_labels[index]), 2)

        white_img = Image.fromarray(white_img)
        white_img.putpalette(palette)
        white_img.save('sample_.png'.format(i))

        white_img = np.zeros(mask.shape, dtype=np.uint8) + 9
        for index, contour in enumerate(list_contours):
            if int(list_labels[index]) > 7:
                continue
            rect = cv2.minAreaRect(contour) # basically you can feed this rect into your classifier
            (x, y), (w, h), a = rect # a - angle
            
            if w < 5 or h < 5:
                continue

            box = cv2.boxPoints(rect)
            box = np.int0(box) #turn into ints
            if len(box[box == 0]) == 4:
                continue
            cv2.drawContours(white_img, [box], 0, int(list_labels[index]), 2)
      
        white_img = Image.fromarray(white_img)
        white_img.putpalette(palette)
        white_img.save('sample_final.png'.format(i))



        
