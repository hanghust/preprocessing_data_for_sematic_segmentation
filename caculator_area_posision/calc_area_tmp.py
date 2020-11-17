import os
import glob
from PIL import Image
import cv2
import numpy as np
import glob
import pandas as pd
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

def get_all_link_image_pred(path_folder, format):
    path_file = glob.glob(path_folder + '/*_prediction.' + format)
    return path_file
def reverse_prediction(np_image):
    grayscale = np.zeros(np_image.shape[:2])
    r, g, b = cv2.split(np_image)
    for i, color in enumerate(color_map):
        condition = np.logical_and(b == color[0], g == color[1])
        condition = np.logical_and(condition, r == color[2])
        grayscale[condition] = i
    return grayscale.astype('uint8')

# # input_images = glob.glob('amp49_vis/*_image.png')
# input_images = ['/home/hangnt/hangnt/1102_export_features/amp49_vis/2018_04_0001_000023_prediction.png']
# for image_path in input_images:
#     print(image_path)
#     prediction_path = image_path.replace('_image.png', '_prediction.png')
#     print(prediction_path)
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
if __name__ == "__main__":
    path_folder = '/home/hangnt/hangnt/1102_export_features/amp49_vis/'
    format = 'png'
    path_file = get_all_link_image_pred(path_folder, format)
    type_class = []
    percent_class = []
    image_name = []
    for prediction_path in path_file:
        image_name.append((prediction_path.split('/'))[-1])
        prediction = Image.open(prediction_path)
        prediction_np = np.array(prediction)
        mask = reverse_prediction(prediction_np)
        height, width = mask.shape
        unique, counts = np.unique(mask, return_counts=True)
        morm_counts = np.round((counts / (height * width) * 100)) / 100
        type_class.append(unique)
        percent_class.append(morm_counts)
        # unique list label of image
        # counts number of pixel for each class of image
        # morm_counts % area of each class in image
    df = pd.DataFrame()
    df['Image_name'] = image_name
    df['Type_class'] = type_class
    df['Percent_class'] = percent_class
    df.to_csv('area_amp49_pred.csv', index=False)

