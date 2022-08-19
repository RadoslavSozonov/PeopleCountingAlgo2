# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Perform test request
"""

import pprint

import requests
DETECTION_URL = "https://team-radoslavsozonov-peoplecountingalgo2-main-ryiib43suq-oa.a.run.app/update_photo"
# DETECTION_URL = "http://localhost:5000/update_photo"
IMAGE = "image.jpg"

# Read image
with open(IMAGE, "rb") as f:
    image_data = f.read()

response = requests.put(DETECTION_URL, files={"image": image_data}).json()

pprint.pprint(response)
