import io
from flask import Flask, request
from PIL import Image
from lwcc import LWCC
import json

from youtube_videos_capture_frames import FrameExtraction

frameExtractor = FrameExtraction(threshold=0.33,
                                         photo_detail=[[770, 855], [1650, 1920]])
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/get_count', methods=["POST"])
def getCount():
    if request.method != "POST":
        return

    if request.files.get("image"):

        im_file = request.files["image"]
        im_bytes = im_file.read()
        im = Image.open(io.BytesIO(im_bytes))
        im.save("img1.jpeg")

        return str(LWCC.get_count("img1.jpeg", "CSRNet", "SHA"))


@app.route('/start')
async def start():  # put application's code here
    print("Request received")
    frameExtractor.capture(url_video="https://www.youtube.com/watch?v=PlAOPMSaV18")
    return "Done"

@app.route('/update_photo', methods=["PUT"])
def update_photo():  # put application's code here
    if request.files.get("image"):
        # Method 1
        # with request.files["image"] as f:
        #     im = Image.open(io.BytesIO(f.read()))

        # Method 2
        im_file = request.files["image"]
        im_bytes = im_file.read()
        im = Image.open(io.BytesIO(im_bytes))
        # print(im)
        im.save("img1.png")
        # Save/Update photo to Firebase
        frameExtractor.update()
    return "Done"

@app.route('/threshold', methods=["PUT"])
def set_threshold():
    global frameExtractor
    threshold = 0.21
    if request.json.get("threshold"):
        threshold = request.json.get("threshold")
    frameExtractor.set_threshold(threshold)
    return "Done"

@app.route('/photo_detail', methods=["PUT"])
def set_photo_details():
    global frameExtractor
    photo_details = [[795, 1000], [0, 400]]
    if request.json.get("photo_detail"):
        photo_details = request.json.get("photo_details")
    frameExtractor.set_photo_details(photo_details)
    return "Done"

@app.route('/get_info', methods=["GET"])
def get_data():
    global frameExtractor
    return json.dumps(frameExtractor.get_info())

@app.route('/get_cycles')
def get_cycles():
    global frameExtractor
    return str(frameExtractor.get_count())

@app.route('/stop_capture')
def stopCapture():
    global frameExtractor
    return frameExtractor.stop_capture()

@app.route('/start_capture')
def startCapture():
    global frameExtractor
    return frameExtractor.start_capture()

@app.route('/at')
def getAtTime():
    global frameExtractor
    return str(frameExtractor.get_at())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)