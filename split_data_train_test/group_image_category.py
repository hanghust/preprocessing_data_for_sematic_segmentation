import pandas as pd
import os

irep_reviews = ['Review1', 'Review2', 'Review3', 'Review4', 'Review5', 'Review6', 'Review11', 'Review17']
mp_reviews = ['MP-Review1', 'MP-Review2', 'MP-Review3', 'MP-Review4', 'MP-Review5', 'MP-Review6', 'MP-Review7']
irep_category_file = 'data_category/STATISTICS Review finished - Sheet1.csv'
mp_category_file = 'data_category/STATISTICS Review MP - Sheet1.csv'
segmentation_dir = '/home/binhps/irep_psd_result_output/data_0930_merge_1/Segmentation'

def parse_review_file(filename):
    with open(os.path.join(segmentation_dir, '{}.txt'.format(filename)), 'r') as file:
        for line in file:
            yield line.strip(), filename

def get_reviews_df(list_review):
    dfs = []
    for review in list_review:
        dfs.append(pd.DataFrame(parse_review_file(review), columns=['Image_name', 'Review']))
    return pd.concat(dfs)

# def read_file_csv(path, Rv_col):
#     df = pd.read_csv(path)
#     Rv_type = df[Rv_col].unique()
#     return df, Rv_type

def read_irep_category_csv(path, cols=['Image_name', 'Category']):
    df = pd.read_csv(path)
    category_df = df[cols]
    category_df.columns = ['Image_name', 'Category']

    category_df['Image_name'] = category_df.apply(lambda row: '_'.join(row['Image_name'].split('/')[2:4]),
                                                  axis=1)
    category_df['Category'] = category_df.apply(lambda row: row['Category'].strip().lower(), axis=1)
    return category_df

def read_mp_category_csv(path, cols=['Image_name', 'Catergory', 'Review_name']):
    df = pd.read_csv(path)
    category_df = df[cols]
    category_df.columns = ['Image_name', 'Category', 'Review_name']
    print(category_df.columns)

    category_df['Image_name'] = category_df.apply(lambda row: '{}-unmerge_{}'.format(row['Review_name'], row['Image_name'].split('/')[-1].split('.png')[0]),
                                                  axis=1)
    category_df['Category'] = category_df.apply(lambda row: row['Category'].strip().lower(), axis=1)
    return category_df[['Image_name', 'Category']]

# def return_list_name_image(s):
#     if s is list:
#         image, Rv_type = s
#         ls_img = image.split('/')
#         img = Rv_type + '-merge_2_'+ ls_img[2] + '_' + ls_img[-1]
#         return img
#     else:
#         image = s
#         ls_img = image.split('/')
#         img = ls_img[2] + '_' + ls_img[-1]
#         return img

# def process_return_list_name_image(df, col1, col2 = None, Rv_type = None):
#     data = pd.DataFrame()
#     if col2 == None:
#         data['image_name'] = df[col1].apply(return_list_name_image)
#         data['category'] = len(df)*[Rv_type]
#         data.to_csv('data_category/'+ Rv_type)
#     else:
#         data['image_name'] = df[[col1, col2]].apply(return_list_name_image, axis = 1)
#         data['category'] = len(df) * [Rv_type]
#         data.to_csv('data_category/' + Rv_type)

# def group_category_data():
#     path = 'data_category/STATISTICS Review finished - Sheet1.csv'
#     col1  = 'Image_name'
#     Rv_col = 'Review Name'
#     col_category = 'Category'
#     df, Rv_type = read_file_csv(path, Rv_col)
#     for Rv in Rv_type:
#         # df_filter = df[df[Rv_col]==Rv]
#         df_filter = df.loc[df[Rv_col] == Rv]
#         category = df_filter[col_category].unique()
#         # category = [(x.replace(' ', '')).lower() for x in category_]
#         if len(Rv.split('-')) == 1:
#             for categ in category:
#                 # df_filter_ = df_filter.loc[df_filter[col_category] == categ]
#                 df_filter_ = df_filter[df_filter[col_category].isin([categ, categ+' ', categ.lower(), (categ+ ' ').lower()])]
#                 process_return_list_name_image(df_filter_, col1= col1, Rv_type= Rv+'_'+(categ.replace(' ', '')).lower())
#         else:
#             for categ in category:
#                 # df_filter_ = df_filter.loc[df_filter[col_category] == categ]
#                 df_filter_ = df_filter[df_filter[col_category].isin([categ, categ + ' ', categ.lower(), (categ + ' ').lower()])]
#                 process_return_list_name_image(df_filter_, col1=col1, col2=Rv_col, Rv_type=Rv+'_'+(categ.replace(' ', '')).lower())

if __name__ == '__main__':
    irep_df = get_reviews_df(irep_reviews)
    mp_df = get_reviews_df(mp_reviews)
    irep_mp_df = pd.concat([irep_df, mp_df])

    irep_category_df = read_irep_category_csv(irep_category_file)
    mp_category_df = read_mp_category_csv(mp_category_file)
    irep_mp_category_df = pd.concat([irep_category_df, mp_category_df])

    irep_mp = pd.merge(irep_mp_df, irep_mp_category_df, how='left', on='Image_name')
    irep_mp.to_csv('data_category/irep_mp_categories.csv', index=False)

    # Concate with new_irep reviews
    irep_mp_old_df = pd.read_csv('data_category/irep_mp_categories.csv')
    irep_mp_new_df = pd.read_csv('data_category/review_7n_review_21n_categories.csv')
    final_irep_mp = pd.concat([irep_mp_old_df, irep_mp_new_df])
    final_irep_mp.to_csv('data_category/final_irep_mp_categories.csv', index=False)