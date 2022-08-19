# import firebaseConfig
# import csv
# data = firebaseConfig.get_from_real_time_database()
#
# header = ["num_objects", " time_stamp", " data_type", " location"]
#
# with open('cars.csv', 'w') as file:
#     writer = csv.writer(file)
#     text = "num_objects, time_stamp, data_type, location, latitude, longitude\n"
#     # writer.writerow(header)
#     for item in data:
#         text+=item["cars"]+", "
#         text+=item["time_stamp"]+", "
#         text+=item["data_type"]+", "
#         text+=item["location"]+", "
#         text+=item["latitude"]+", "
#         text+=item["longitude"]
#         text+="\n"
#     array = []
#     array.append(text)
#     writer.writerow(array)

import sys

import cv2
from PIL import Image
from pympler import asizeof

img = cv2.imread('image.jpg')
print(asizeof.asizeof(img))