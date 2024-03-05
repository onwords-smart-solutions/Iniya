import f
import mqtt
import word_db
from firebase import get_data_from_firebase


def smart_home(uid,command,bigrams_command):
    homes = get_data_from_firebase(f"new_db/users/{uid}/homes")
    common_device_words = [word for word in command if word in word_db.device_words]



    rooms = f.get_users_room(homes=homes)
    room = set(rooms) & set(bigrams_command)
    if room:
        print(f"room found : {room}")
    else:
        room = set(rooms) & set(command)
        if room:
            print(f"room found : {room}")
        else:
            print("room not found...!!")


    #
    user_device_words = f.get_users_device_names(homes)
    print(type(user_device_words))
    # rooms_details = extract_room_details(homes)
    # print(user_device_words)

    user_device = set(command) & set(user_device_words)
    print(user_device)


    state = set(command) & set(word_db.controll_words)
    state = list(state)
    room=list(room)
    device = set(command) & set(word_db.device_words)
    device = list(device)
    if room:
        if device:
            print(f"ok boss, I am turning {state[0]} {room[0] }'s {device}")
        else:
            print(f"ok boss, I am turning {state[0]} {room[0]}")
            data = f.get_device_details_by_room_name(room[0])

            for x in data:
                pid = x["product_id"]
                topic = f"onwords/{pid}/status"
                did = x["device_id"]
                msg = {f"{did}": 1 if state[0]=="on" else 0}

                print(topic,msg)

                mqtt.publish(topic,str(msg))


    else:
        print(f"DO I need to turn off all {device}")
def extract_room_details(data):
    all_rooms = []
    # Iterate through each key (home ID) in the data
    for home_id, home_details in data.items():
        home_name = home_details.get('name', 'Unknown Home')
        rooms = home_details.get('rooms', {})
        for room_id, room_details in rooms.items():
            room_name = room_details.get('name', 'Unknown Room')
            products = room_details.get('products', {})
            for product_id, product_details in products.items():
                devices = product_details.get('devices', {})
                device_details = []
                for device_id, device_info in devices.items():
                    device_name = device_info.get('name', 'Unknown Device')
                    device_type = device_info.get('type', 'Unknown Type')
                    x = {"device_name":device_name,"type":device_type}
                    device_details.append(x)
                all_rooms.append(
                    {'Home': home_name, 'Room': room_name, 'Product ID': product_id, 'Devices': device_details})
    return all_rooms

# Extract room details






