import pyrebase

config = {
    "apiKey": "AIzaSyCAvnQjaKVj_5AhqIzz5RgAnQ07cCkRBrA",
    "authDomain": "livecamerazandvoortstation.firebaseapp.com",
    "projectId": "livecamerazandvoortstation",
    "storageBucket": "livecamerazandvoortstation.appspot.com",
    "messagingSenderId": "167375040356",
    "appId": "1:167375040356:web:84d2c26b2baf6dd3255471",
    "measurementId": "G-X3D12E4EGN",
    "databaseURL": "https://livecamerazandvoortstation-default-rtdb.europe-west1.firebasedatabase.app/"
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

    prev_time = 100
    filtered = []
    for item in list_item:
        time = item["time"].split(" ")[1].split(":")[1]
        if int(time) != prev_time and int(time)-1 != prev_time:
            filtered.append({
                "cars": item["items"],
                "time_stamp": item["time"],
                "data_type": "car",
                "location": "Centre Parcs Strandhotel",
                "latitude": "52.3797712",
                "longitude": "4.5319976"
            })
            prev_time = int(time)

    return filtered

