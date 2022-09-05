import pyrebase

config = {
    "apiKey": "AIzaSyAqWkRyXczSv9Df3nRJf5YaVdJP-kT2krQ",
    "authDomain": "livecamerazandvoortstation2.firebaseapp.com",
    "projectId": "livecamerazandvoortstation2",
    "storageBucket": "livecamerazandvoortstation2.appspot.com",
    "messagingSenderId": "803951266182",
    "appId": "1:803951266182:web:9fb71777edf07eae750407",
    "measurementId": "G-S88YF16DCH",
    "databaseURL": "https://livecamerazandvoortstation2-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config=config)
storage = firebase.storage()
database = firebase.database()

path_on_cloud = "image1.jpg"
path_local = "img1.png"


def upload_to_storage(name_cloud, name_local):
    storage.child(name_cloud).put(name_local)


def download_from_storage(name_cloud, name_local):
    storage.child(name_cloud).download(name_local)


def upload_to_real_time_database(data):
    database.push(data)


def get_from_real_time_database():
    res = database.get()
    list_item = []
    for item in res.each():
        list_item.append(item.val())

    return image_filter(list_item)



def image_filter(list_item):
    prev_time = 100
    filtered = []

    for item in list_item:
        time = extract_time(item)
        if int(time) != prev_time and int(time) - 1 != prev_time and int(item["items"]) != 0:
            filtered.append(config_object(item))
            prev_time = int(time)

    return filtered


def extract_time(item):
    return item["time"].split(" ")[1].split(":")[1]


def config_object(item):
    return {
                "cars": item["items"],
                "time_stamp": item["time"],
                "data_type": "people",
                "location": "Railcam - Zandvoort",
                "latitude": "52.3758194",
                "longitude": "4.5306274"
            }

