import os
import glob
from PIL import Image 
import cv2
import numpy as np

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

def reverse_prediction(np_image):
    grayscale = np.zeros(np_image.shape[:2])
    r, g, b = cv2.split(np_image)
    for i, color in enumerate(color_map):
        condition = np.logical_and(b == color[0], g == color[1])
        condition = np.logical_and(condition, r == color[2])
        grayscale[condition] = i
    return grayscale.astype('uint8')

# input_images = ['/data/1102_export_features/amp49_vis/2018_04_0001_000023_prediction.png']
input_images = glob.glob('amp49_vis/*_image.png')
for image_path in input_images:
    prediction_path = image_path.replace('_image.png', '_prediction.png')

    prediction = Image.open(prediction_path) 
    prediction_np = np.array(prediction) 
    mask = reverse_prediction(prediction_np)
    height, width = mask.shape

    unique, counts = np.unique(mask, return_counts=True)
    print(unique)
    print(counts)
    morm_counts = np.round((counts / (height * width) * 100)) / 100

    print(image_path)
    print(morm_counts)
