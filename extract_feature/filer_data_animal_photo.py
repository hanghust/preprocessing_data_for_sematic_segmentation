import pandas as pd
import os

df_0930 = pd.read_csv('data/data_0903.csv')
image_name = df_0930['names_image']
labels = df_0930['labels']
data = zip(image_name, labels)
# animal_photo = []
# animal_drawing = []
# peson_photo = []
# person_drawing = []
object_photo = []
object_drawing = []
for img_name, label in data:
    # if label == 0:
    #     peson_photo.append(img_name)
    #     img_name = img_name.replace('masks', 'origins')
    #     os.system("cp " + img_name + " person_photo/")
    # elif label == 1:
    #     person_drawing.append(img_name)
    #     img_name = img_name.replace('masks', 'origins')
    #     os.system("cp " + img_name + " person_drawing/")
    # elif label == 2:
    #     animal_photo.append(img_name)
    #     img_name = img_name.replace('masks', 'origins')
    #     os.system("cp "+ img_name +" animal_photo/")
    # elif label == 3:
    #     animal_drawing.append(img_name)
    #     img_name = img_name.replace('masks', 'origins')
    #     os.system("cp "+ img_name +" animal_drawing/")
    if label == 4:
        object_photo.append(img_name)
        img_name = img_name.replace('masks', 'origins')
        os.system("cp " + img_name + " object_photo/")
    elif label == 5:
        object_drawing.append(img_name)
        img_name = img_name.replace('masks', 'origins')
        os.system("cp " + img_name + " object_drawing/")



# list_ = [animal_photo, animal_drawing, peson_photo, person_drawing]
# list_name = ['animal_photo', 'animal_drawing', 'person_photo', 'person_drawing']
list_ = [object_photo, object_drawing]
list_name = ['object_photo', 'object_drawing']
data = zip(list_, list_name)
for img, names in data:
    df = pd.DataFrame()
    df[names] = img
    df.to_csv(names + '.csv')


