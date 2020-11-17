import numpy as np
import os
import pandas as pd
from extract_information_image import extract_info_image, EDA_data_label, extract_all_path
def create_path_image(folder, image_list):
    for img in image_list:
        img = img.replace("unmerge", "merge_1")
        yield(folder + img + '.png')

# data_words = list(sent_to_words(df_train['Review']))
# ten anh tuong ung
def label(path_list, folder, path_file_csv, file_name):

    my_array2 = np.genfromtxt(path_list, dtype=str,
                              skip_header=0)
    image_list = list(create_path_image(folder, my_array2))
    df_info_image = pd.DataFrame()
    try:
        df_info_image = extract_info_image(image_list)
        df_info_image.to_csv(path_file_csv)
        EDA_data_label(path_file_csv, file_name)
    except Exception:
        print(Exception)
    return df_info_image


path = 'data_0930_merge_1_tmp/Segmentation/'
folder = 'data_0930_merge_1_tmp/masks/'
path_file_text = extract_all_path(path, 'txt')
for path_list in path_file_text:
    save_path = 'data/data_0930_merge_1/' + (str(path_list).split('/')[-1]).split('.')[0]
    path_file_csv = save_path + '.csv'
    file_name = save_path + '.png'
    df_info_inmage = label(path_list, folder, path_file_csv, file_name)
    print(df_info_inmage)
