import pandas as pd
import json
def convert_csv_json(path, input_file, output_file):
        df = pd.read_csv(input_file)
        output_percent = []
        image = {}
        info_image = {}
        i = 0
        class_list = ['person_photo', 'person_drawing', 'animal_photo', 'animal_drawing', 'object_photo',
                      'object_drawing', 'symbol', 'text', 'other_photo', 'other_drawing']
        for type_class, percent_class in zip(df['Type_class'], df['Percent_class']):
            image_name = df['Image_name'][i]
            info_image['Image_name_pred'] = path + image_name
            i = i + 1
            type_class = type_class.replace('[', '')
            type_class = type_class.replace(']', '')
            type_class = type_class.split(' ')
            type_class = [i for i in type_class if i != '']
            percent_class = percent_class.replace('[', '')
            percent_class = percent_class.replace(']', '')
            percent_class = percent_class.split(' ')
            percent_class = [i for i in percent_class if i != '']
            j = 0
            for class_name in class_list:
                if str(j) in type_class:
                    info_image[class_name] = percent_class[type_class.index(str(j))]
                else:
                    info_image[class_name] = ''
                j = j + 1
            image['Image_name'] = path + image_name.replace('_prediction', '_image')
            image['Infor'] = info_image
            output_percent.append(image)
        with open(output_file+'result.json', 'w') as fp:
            json.dump(output_percent, fp)
if __name__ == '__main__' :
    convert_csv_json('/home/hangnt/hangnt/1102_export_features/amp49_vis/', 'area_amp49_pred.csv', 'EDA_data_percent/')


