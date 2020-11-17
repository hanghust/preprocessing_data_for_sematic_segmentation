from extract_information_image import extract_all_path, EDA_data_label
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sweetviz

# all file
def load_file_csv(path_file):
    df_0930_categ = pd.read_csv(path_file)
    list_label = df_0930_categ['list_label']
    df = pd.DataFrame()
    Image_name = []
    Review = []
    Category = []
    Labels = []
    i = 0
    for label in list_label:
        for x in str(label).split(' '):
            Image_name.append(df_0930_categ['Image_name'][i])
            Review.append(df_0930_categ['Review'][i])
            Category.append(df_0930_categ['Category'][i])
            Labels.append(int(x))
        i = i + 1
    df['Image_name'] = Image_name
    df['Review'] = Review
    df['Category'] = Category
    df['Labels'] = Labels
    return  df

def group_category_data(path, In_col, Cteg_col):

    df = pd.read_csv(path)
    df_group = df.groupby([In_col, Cteg_col], axis=0).count().reset_index()
    df_group = df_group.sample(len(df_group))
    # msk = np.random.rand(len(df_group)) < 0.8
    # df_train_gb = df_group[msk]
    # df_test_gb = df_group[~msk]

    df_train_gb = df_group[:round(80*len(df_group))]
    df_test_gb = df_group[round(80 * len(df_group)):]
    df_train = df[df[In_col].isin(df_train_gb[In_col])]
    df_test = df[df[In_col].isin(df_test_gb[In_col])]
    return df_train, df_test

def save_gb_category(path, Cteg_col, output_path):

    df = pd.read_csv(path)
    Cteg_type = df[Cteg_col].unique()
    for Cteg in Cteg_type:
        df_filter = df.loc[df[Cteg_col] == Cteg]
        df_filter.to_csv(output_path+Cteg+'.csv', index=False)

def merge_data_same_category(df, Category_col):
    category_map1 = ['unlabeled', 'unknow', 'gym', 'u-insurance', 'insurrance', 'card-bank', 'card', 'bank card', 'takanofuuzu', 'kabu', 'superman', 'panasonic']
    category_map2 = ['unknown', 'unknown', 'service', 'insurance', 'insurance', 'bank', 'bank', 'bank', 'medicine', 'service', 'game', 'service']

    category_map = zip(category_map1, category_map2)
    for map1, map2 in category_map:
        df[Category_col] = df[Category_col].replace({map2: map1})
    return df

if __name__ == '__main__':
    # data 0930_category
    input_file = 'data/data_0903_category.csv'
    output_file = 'data/0930_category_merge/data_0903_category_split_labels.csv'

    In_col  = 'Image_name'
    Cteg_col = 'Category'
    output_path = 'sample/'
    output_train = 'sample/0930_category_train'
    output_test = 'sample/0930_category_test'


    # output_path = 'data/0930_category_merge/Category/'
    # output_train = 'data/0930_category_merge/Train/0930_category_train'
    # output_test = 'data/0930_category_merge/Test/0930_category_test'
    #
    # # data 0930_merge_1_category
    # input_file = 'data/data_0903_merge_1_category.csv'
    # output_file = 'data/0930_merge_1/data_0903_category_split_labels.csv'
    #
    # In_col  = 'Image_name'
    # Cteg_col = 'Category'
    # output_path = 'data/0930_merge_1/Category/'
    # output_train = 'data/0930_merge_1/Train/0930_category_train'
    # output_test = 'data/0930_merge_1/Test/0930_category_test'


    # # data 0930_merge_2_category
    # input_file = 'data/data_0903_merge_2_category.csv'
    # output_file = 'data/0930_merge_2/data_0903_category_split_labels.csv'
    #
    # In_col  = 'Image_name'
    # Cteg_col = 'Category'
    # output_path = 'data/0930_merge_2/Category/'
    # output_train = 'data/0930_merge_2/Train/0930_category_train'
    # output_test = 'data/0930_merge_2/Test/0930_category_test'
    try:
        # df = load_file_csv(input_file)
        # df = merge_data_same_category(df, Cteg_col)
        # df.to_csv(output_file, index=False)
        # # report = sweetviz.analyze(df)
        # # report.show_html(output_path+"Report.html")
        #
        #
        # df_train, df_test = group_category_data(output_file, In_col, Cteg_col)
        # # my_report = sweetviz.compare([df_train, "Train"], [df_test, "Test"], "Labels")
        # # my_report.show_html(output_path + "Report_compare.html")
        # df_train.to_csv(output_train+'.csv', index=False)
        # # report_train = sweetviz.analyze(df_train)
        # # report_train.show_html(output_train + "_Report_train.html")
        # # EDA_data_label(output_train+'.csv', output_train+'.png')
        # df_test.to_csv(output_test + '.csv', index=False)
        # # report_test = sweetviz.analyze(df_test)
        # # report_test.show_html(output_test + "_Report_test.html")
        # # EDA_data_label(output_test + '.csv', output_test + '.png')
        # # #
        # EDA_data_label(output_train + '.csv', output_train + '4.png')
        # print(output_test)
        EDA_data_label(output_test + '.csv', output_test + '4.png')
    except Exception:
        pass
