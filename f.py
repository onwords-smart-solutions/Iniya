from firebase import get_data_from_firebase

def get_users_room(homes):
    _rooms = []
    for home_ids in homes:
        rooms = homes[home_ids]["rooms"]
        for room in rooms:
            room_name = rooms[room]['name']
            _rooms.append(room_name.lower())
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
    return _devices

def generate_bigrams(text):
    words = text.split()
    bigrams = zip(words, words[1:])
    return [" ".join(bigram) for bigram in bigrams]

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
                if "visibility" in device:
                    device_info["Visibility"] = device['visibility']
                room_info["Devices"].append(device_info)
            extracted_info.append(room_info)
    return extracted_info


def get_device_details_by_room_name(uid, room_name):
    product_ids = []
    device_ids = []
    type = []
    data = []

    user_data = get_data_from_firebase(f"new_db/users/{uid}/homes")
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
    return data

def get_device_details_by_device_name(device_name, uid):
    user_data = get_data_from_firebase(f"new_db/users/{uid}/homes")
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