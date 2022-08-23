import os

from vidgear.gears import CamGear
import requests
import datetime
import cv2
import time
from edge_detection import Edge_detection
import firebaseConfig as firebase
from os.path import exists


detected_photos_info = []
# DETECTION_URL = "http://localhost:5010/get_count"
# DETECTION_URL = "http://localhost:5002/cars-counting"
DETECTION_URL = "https://team-radoslavsozonov-peoplecountingalgo2-main-ryiib43suq-oa.a.run.app/get_count"
IMAGE = "img1.png"


class FrameExtraction:

    def __init__(self, threshold, photo_detail):
        self.stream = None
        edge_detection = Edge_detection()
        self.threshold = threshold
        self.photo_detail = photo_detail
        self.count = 1
        self.photo_to_compare = []
        self.detected_photos_info = []
        self.at = datetime.datetime.now()

        firebase.download_from_storage("img1.png", "img1.png")
        frame = cv2.imread("img1.png")
        if frame is None:
            self.photo_to_compare = None
        else:
            y_zone = self.photo_detail[0]
            x_zone = self.photo_detail[1]
            cropped_image = frame[y_zone[0]:y_zone[1], x_zone[0]:x_zone[1]]
            cropped_image = edge_detection.edge_detection_detect(cropped_image)
            self.photo_to_compare = []
            self.photo_to_compare = cropped_image

    def get_info(self):
        # print(detected_photos_info)
        return firebase.get_from_real_time_database()

    def get_at(self):
        return self.at

    def update(self):
        edge_detection = Edge_detection()
        # Get photo from firebas
        # if None, set self.photo_to_compare = None
        firebase.upload_to_storage("img1.png", "img1.png")
        frame = cv2.imread("img1.png")
        y_zone = self.photo_detail[0]
        x_zone = self.photo_detail[1]
        cropped_image = frame[y_zone[0]:y_zone[1], x_zone[0]:x_zone[1]]
        cropped_image = edge_detection.edge_detection_detect(cropped_image)
        self.photo_to_compare = []
        self.photo_to_compare = cropped_image

    def start_capture(self):
        # capture["start"] = 1
        return "Started"

    def stop_capture(self):
        # capture["start"] = 0
        return "Stopped"

    def get_count(self):
        return self.count

    def capture(self, url_video):
        print("stratred")
        self.stream = CamGear(source=url_video, stream_mode=True, time_delay=5,
                              logging=True).start()
        start_time = datetime.datetime.now()
        while True:
            timeC = datetime.datetime.now() + datetime.timedelta(hours=2)
            if timeC.hour == 6 and timeC.minute == 58:
                frame = self.stream.read()
                cv2.imwrite("img1.png", frame)
                firebase.upload_to_storage("img1.png", "img1.png")
                time.sleep(10)
            if 7 < timeC.hour < 20:
                break
            diff = timeC - start_time
            if diff.total_seconds() / 60 > 20:
                return

        edge_detection = Edge_detection()
        prev_res = []
        prev_res.append(0)
        self.count = 0
        loop = 1
        counter = 1
        # file = open("MyFile.txt", "a")
        while exists("img1.png") is None or self.photo_to_compare is None:
            now = datetime.datetime.now()
            diff = now - start_time
            if diff.total_seconds()/60 > 20:
                return
            continue
        # print("picture_found")
        frame = None
        image = cv2.imread("img1.png")
        y_zone = self.photo_detail[0]
        x_zone = self.photo_detail[1]
        cropped_image = image[y_zone[0]:y_zone[1], x_zone[0]:x_zone[1]]
        self.photo_to_compare = edge_detection.edge_detection_detect(cropped_image)
        while True:
            now = datetime.datetime.now()
            diff = now - start_time
            if diff.total_seconds() / 60 > 35:
                return
            for i in range(loop):
                    frame = self.stream.read()  # using functions from vidGear module

            loop = 30
            self.count += 1
            # print(self.count)
            metric_val_average = []
            y_zone = self.photo_detail[0]
            x_zone = self.photo_detail[1]
            cropped_image = frame[y_zone[0]:y_zone[1], x_zone[0]:x_zone[1]]
            cropped_image = edge_detection.edge_detection_detect(cropped_image)
            result = self.compare_edges_only(self.photo_to_compare, cropped_image)

            metric_val_average.append(result)
            result = round(sum(metric_val_average) / len(metric_val_average), 4)
            skip = self.write_to_directory(result, counter, cropped_image, prev_res, frame)
            # to_write += str(round(result, 3)) + " "

    def write_to_directory(self, result, counter, cropped_image, prev_res, frame):
        # self.threshold = 0.21
        # print(result)
        if result >= self.threshold and os.path.getsize('img1.png') > 2000000:
            if result > prev_res[0]:
                if prev_res[0] < self.threshold:
                    counter += 1
                    # print("Match")
                cv2.imwrite(IMAGE, frame)
                with open(IMAGE, "rb") as f:
                    image_data = f.read()
                # print(image_data)
                response = requests.post(DETECTION_URL, files={"image": image_data}).json()
                # print(response)
                firebase.upload_to_real_time_database({
                    "items": str(response),
                    "counter": str(counter),
                    "time": str(datetime.datetime.now() + datetime.timedelta(hours=2))
                })
                prev_res[0] = result
                self.photo_to_compare = cropped_image
                firebase.upload_to_storage("img1.png", "img1.png")
                time = datetime.datetime.now() + datetime.timedelta(hours=2)
                firebase.upload_to_storage("images/"+str(time.strftime("%Y-%m-%d %H:%M:%S"))+".png", "img1.png")

            return 0
        prev_res[0] = 0
        return 0

    def compare_edges_only(self, image1, image2):
        white_cells_image1 = 0
        white_cells_image2 = 0
        counter1 = 0
        counter2 = 0
        for i in range(len(image1)):
            for y in range(len(image1[0])):
                if image1[i][y] != 0:
                    white_cells_image1 += 1
                if image2[i][y] != 0:
                    white_cells_image2 += 1
                if image1[i][y] != 0 and image2[i][y] != 0:
                    counter2 += 1
        counter1 = max(1, counter1)
        counter2 = max(1, counter2)
        try:
            pers1 = round(counter1 / white_cells_image1, 4)
        except:
            pers1 = 0
        try:
            pers2 = round(counter2 / white_cells_image2, 4)
        except:
            pers2 = 0
        return (pers2) / 2

    def set_threshold(self, threshold):
        self.threshold = threshold

    def set_photo_details(self, photo_details):
        self.photo_detail = photo_details
