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

        # cv2.imwrite('sample_{}.png'.format(i), mask_i)

        contours, _ = cv2.findContours(mask_i, 1, 1)

        # white_img = np.zeros(mask_i.shape, dtype=np.uint8) + 9
        # for contour in contours:
        #     cv2.drawContours(white_img, [contour], 0, int(i), 2)
        # white_img = Image.fromarray(white_img)
        # white_img.putpalette(palette)
        # white_img.save('sample_ct_{}.png'.format(i))

        list_contours += contours
        list_labels += ([i] * len(contours))

    return list_contours, list_labels

if __name__ == '__main__':
    # input_images = ['/data/1102_export_features/amp49_vis/2018_05_0002_000117_prediction.png']
    input_images = glob.glob('amp49_vis/*_image.png')
    for image_path in input_images:
        print(image_path)
        prediction_path = image_path.replace('_image.png', '_prediction.png')

        image = Image.open(image_path)
        image = ImageOps.expand(image, border=10, fill=128)
        image_np = np.array(image).astype('uint8')

        prediction = Image.open(prediction_path) 
        width, height = prediction.size
        
        prediction_np = np.array(prediction) 
        mask = reverse_prediction(prediction_np)
        mask = Image.fromarray(mask)
        mask = np.array(ImageOps.expand(mask, border=10, fill=9))
        
        list_contours, list_labels = get_contours(mask)

        # print(len(contours_label), len(list_contours))

        white_img = np.zeros(mask.shape, dtype=np.uint8) + 9
        boxes = []
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

            center_point_x = int((box[0][0] + box[2][0]) / 2)
            center_point_y = int((box[0][1] + box[2][1]) / 2)
            center_point = (center_point_x, center_point_y)
            boxes.append((center_point_x, center_point_y, int(list_labels[index])))
            cv2.circle(mask, center_point, radius=0, color=255, thickness=3)
            # cv2.drawContours(white_img, [box], 0, int(list_labels[index]), 1)
      
        height, width = mask.shape
        mask = mask[10:height - 10, 10:width - 10]

        new_height, new_width = mask.shape
        for box in boxes:
            x, y, label = box

            if x <= new_width / 3:
                x_pos = 'left'
            elif x <= new_width * 2 / 3:
                x_pos = 'center'
            else:
                x_pos = 'right'

            if y <= new_height / 3:
                y_pos = 'top'
            elif y <= new_height * 2 / 3:
                y_pos = 'middle'
            else:
                y_pos = 'bottom'

            print(mask, x_pos, y_pos)

        cv2.rectangle(mask, (0, int(new_height / 3)), (new_width, int(new_height / 3)), 255, thickness=1)
        cv2.rectangle(mask, (0, int(new_height * 2 / 3)), (new_width, int(new_height * 2 / 3)), 255, thickness=1)
        cv2.rectangle(mask, (int(new_width / 3), 0), (int(new_width / 3), new_height), 255, thickness=1)
        cv2.rectangle(mask, (int(new_width * 2 / 3), 0), (int(new_width * 2 / 3), new_height), 255, thickness=1)

        img_mask = Image.fromarray(mask)
        img_mask.putpalette(palette)
        img_mask.save('{}_seq.png'.format(prediction_path.split('_prediction.png')[0]))
        #Image.fromarray(rs).save('MP-Review4-unmerge_273648208311_seg.png')



        
