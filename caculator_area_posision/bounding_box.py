# # import os
# # import glob
# # from PIL import Image, ImageOps
# # import cv2
# # import numpy as np
# # from skimage.segmentation import quickshift
# # from skimage.segmentation import mark_boundaries
# # import time
# #
# # color_map = [[0, 0, 255],
# #     [0, 255, 0],
# #     [255, 0, 0],
# #     [255, 0, 255],
# #     [0, 255, 255],
# #     [225, 255, 20],
# #     [0, 102, 204],
# #     [50, 150, 150],
# #     [150, 150, 150],
# #     [0, 0, 0],
# # ]
# #
# # ignore_color = [255, 255, 255]
# # other_color = [0, 0, 0]
# # palette = [255, 0, 0,
# #            0, 255, 0,
# #            0, 0, 255,
# #            255, 0, 255,
# #            255, 255, 0,
# #            20, 255, 255,
# #            204, 102, 0,
# #            150, 150, 50,
# #            150, 150, 150]
# #
# # for i in range(244):
# #     palette += other_color
# # palette += ignore_color
# # def reverse_prediction(np_image):
# #     grayscale = np.zeros(np_image.shape[:2])
# #     r, g, b = cv2.split(np_image)
# #     for i, color in enumerate(color_map):
# #         condition = np.logical_and(b == color[0], g == color[1])
# #         condition = np.logical_and(condition, r == color[2])
# #         grayscale[condition] = i
# #     return grayscale.astype('uint8')
# #
# # def get_contours(mask):
# #     list_contours = []
# #     for i in range(8):
# #         mask_i = mask.copy()
# #         mask_i[mask != i] = 255
# #         mask_i[mask == i] = 0
# #         contours, _ = cv2.findContours(mask_i, 1, 1)
# #         list_contours += contours
# #
# #     return list_contours
# #
# # def get_contours_label(img, list_contours):
# #     contours_label = []
# #     cleaned_contours = []
# #     for contour in list_contours:
# #         white_img = np.zeros(img.shape, dtype=np.uint8)
# #         cv2.drawContours(white_img, [contour], -1, 1, -1)
# #         white_img = white_img * (img + 1)
# #
# #         unique, counts = np.unique(white_img - 1, return_counts=True)
# #
# #         if 255 in unique:
# #             illegal_indexs = np.where(unique > 9)
# #             unique = np.delete(unique, illegal_indexs)
# #             counts = np.delete(counts, illegal_indexs)
# #
# #         if len(unique) == 0:
# #             continue
# #
# #         max_class_index = np.argmax(counts)
# #         contours_label.append(unique[max_class_index])
# #         cleaned_contours.append(contour)
# #
# #     return cleaned_contours, np.array(contours_label, dtype=np.uint8)
# #
# # def remove_illegal_contour(list_contours, contours_label):
# #     illegal_indexs = np.where(contours_label > 7)
# #     list_contours = np.delete(list_contours, illegal_indexs)
# #     contours_label = np.delete(contours_label, illegal_indexs)
# #
# #     return list_contours, contours_label
# #
# # if __name__ == '__main__':
# #     for image_path in glob.glob('amp49_vis/*_image.png'):
# #         prediction_path = image_path.replace('_image.png', '_prediction.png')
# #         image = Image.open(image_path)
# #
# #         # image = ImageOps.expand(image, border=10, fill=128)
# #         # image_np = np.array(image).astype('uint8')
# #
# #         prediction = Image.open(prediction_path)
# #         width, height = prediction.size
# #
# #         prediction_np = np.array(prediction)
# #         mask = reverse_prediction(prediction_np)
# #         mask = Image.fromarray(mask)
# #         mask = np.array(ImageOps.expand(mask, border=10, fill=9))
# #         list_contours = get_contours(mask)
# #         list_contours, contours_label = get_contours_label(mask, list_contours)
# #         list_contours, contours_label = remove_illegal_contour(list_contours, contours_label)
# #         print(len(contours_label), len(list_contours))
# #
# #         for index, contour in enumerate(list_contours):
# #             rect = cv2.minAreaRect(contour) # basically you can feed this rect into your classifier
# #             (x, y), (w, h), a = rect # a - angle
# #             if w < 5 or h < 5:
# #                 continue
# #
# #
# #             box = cv2.boxPoints(rect)
# #             box = np.int0(box) #turn into ints
# #             print(box)
# #             cv2.drawContours(mask, [box], 0, int(contours_label[index]), 1)
# #
# #         img_mask = Image.fromarray(mask)
# #         img_mask = ImageOps.crop(img_mask, border=10)
# #         img_mask.putpalette(palette)
# #         # img_mask = ImageOps.crop(img_mask, border=10)
# #         img_mask.save('{}_seq_tmp.png'.format(prediction_path.split('_prediction.png')[0]))
# #
# #
# #
# #
#
# import os
# import glob
# from PIL import Image
# import cv2
# import numpy as np
# import glob
# import pandas as pd
# color_map = [[0, 0, 255],
#     [0, 255, 0],
#     [255, 0, 0],
#     [255, 0, 255],
#     [0, 255, 255],
#     [225, 255, 20],
#     [0, 102, 204],
#     [50, 150, 150],
#     [150, 150, 150],
#     [0, 0, 0],
# ]
#
# def get_all_link_image_pred(path_folder, format):
#     path_file = glob.glob(path_folder + '/*_prediction.' + format)
#     return path_file
# def reverse_prediction(np_image):
#     grayscale = np.zeros(np_image.shape[:2])
#     r, g, b = cv2.split(np_image)
#     for i, color in enumerate(color_map):
#         condition = np.logical_and(b == color[0], g == color[1])
#         condition = np.logical_and(condition, r == color[2])
#         grayscale[condition] = i
#     return grayscale.astype('uint8')
#
# # # input_images = glob.glob('amp49_vis/*_image.png')
# # input_images = ['/home/hangnt/hangnt/1102_export_features/amp49_vis/2018_04_0001_000023_prediction.png']
# # for image_path in input_images:
# #     print(image_path)
# #     prediction_path = image_path.replace('_image.png', '_prediction.png')
# #     print(prediction_path)
# #     prediction = Image.open(prediction_path)
# #     prediction_np = np.array(prediction)
# #     mask = reverse_prediction(prediction_np)
# #     height, width = mask.shape
# #
# #     unique, counts = np.unique(mask, return_counts=True)
# #     print(unique)
# #     print(counts)
# #     morm_counts = np.round((counts / (height * width) * 100)) / 100
# #
# #     print(image_path)
# #     print(morm_counts)
# if __name__ == "__main__":
#     path_folder = '/home/hangnt/hangnt/1102_export_features/amp49_vis/'
#     format = 'png'
#     path_file = get_all_link_image_pred(path_folder, format)
#     type_class = []
#     percent_class = []
#     image_name = []
#     for prediction_path in path_file:
#         image_name.append((prediction_path.split('/'))[-1])
#         prediction = Image.open(prediction_path)
#         prediction_np = np.array(prediction)
#         mask = reverse_prediction(prediction_np)
#         height, width = mask.shape
#         unique, counts = np.unique(mask, return_counts=True)
#         morm_counts = np.round((counts / (height * width) * 100)) / 100
#         type_class.append(unique)
#         percent_class.append(morm_counts)
#         # unique list label of image
#         # counts number of pixel for each class of image
#         # morm_counts % area of each class in image
#     df = pd.DataFrame()
#     df['Image_name'] = image_name
#     df['Type_class'] = type_class
#     df['Percent_class'] = percent_class
#     df.to_csv('area_amp49_pred.csv', index=False)
#
#
# import glob
# from PIL import Image, ImageOps
# import cv2
# import numpy as np
# from skimage.segmentation import quickshift
# from skimage.segmentation import mark_boundaries
# import time
# for prediction_path in glob.glob('amp49_vis/*_seq_tmp.png'):
#     prediction = Image.open(prediction_path)
#     width, height = prediction.size
#
#     prediction_np = np.array(prediction)
#     mask = reverse_prediction(prediction_np)
#     mask = Image.fromarray(mask)
#     mask = np.array(ImageOps.expand(mask, border=10, fill=9))
#     list_contours = get_contours(mask)
#     list_contours, contours_label = get_contours_label(mask, list_contours)
#     list_contours, contours_label = remove_illegal_contour(list_contours, contours_label)
#     # print(len(contours_label), len(list_contours))
#     for index, contour in enumerate(list_contours):
#         rect = cv2.minAreaRect(contour)  # basically you can feed this rect into your classifier
#         (x, y), (w, h), a = rect  # a - angle
#         if w < 5 or h < 5:
#             continue
#         box = cv2.boxPoints(rect)
#         box = np.int0(box)  # turn into ints
#         cv2.drawContours(mask, [box], 0, int(contours_label[index]), 1)
#
#     img_mask = Image.fromarray(mask)
#     img_mask = ImageOps.crop(img_mask, border=10)
#     img_mask.putpalette(palette)
#     # img_mask = ImageOps.crop(img_mask, border=10)
#     img_mask.save('{}_seq_tmp.png'.format(prediction_path.split('_prediction.png')[0]))



