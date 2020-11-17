import pandas as pd
import os

category_file = 'data_category/final_irep_mp_categories.csv'
label_file_unmerge = 'data/data_0903.csv'
label_file_merge_1 = 'data/data_0903_merge_1.csv'
label_file_merge_2 = 'data/data_0903_merge_2.csv'

def read_label_csv(path, cols=['names_image', 'list_label']):
    df = pd.read_csv(path)
    label_df = df[cols]
    label_df.columns = ['Image_name', 'list_label']

    label_df = label_df.drop_duplicates()

    label_df['Image_name'] = label_df.apply(lambda row: row['Image_name'].split('/')[-1].split('.png')[0],
                                                  axis=1)
    label_df['list_label'] = label_df.apply(lambda row: row['list_label'][1:-1], axis=1)
    return label_df

if __name__ == '__main__':
    category_df = pd.read_csv(category_file)

    label_unmerge_df = read_label_csv(label_file_unmerge)
    print(label_unmerge_df)
    label_merge_1_df = read_label_csv(label_file_merge_1)
    label_merge_2_df = read_label_csv(label_file_merge_2)

    label_unmerge_category_df = pd.merge(category_df, label_unmerge_df, how='left', on='Image_name')
    label_merge_1_category_df = pd.merge(category_df, label_merge_1_df, how='left', on='Image_name')
    label_merge_2_category_df = pd.merge(category_df, label_merge_2_df, how='left', on='Image_name')

    label_unmerge_category_df.to_csv('data/data_0903_category.csv', index=False)
    label_merge_1_category_df.to_csv('data/data_0903_merge_1_category.csv', index=False)
    label_merge_2_category_df.to_csv('data/data_0903_merge_2_category.csv', index=False)