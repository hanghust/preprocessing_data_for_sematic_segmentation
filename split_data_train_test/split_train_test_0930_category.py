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
        for x in label.split(' '):
            Image_name.append(df_0930_categ['Image_name'][i])
            Review.append(df_0930_categ['Review'][i])
            Category.append(df_0930_categ['Category'][i])
            Labels.append(x)
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
    msk = np.random.rand(len(df_group)) < 0.8
    df_train_gb = df_group[msk]
    df_test_gb = df_group[~msk]
    df_train = df[df[In_col].isin(df_train_gb[In_col])]
    df_test = df[df[In_col].isin(df_test_gb[In_col])]
    return df_train, df_test

def save_gb_category(path, Cteg_col, output_path):

    df = pd.read_csv(path)
    Cteg_type = df[Cteg_col].unique()
    for Cteg in Cteg_type:
        df_filter = df.loc[df[Cteg_col] == Cteg]
        df_filter.to_csv(output_path+Cteg+'.csv', index=False)

if __name__ == '__main__':
    # input_file = 'data/data_0903_category.csv'
    # output_file = 'data/0930_category/data_0903_category_split_labels.csv'
    # df = load_file_csv(input_file)
    # df.to_csv(output_file, index=False)
    # EDA_data_label(output_file, 'data/0930_category/0930_category.png')

    In_col  = 'Image_name'
    Cteg_col = 'Category'
    output_path = 'data/0930_category/Category/'
    output_train = 'data/0930_category/Category/Train/0930_category_train_'
    output_test = 'data/0930_category/Category/Test/0930_category_test_'

    # category_file = extract_all_path(output_path, 'csv')
    # for path_file in category_file:
    #     try:
    #         df_train, df_test = group_category_data(path_file, In_col, Cteg_col)
    #         df_train.to_csv(output_train + (path_file.split('/'))[-1], index=False)
    #         EDA_data_label(output_train+(path_file.split('/'))[-1], output_train+((path_file.split('/'))[-1]).split('.')[0]+'.png')
    #         df_test.to_csv(output_test + (path_file.split('/'))[-1], index=False)
    #         EDA_data_label(output_test + (path_file.split('/'))[-1], output_test + (((path_file.split('/'))[-1]).split('.'))[0]+'.png')
    #     except Exception:
    #         print(path_file)
    #         pass

    # df_train, df_test = group_category_data(output_file, In_col, Cteg_col)
    # df_train.to_csv(output_train+'.csv', index=False)
    # EDA_data_label(output_train+'.csv', output_train+'.png')
    # df_test.to_csv(output_test + '.csv', index=False)
    # EDA_data_label(output_test + '.csv', output_test + '.png')


    #group data category

    # df_train_group = df_train.groupby([In_col, Cteg_col], axis=0).count().reset_index()
    # df_test_group = df_test.groupby([In_col, Cteg_col], axis=0).count().reset_index()
    # df_train_group.to_csv(output_train+'gb.csv', index=False)
    # EDA_data_label(output_train+'gb.csv', output_train+'gb.png')
    # df_test_group.to_csv(output_test + 'gb.csv', index=False)
    # EDA_data_label(output_test + 'gb.csv', output_test + 'gb.png')


    # plt test_data category
    df_train = pd.read_csv(output_path + 'train_gb.csv')
    my_report_train = sweetviz.analyze(df_train)
    my_report_train.show_html("data/0930_category/Category/Report_train.html")
    # print(df_train)
    # print(type(df_train['Labels']))
    # df_ = sns.countplot(df.Category)
    # plt.xlabel('the number of category')
    # plt.savefig(output_test + 'gb.png')

    # plt train_data category
    df_test = pd.read_csv(output_path + 'test_gb.csv')
    my_report_test = sweetviz.analyze(df_test)
    my_report_test.show_html("data/0930_category/Category/Report_test.html")
    # df_test['Labels'] = df_test['Labels'].astype('numeric')
    # df1 = sns.countplot(df.Category)
    # plt.xlabel('the number of category')
    # plt.savefig(output_train + 'gb.png')

    # my_report = sweetviz.compare([df_train, "Train"], [df_test, "Test"], "Labels")
    # my_report.show_html("data/0930_category/Category/Report.html")
    ################################################################3
    # save_gb_category(output_file, Cteg_col, output_path)

    # category_train = extract_all_path(output_path+'Train/', 'csv')
    # category_test = extract_all_path(output_path + 'Test/', 'csv')
    # i = 0
    # j = 0
    # try:
    #     for path in category_train:
    #         if i == 0:
    #             df_train = pd.read_csv(path)
    #             i = i+1
    #         else:
    #             df_train = df_train.append(pd.read_csv(path))
    #     df_train.to_csv(output_path+'train.csv', index=False)
    #     for path in category_test:
    #         if j == 0:
    #             df_test = pd.read_csv(path)
    #             j = j + 1
    #         else:
    #             df_test = df_test.append(pd.read_csv(path))
    #     df_test.to_csv(output_path + 'test.csv', index=False)
    # except Exception:
    #     print(Exception)
    #     pass

    # EDA_data_label(output_path+'train.csv', output_path+'train.png' )
    # EDA_data_label(output_path + 'test.csv', output_path + 'test.png')

    # demo group category

    # group data category
    # df_train = pd.read_csv(output_path + 'train.csv')
    # df_test = pd.read_csv(output_path + 'test.csv')
    # df_train_group = df_train.groupby([In_col, Cteg_col], axis=0).count().reset_index()
    # df_test_group = df_test.groupby([In_col, Cteg_col], axis=0).count().reset_index()
    # df_train_group.to_csv(output_path + 'train_gb.csv', index=False)
    # # EDA_data_label(output_path + 'train_gb.csv',output_path + 'train_gb.png')
    # df_test_group.to_csv(output_path + 'test_gb.csv', index=False)
    # EDA_data_label(output_path + 'test_gb.csv', output_path + 'test_gb.png')

    # # plt test_data category
    # df = pd.read_csv(output_path + 'test_gb.csv')
    #
    # sns.countplot(df.Category)
    # plt.xlabel('the number of category - test')
    # plt.savefig(output_path + 'test_gb.png')

    # # plt train_data category
    # df = pd.read_csv(output_path + 'train_gb.csv')
    #
    # sns.countplot(df.Category)
    # plt.xlabel('the number of category - train')
    # plt.savefig(output_path + 'train_gb.png')
