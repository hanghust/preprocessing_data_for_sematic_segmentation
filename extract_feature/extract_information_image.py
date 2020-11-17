import pandas as pd
import numpy as np
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import sys
def read_image(path_image):
    img = Image.open(path_image)
    np_img = np.array(img)
    list_label = np.unique(np_img)
    return list_label

def extract_all_path(path, format):
    path_file = glob.glob(path+'/*.'+format)
    return path_file

def extract_info_image(path_file):
    df_info_image = pd.DataFrame()
    list_label = []
    list_id = []
    labels = []
    for path_image in path_file:
        list_lb = read_image(path_image)
        for label in list_lb:
            list_id.append(path_image)
            labels.append(label)
            list_label.append(list_lb)
    df_info_image['names_image'] = list_id
    df_info_image['list_label'] = list_label
    df_info_image['labels'] = labels
    return df_info_image
def EDA_data_label(path, file_name):
    df = pd.read_csv(path)

    sns.countplot(df.labels)
    plt.xlabel('the number of labels')
    plt.savefig(file_name)




# path_file = extract_all_path('data_0930/masks/', 'png')
# df_info_image = extract_info_image(path_file)
# path = 'data/data_0903.csv'
# file_name = 'data/data_0930.png'
# df_info_image.to_csv(path)
# EDA_data_label(path, file_name)