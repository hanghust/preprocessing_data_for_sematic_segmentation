from extract_information_image import extract_all_path, EDA_data_label
import numpy as np
import pandas as pd

# all file
def load_file_csv(path, file_name):
    path_list = extract_all_path(path, 'csv')
    data = pd.read_csv(path_list[0])
    for path_file in path_list[1:]:
        data1 = pd.read_csv(path_file)
        data = data.append(data1)
    data.to_csv(path + file_name+ '.csv', index=False)
    EDA_data_label(path + file_name+ '.csv', path + file_name + '.png')

# load_file_csv('data/data_0930_merge_2/data_unmerge/test/', 'data_test')
# each file
def split_train_test_data(path):
    path_list = extract_all_path(path, 'csv')
    for path_file in path_list:
        data = pd.read_csv(path_file)
        data_group = data.groupby(['names_image', 'list_label'], axis=0).count().reset_index()
        data_group = data_group.sample(len(data_group))
        msk = np.random.rand(len(data_group)) < 0.8
        train_merge = data_group[msk]
        test_merge = data_group[~msk]
        print(train_merge.shape)
        print(test_merge.shape)
        # train.to_csv('data/data_0930_merge_2/train_merge.csv',index=False)
        # test.to_csv('data/data_0930_merge_2/test_merge.csv', index=False)
        # data = pd.read_csv('data/data_0930_merge_2/data_0930_merge_2.csv')
        # train_label = pd.read_csv('data/data_0930_merge_2/train_merge.csv')
        train = data[~data['names_image'].isin(train_merge['names_image'])]
        test = data[~data['names_image'].isin(test_merge['names_image'])]
        if len(train) > len(test):
            train.to_csv('data/data_0930_tmp/data_unmerge/train/' + path_file.split('/')[-1], index=False)
            EDA_data_label('data/data_0930_tmp/data_unmerge/train/' + path_file.split('/')[-1],
                           'data/data_0930_tmp/data_unmerge/train/' + (path_file.split('/')[-1]).split('.')[
                               0] + '.png')
            test.to_csv('data/data_0930_tmp/data_unmerge/test/' + path_file.split('/')[-1], index=False)
            EDA_data_label('data/data_0930_tmp/data_unmerge/test/' + path_file.split('/')[-1],
                           'data/data_0930_tmp/data_unmerge/test/' + (path_file.split('/')[-1]).split('.')[
                               0] + '.png')
        else:
            train.to_csv('data/data_0930_tmp/data_unmerge/test/' + path_file.split('/')[-1], index=False)
            EDA_data_label('data/data_0930_tmp/data_unmerge/test/' + path_file.split('/')[-1],
                           'data/data_0930_tmp/data_unmerge/test/' + (path_file.split('/')[-1]).split('.')[
                               0] + '.png')
            test.to_csv('data/data_0930_tmp/data_unmerge/train/' + path_file.split('/')[-1], index=False)
            EDA_data_label('data/data_0930_tmp/data_unmerge/train/' + path_file.split('/')[-1],
                           'data/data_0930_tmp/data_unmerge/train/' + (path_file.split('/')[-1]).split('.')[
                               0] + '.png')
        # if len(train) > len(test):
        #     train.to_csv('data/data_0930_merge_2/data_unmerge/train/'+ path_file.split('/')[-1], index=False)
        #     EDA_data_label('data/data_0930_merge_2/data_unmerge/train/'+ path_file.split('/')[-1],
        #                    'data/data_0930_merge_2/data_unmerge/train/'+ (path_file.split('/')[-1]).split('.')[0]+'.png')
        #     test.to_csv('data/data_0930_merge_2/data_unmerge/test/'+ path_file.split('/')[-1], index=False)
        #     EDA_data_label('data/data_0930_merge_2/data_unmerge/test/' + path_file.split('/')[-1],
        #                    'data/data_0930_merge_2/data_unmerge/test/' + (path_file.split('/')[-1]).split('.')[0] + '.png')
        # else:
        #     train.to_csv('data/data_0930_merge_2/data_unmerge/test/' + path_file.split('/')[-1], index=False)
        #     EDA_data_label('data/data_0930_merge_2/data_unmerge/test/' + path_file.split('/')[-1],
        #                    'data/data_0930_merge_2/data_unmerge/test/' + (path_file.split('/')[-1]).split('.')[0] + '.png')
        #     test.to_csv('data/data_0930_merge_2/data_unmerge/train/' + path_file.split('/')[-1], index=False)
        #     EDA_data_label('data/data_0930_merge_2/data_unmerge/train/' + path_file.split('/')[-1],
        #                    'data/data_0930_merge_2/data_unmerge/train/' + (path_file.split('/')[-1]).split('.')[0] + '.png')

split_train_test_data('data/data_0930_tmp/')
