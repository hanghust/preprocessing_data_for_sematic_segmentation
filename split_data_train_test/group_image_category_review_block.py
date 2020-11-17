import os

segmentation_dir = '/home/binhps/irep_psd_result_output/data_0930_merge_1/Segmentation'
output_file = 'data_category/review_7n_review_21n_categories.csv'

category_dict = {
    'Review7_n': 'food',
    'Review8_n': 'food',
    'Review9_n': 'food',
    'Review10_n': 'food',
    'Review11_n': 'food',
    'Review12_n': 'food',
    'Review13_n': 'album',
    'Review14_n': 'app',
    'Review15_n': 'car',
    'Review16_n': 'card',
    'Review17_n': 'cosmetic',
    'Review18_n': 'cosmetic',
    'Review19_n': 'cosmetic',
    'Review20_n': 'energy',
    'Review21_n': 'fashion',
}

if __name__ == '__main__':
    list_review = category_dict.keys()
    with open(output_file, 'w') as cat_file:
        cat_file.write('Image_name,Category,Review\n')
        for review in category_dict:
            category = category_dict[review]
            with open(os.path.join(segmentation_dir, '{}.txt'.format(review)), 'r') as review_file:
                for filename in review_file:
                    cat_file.write('{},{},{}\n'.format(filename.strip(), category, review))


