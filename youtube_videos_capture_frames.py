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
DETECTION_URL = "https://team-radoslavsozonov-peoplecountingalgo2-main-ryiib43suq-oa.a.run.app/get_count"
IMAGE = "img1.png"


class FrameExtraction:

    def __init__(self, threshold, photo_detail):
        self.stream = None
        self.threshold = threshold
        self.photo_detail = photo_detail
        # self.count = 1
        self.photo_to_compare = []
        self.detected_photos_info = []
        self.at = datetime.datetime.now()

        firebase.download_from_storage("img1.png", "img1.png")
        frame = cv2.imread("img1.png")

        if frame is None:
            self.photo_to_compare = None
        else:
            self.set_image(frame)

    # set the new 'photo_to_look_for'
    def set_image(self, frame):
        cropped_image = self.crop_detect_edge_image(frame)
        self.photo_to_compare = []
        self.photo_to_compare = cropped_image

    # get the info from all extracted images
    def get_info(self):
        return firebase.get_from_real_time_database()

    # update photo in firebase storage and in the class
    def update(self):
        firebase.upload_to_storage("img1.png", "img1.png")
        frame = cv2.imread("img1.png")
        self.set_image(frame)

    # def get_count(self):
    #     return self.count

    # The function that lead the photo extraction
    def capture(self, url_video):
        self.stream = CamGear(source=url_video, stream_mode=True, time_delay=5,
                              logging=True).start()
        start_time = datetime.datetime.now() + datetime.timedelta(hours=2)

        # First while loop, check if it is the time period to extract frames
        if not self.check_the_time_zone(start_time):
            return

        # Second while loop, check if there is a set 'photo_to_look_for'
        if not self.check_if_the_photo_is_set(start_time):
            return

        # Third while loop, here is happening the frame extraction
        self.start_extracting(start_time)
        return

    # Check if it is the time period to extract frames
    def check_the_time_zone(self, start_time):
        while True:
            timeC = datetime.datetime.now() + datetime.timedelta(hours=2)
            if timeC.hour == 6 and timeC.minute == 58:
                frame = self.stream.read()
                cv2.imwrite("img1.png", frame)
                firebase.upload_to_storage("img1.png", "img1.png")
                time.sleep(90)
            if 7 <= timeC.hour < 20:
                break
            diff = timeC - start_time
            if diff.total_seconds() / 60 > 20:
                return False
        return True

    # Check if there is a set 'photo_to_look_for'
    def check_if_the_photo_is_set(self, start_time):
        while exists("img1.png") is None or self.photo_to_compare is None:
            now = datetime.datetime.now()
            diff = now - start_time
            if diff.total_seconds() / 60 > 20:
                return False
            continue

        return True

    # Extraction of a frame every 1 second
    def start_extracting(self, start_time):
        prev_res = [0]

        frame = None
        image = cv2.imread("img1.png")

        self.photo_to_compare = self.crop_detect_edge_image(image)
        loop = 1
        while True:
            now = datetime.datetime.now()
            diff = now - start_time
            if diff.total_seconds() / 60 > 30:
                return

            for i in range(loop):
                frame = self.stream.read()  # using functions from vidGear module

            loop = 30
            # the edges of the frame are detected and compared to the 'photo_to_look_for'
            self.frame_procession(frame, prev_res)

    # The edges of the frame are detected and compared to the 'photo_to_look_for'
    def frame_procession(self, frame, prev_res):
        metric_val_average = []

        # crop the image and detect edges
        cropped_image = self.crop_detect_edge_image(frame)
        # compare to the 'photo_to_look_for'
        result = self.compare_edges_only(self.photo_to_compare, cropped_image)

        metric_val_average.append(result)
        result = round(sum(metric_val_average) / len(metric_val_average), 4)

        # check the similarity between the photos and update 'photo_to_look_for'
        self.write_to_directory(result, cropped_image, prev_res, frame)

    # Crop the image and detect edges
    def crop_detect_edge_image(self, frame):
        edge_detection = Edge_detection()
        y_zone = self.photo_detail[0]
        x_zone = self.photo_detail[1]
        cropped_image = frame[y_zone[0]:y_zone[1], x_zone[0]:x_zone[1]]
        return edge_detection.edge_detection_detect(cropped_image)

    # Check the similarity between the photos and update 'photo_to_look_for'
    def write_to_directory(self, result, cropped_image, prev_res, frame):
        if result >= self.threshold and result > prev_res[0]:
            response = self.photo_process(frame)

            if response == 0:
                prev_res[0] = 0
                return 0

            self.to_firebase_save_data(response, result)
            self.photo_to_compare = cropped_image
            prev_res[0] = result
            return 0

        prev_res[0] = 0
        return 0

    # Save the new photo to the firebase storage
    # Update the photo to look for
    # Save the info for the photo in the firebase realtime database
    def to_firebase_save_data(self, response = 0, result = 0):
        firebase.upload_to_real_time_database({
            "items": str(response),
            "counter": str(1),
            "time": str(datetime.datetime.now() + datetime.timedelta(hours=2)),
            "threshold": result
        })

        time = datetime.datetime.now() + datetime.timedelta(hours=2)
        firebase.upload_to_storage("img1.png", "img1.png")
        firebase.upload_to_storage("images/" + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".png", "img1.png")

    # Processing of the photo, send the photo to the car or people counting algorithms
    def photo_process(self, frame):
        cv2.imwrite(IMAGE, frame)
        with open(IMAGE, "rb") as f:
            image_data = f.read()
        if os.path.getsize('img1.png') < 2200000:
            return 0
        # receive the number of cars or people
        response = requests.post(DETECTION_URL, files={"image": image_data}).json()
        return response

    # Comparison between the detected edges of the two photos
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
                    counter1 += 1
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
        if pers2 > 0.25 and pers1 > 0.25:
            return (pers2 + pers1) / 2
        return 0

    # set a new threshold
    def set_threshold(self, threshold):
        self.threshold = threshold

    # set a new zone to compare only
    def set_photo_details(self, photo_details):
        self.photo_detail = photo_details