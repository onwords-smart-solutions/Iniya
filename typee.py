
from firebase import get_data_from_firebase

uid = "3BoUcBC6ARWdtXfPHQstFaIPzum1"
user_data = get_data_from_firebase(f"new_db/users/{uid}/homes")

def get_device_details_by_type(room_name, device_type):
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
                        
                        for device_id, device_info in devices.items():
                            _type = device_info.get("type", "")
                            set(_type)
                            if _type.lower() == device_type.lower():
                                y = {"product_id": product_id, "device_id": device_id, "type": _type}
                                data.append(y)

    return data

def get_device_name():
    device_names = []
    if user_data:
        # Iterate over homes in user_data
        for home_id, home_info in user_data.items():
            # Check if 'rooms' exist in home_info
            if 'rooms' in home_info:
                rooms = home_info['rooms']
                # Iterate over rooms
                for room_id, room_info in rooms.items():
                    # Check if 'products' exist in room_info
                    if 'products' in room_info:
                        products = room_info['products']
                        # Iterate over products
                        for product_id, product_info in products.items():
                            # Check if 'devices' exist in product_info
                            if 'devices' in product_info:
                                devices = product_info['devices']
                                # Iterate over devices
                                for device_id, device_info in devices.items():
                                    # Check if 'name' exists in device_info
                                    if 'name' in device_info:
                                        device_names.append(device_info['name'].lower())
    return device_names

# Get device names


def get_home_device_details_by_type_(device_type):
    data = []
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
                        name = device_info.get("name", "")
                        _type = device_info.get("type", "")
                        if _type.lower() == device_type.lower():
                            y = {"home_uid": home_uid, "room_id": room_id, "product_id": product_id, "device_id": device_id, "type": _type}
                            data.append(y)

    return data

def get_device_details_by_devices_name(device_names):
    device_details = []
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
                        
                        if device_info.get('name', '').lower() in [name.lower() for name in device_names]:
                            device_info["home_uid"] = home_uid
                            device_info["room_id"] = room_id
                            device_info["product_id"] = product_id
                            device_info["device_id"] = device_id
                            device_details.append(device_info)

    return device_details    

