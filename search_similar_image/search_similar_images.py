## using download weight pretrain_model for search similar images project

# using pretrain model InceptionV3
# from tensorflow.keras.applications import InceptionV3
# from tensorflow.keras.applications.inception_v3 import decode_predictions
# from keras.applications.inception_v3 import preprocess_input

# using for cosine distance (between two vector)
from scipy import spatial

# using for cosine distance for array multiable dim
from sklearn.metrics.pairwise import cosine_similarity

# #Model for Resnet
# from tensorflow.keras.applications.resnet50 import ResNet50
# from tensorflow.keras.applications.resnet50 import decode_predictions
# from keras.applications.resnet50 import preprocess_input

#Model for VGG16
from tensorflow.keras.applications import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.layers import Flatten

from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from os import listdir
from PIL import Image as PImage

# For ResNet and VGG, img_width, img_height = 224, 224

def search_similar_images(folder_path, path_file):
    img_width, img_height = 224, 224

    #for ResNet, InceptionV3 will be replaced by ResNet50, for VGG, InceptionV3 will be replaced by VGG16

    model_pretrained = VGG16(weights='imagenet',
                          include_top=False,
                          input_shape=(img_height, img_width, 3))

    # images = os.listdir(folder_path)
    # f = open("list_16_image.txt", "r")
    # images = f.readlines()
    # images = [i.replace('\n','') for i in images]
    images = ['MP-Review4-unmerge_283167891512.png', 'Review18_n-unmerge_108_00002_2019_01_0005_000464.png', 'Review18_n-unmerge_109_00018_2018_10_0009_000882.png', 'Review19_n-unmerge_00121_00021_2018_08_0001_000054.png', '2018_04_0001_000025.png', 'Review19_n-unmerge_00250_00171_2018_06_0007_000613.png']
    df_feature = pd.DataFrame()
    for image1 in images:
        im = image.load_img(folder_path + image1, target_size=(img_width, img_height))
        img_data = image.img_to_array(im)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)

        cnn_feature = model_pretrained.predict(img_data, verbose=0)
        out_put = Flatten()(cnn_feature)

        df_feature[image1.split('.')[0]] = out_put[0]
    df_feature.to_csv(path_file, index=False)

def cosine_distance(path_file, output_file):
    df_feature = pd.read_csv(path_file)
    cosine_feature = pd.DataFrame(cosine_similarity(df_feature.T))
    cosine_feature.to_csv(output_file, index=False)

def correlation(path_file, output_file):
    # col_corr = set() # Set of all the names of deleted columns
    df = pd.read_csv(path_file)
    corr_matrix = df.corr()
    (pd.DataFrame(corr_matrix)).to_csv(output_file)
    # for i in range(len(corr_matrix.columns)):
    #     for j in range(i):
    #         if (corr_matrix.iloc[i, j] >= threshold) and (corr_matrix.columns[j] not in col_corr):
    #             colname = corr_matrix.columns[i] # getting the name of column
    #             col_corr.add(colname)
    #             if colname in dataset.columns:
    #                 del dataset[colname] # deleting the column from the dataset
    # return dataset
if __name__ == "__main__":
    folder_path = '/home/tanlm/hangnt/search_similar_images/origins/'
    path_file = '/home/tanlm/hangnt/search_similar_images/output/feature_images1.csv'
    output_file = '/home/tanlm/hangnt/search_similar_images/output/cosine_similarity_images1.csv'
    search_similar_images(folder_path, path_file)
    output_file_ = '/home/tanlm/hangnt/search_similar_images/output/correlation1.csv'
    cosine_distance(path_file, output_file)
    correlation(path_file, output_file_)

# import pandas as pd
# path_file = '/home/hangnt/hangnt/search_similar_images/output/feature_images.csv'
# output_file = '/home/hangnt/hangnt/search_similar_images/output/cosine_similarity_images.csv'
# feature = pd.read_csv(path_file)
# print(feature.shape)
# output = pd.read_csv(output_file)
# print(output.shape)
# col = feature.columns
# print(len(col))
# output.columns = col
# output['col'] = col
# output.to_csv(output_file, index=False)