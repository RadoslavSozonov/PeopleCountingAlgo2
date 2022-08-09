import argparse
import io
from flask import Flask, request
from PIL import Image
from lwcc import LWCC

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


if __name__ == '__main__':
    app.run()