import os
import glob
from PIL import Image, ImageOps
import cv2
import numpy as np

import time
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sweetviz


def EDA_data_percent_class(path_file, output):
    df = pd.read_csv(path_file)
    df_ = pd.DataFrame()
    type_class = []
    percent_class = []
    for data in df['Type_class']:
        data = data.replace('[', '')
        data = data.replace(']', '')
        data = data.split(' ')
        data = [i.replace(' ', '') for i in data if i != '']
        type_class = type_class + data
    for data in df['Percent_class']:
        data = data.replace('[', '')
        data = data.replace(']', '')
        data = data.split(' ')
        data = [i.replace(' ', '') for i in data if i != '']
        percent_class = percent_class + data
    print(len(type_class))
    print(len(percent_class))

    df_['Type_class'] = type_class
    df_['Percent_class'] = percent_class
    print(df_['Type_class'].unique())
    class_ = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in class_:
        df_fillter =df_.loc[df_['Type_class'] == i]
        try:
            sns.countplot(df_fillter.Percent_class)
            plt.xlabel('the Percent of labels ' + i)
            plt.savefig(output + i + '.png')
        except Exception:
            print(i)
    sns.countplot(df_.Percent_class)
    plt.xlabel('the Percent of labels ')
    plt.savefig(output)
    return df_

def EDA_data_posision(path_file, output):
    df = pd.read_csv(path_file)
    df_ = pd.DataFrame()
    type_class = []
    posision = []
    for data in df['Type_class']:
        data = data.replace('[', '')
        data = data.replace(']', '')
        data = data.split(',')
        data = [i.replace(' ', '') for i in data if i != '']
        type_class = type_class + data
    for data in df['Posision']:
        data = data.replace('[', '')
        data = data.replace(']', '')
        data = data.split(',')
        data = [i.replace(' ', '') for i in data if i != '']
        posision = posision + data
    print(len(type_class))
    print(len(posision))
    df_['Type_class'] = type_class
    df_['Posision'] = posision
    print(df_['Type_class'].unique())
    class_ = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # report = sweetviz.analyze(df_)
    # report.show_html('EDA_data_posision/'+"Report.html")
    for i in class_:
        df_fillter =df_.loc[df_['Type_class'] == i]
        # print(df_fillter)
        try:
            sns.countplot(df_fillter.Posision)
            plt.xlabel('the Percent of labels ' + i)
            plt.savefig(output + i + '.png')
        except Exception:
            print(i)
    sns.countplot(df_.Posision)
    plt.xlabel('the Percent of labels ')
    plt.savefig(output)

if __name__ == "__main__":
    df_ = EDA_data_percent_class('area_amp49_pred.csv', 'EDA_data_percent/area_amp49_pred_')
    # report = sweetviz.analyze(df_)
    # report.show_html('EDA_data_percent/'+"Report.html")
    # EDA_data_posision('locate_area_5x5.csv', 'EDA_data_posision/locate_area_5x5_')