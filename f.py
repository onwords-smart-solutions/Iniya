import time
from functools import wraps

from firebase import get_data_from_firebase
def time_decorator(func):
    @wraps(func)  # Use wraps to preserve metadata of the original function
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.time()  # Record the end time
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")  # Print the execution time
        return result  # Return the result of the function
    return wrapper
# @time_decorator
def get_users_room(homes):

    # homes = ref.get()
    _rooms = []
    for home_ids in homes:
        rooms = homes[home_ids]["rooms"]
        for room in rooms:
            room_name = rooms[room]['name']
            _rooms.append(room_name.lower())


    # print("returning rooms")
    return _rooms
def extract_device_names(data):
    device_names = []
    for home_id, home_data in data.items():
        for room_id, room_data in home_data['rooms'].items():
            if 'products' in room_data:
                for product_id, product_data in room_data['products'].items():
                    for device_id, device_data in product_data['devices'].items():
                        device_names.append(device_data['name'])
    return device_names

def get_users_device_names(homes):
    _devices = extract_device_names(homes)
    print(_devices)
    return _devices

    # for home_ids in homes:
    #     rooms = homes[home_ids]["rooms"]
    #     for room in rooms:
    #         try:
    #             product_id = rooms[room]["products"]
    #             for device in product_id:
    #                 devices = product_id[device]
    #                 print(devices)
    #                 for device_name in devices:
    #                     # print(device_name)
    #                     x = devices[device_name]
    #                     print(f"x = {x}")
    #                     for device in x:
    #                         print(device)
    #
    #         except:
    #             pass
    # print(_devices)



    # return devices

def generate_bigrams(text):
    words = text.split()
    bigrams = zip(words, words[1:])
    return [" ".join(bigram) for bigram in bigrams]



data = {
    "homes": [
        {
            "rooms": [
                {
                    "name": "Kitchen",
                    "productID": "3chfb126",
                    "devices": [
                        {"name": "Kitchen Fan", "type": "light"},
                        {"name": "Kitchen Light", "type": "light"},
                        {"name": "Kitchen Light", "type": "light"}
                    ]
                },
                {
                    "name": "Master Bedroom",
                    "productID": "3l1ftc009",
                    "devices": [
                        {"name": "Master Bedroom Tube", "type": "light"},
                        {"name": "Dummy1", "type": "light", "visibility": False},
                        {"name": "Dummy2", "type": "light", "visibility": False},
                        {"name": "Master Bedroom Fan", "type": "fan"}
                    ]
                },
                # Add other rooms as per your data structure
            ]
        },
        # Add other homes as per your data structure
    ]
}

# Function to extract rooms and their devices
def extract_rooms_and_devices(data):
    extracted_info = []

    for room in data['rooms']:
            room_info = {
                "Room Name": room['name'],
                "Product ID": room['productID'],
                "Devices": []
            }
            for device in room['devices']:
                device_info = {
                    "Name": device['name'],
                    "Type": device['type']
                }
                # Include visibility if it exists
                if "visibility" in device:
                    device_info["Visibility"] = device['visibility']
                room_info["Devices"].append(device_info)
            extracted_info.append(room_info)
    return extracted_info
uid = "3BoUcBC6ARWdtXfPHQstFaIPzum1"

# Printing the extracted information
user_data = get_data_from_firebase(f"new_db/users/{uid}/homes")
def get_device_details_by_room_name(room_name):
    product_ids = []
    device_ids = []
    type = []
    data = []



    if user_data:
        for home_uid in user_data:
            home_data = user_data[home_uid]
            rooms = home_data.get('rooms', {})
            for room_id, room_info in rooms.items():
                if room_info.get('name').lower() == room_name.lower():
                    products = rooms[room_id].get('products', {})
                    for product_id in products:
                        device_data = products.get(product_id, {})
                        devices = device_data.get('devices', {})

                        for device_id in devices:
                            _type = devices[device_id]["type"]
                            y = {"product_id": product_id, "device_id": device_id, "type": _type}
                            data.append(y)
                            # print(type)

                            # print(device_id)
                            # for x in devices[device_id]:
                            #     print(type(x))
                            #     _type = x.get('type', {})
                            #


    return data

print(get_device_details_by_room_name("green room"))


def get_device_details_by_device_name(device_name):
    if user_data:
        for home_uid in user_data:
            home_data = user_data[home_uid]
            rooms = home_data.get('rooms', {})
            for room_id, room_info in rooms.items():
                products = room_info.get('products', {})
                for product_id in products:
                    device_data = products.get(product_id, {})
                    devices = device_data.get('devices', {})
                    for device_id, device_info in devices.items():
                        if device_info.get('name').lower() == device_name.lower():
                            return product_id, device_id

    return None, None

# print(get_device_details_by_device_name("spot1"))