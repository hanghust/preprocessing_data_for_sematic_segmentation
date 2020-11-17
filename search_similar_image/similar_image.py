
from skimage.measure import compare_ssim
import os
import pandas as pd
import numpy as np
from keras.preprocessing import image

def similar_images(folder_path):
    images = os.listdir(folder_path)
    compare = np.zeros((9025, 9025))
    image_name = []
    i = 0
    target_size = (224, 224)

    for image1 in range(len(images)):
        j= i
        image_name.append(images[image1])
        img = image.load_img(folder_path + images[image1], target_size=target_size)
        img = np.array(img)
        for image2 in range(image1, len(images)):
            img_2 = image.load_img(folder_path + images[image2], target_size=target_size)
            img_2 = np.array(img_2)
            cs = compare_ssim(img, img_2, multichannel=True)
            compare[i][j] = cs
            compare[j][i] = cs
            j += 1
        i += 1
    df_feature = pd.DataFrame(compare)
    df_feature.columns = image_name
    df_feature['image_names'] = image_name
    return df_feature


if __name__ == "__main__":
    folder_path = '/home/tanlm/hangnt/search_similar_images/origins/'
    df_feature = similar_images(folder_path)
    path_file = '/home/tanlm/hangnt/search_similar_images/output/compare.csv'
    df_feature.to_csv(path_file)
# import numpy as np
# import cv2
# import os
# import pandas as pd
# from keras.preprocessing import image
# from sklearn.metrics.pairwise import cosine_similarity
# def extract_feature(folder_path, path_file):
#     images = os.listdir(folder_path)
#     df_feature = pd.DataFrame()
#     target_size = (224, 224)
#     for image1 in images:
#         im = cv2.imread(folder_path + image1)
#         img_data = cv2.resize(im, target_size)
#         feature = img_data.reshape(224*224*3)
#         df_feature[image1.split('.')[0]] = feature
#     df_feature.to_csv(path_file, index=False)
#
# def cosine_distance(path_file, output_file):
#     df_feature = pd.read_csv(path_file)
#     cosine_feature = pd.DataFrame(cosine_similarity(df_feature.T))
#     cosine_feature.to_csv(output_file, index=False)
# if __name__ == "__main__":
#     folder_path = '/home/tanlm/hangnt/search_similar_images/origins/'
#     path_file = '/home/tanlm/hangnt/search_similar_images/output/feature_images_1.csv'
#     output_file = '/home/tanlm/hangnt/search_similar_images/output/cosine_similarity_images_1.csv'
#     extract_feature(folder_path, path_file)
#     # output_file = '/home/tanlm/hangnt/search_similar_images/output/correlation.csv'
#     cosine_distance(path_file, output_file)
#     # correlation(path_file, output_file)