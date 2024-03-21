import f
import mqtt
import word_db
from firebase import get_data_from_firebase
import datas
import re

def smart_home(uid,command,bigrams_command):
    homes = get_data_from_firebase(f"new_db/users/{uid}/homes")
    common_device_words = [word for word in command if word in word_db.device_words]


    device_names = datas.get_device_name()
    device_name = set(device_names) & set(bigrams_command)
    if device_name:
        print(f"Device name found : {device_name}")
    else:
        device_name = set(device_names) & set(command)
        if device_name:
            print(f"Device name found : {device_name}")
        else:
                print("Device name not found...!!")

    devices_name = list(device_name)
    rooms = f.get_users_room(homes=homes)
    # Assuming bigram_command is a list of words from the command
    bigram_command = command

    room_names = []
    i = 0
    while i < len(bigram_command):
        if i + 1 < len(bigram_command) and f"{bigram_command[i]} {bigram_command[i + 1]}" in rooms:
            room_names.append(f"{bigram_command[i]} {bigram_command[i + 1]}")
            i += 2
        elif bigram_command[i] in rooms:
            room_names.append(bigram_command[i])
            i += 1
        else:
            i += 1

    state = set(command) & set(word_db.controll_words)
    state = list(state)
    room = room_names
    device = set(command) & set(word_db.device_words)
    device = list(device)

    speed = set(command) & set(word_db.fan_speed_word)
    speed = list(speed)
    speeds = []
   
    for s in speed:
        speeds.extend(re.findall(r'\d+', s))
        
 # Speed Count 
    full_device_name = ' '.join(devices_name)

    command_string = ' '.join(command)
    command_string_without_device_name = command_string.replace(full_device_name, '').strip()
    command_without_device_name = command_string_without_device_name.split()
    speed_count = set(command_without_device_name) & set(word_db.fan_speed_count)
    speed_count = list(speed_count)

    if room and devices_name:
        data = datas.get_device_details_by_devices_name(devices_name)
                
        for x in data:  
            pid = x["product_id"]
            topic = f"onwords/{pid}/status"
            did = x["device_id"]
            
            msg = {f"{did}": 1 if state[0]=="on" else 0}

            print(topic,msg)
            
            #mqtt.publish(topic,str(msg))
            
    elif room:
        for room_name in room:
            if device:
                for dev in device:
                    if dev in ['lights', 'light', 'bulb']:
                        device_type = "light"
                        print(f"Ok boss, I am turning {state[0]} {room_name}'s {device_type}")
                        data = datas.get_device_details_by_type(room_name, device_type)
                        for x in data:
                            pid = x["product_id"]
                            topic = f"onwords/{pid}/status"
                            did = x["device_id"]
                            msg = {f"{did}": 1 if state[0] == "on" else 0}
                            print(topic, msg)
                            # mqtt.publish(topic, str(msg))
                            
                    elif dev in ['fans', 'fan']:
                        device_type = "fan"
                        if speed:
                            if speed_count:
                                    print("speed count is :", speed_count)

                                    print(f"Ok boss, I am {state[0]} the {room_name}'s {device_type} {speed[0]} to {speed_count[0]}")
                                    data = datas.get_device_details_by_type(room_name, device_type)
                                    for x in data:
                                        pid = x["product_id"]
                                        topic = f"onwords/{pid}/status"
                                        did = x["device_id"]
                                        
                                        if speed_count[0] == "low":
                                            msg = {f"{did}": 1 if state[0] == "on "or state[0] == "start" else (0 if state[0] == "off" or state[0] == "stop" else 1), 'speed': 1}
                                            
                                        elif speed_count[0] == "medium":
                                            msg = {f"{did}": 1 if state[0] == "on" or state[0] == "start" else (0 if state[0] == "off" or state[0] == "stop" else 1), 'speed': 3}
 
                                        elif speed_count[0] == "high":
                                            msg = {f"{did}": 1 if state[0] == "on" or state[0] == "start" else (0 if state[0] == "off" or state[0] == "stop" else 1), 'speed': 5}
                                        
                                        else:
                                            msg = {f"{did}": 1 if state[0] == "on" or state[0] == "start" else (0 if state[0] == "off" or state[0] == "stop" else 1), 'speed': int(speed_count[0])}

                                        print(topic, msg)
                                        # mqtt.publish(topic, str(msg))
  
                            else:
                                print(f"Ok boss, I am {state[0]} the {room_name}'s {device_type} speed-{speeds[0]}")
                                data = datas.get_device_details_by_type(room_name, device_type)
                                for x in data:
                                    pid = x["product_id"]
                                    topic = f"onwords/{pid}/status"
                                    did = x["device_id"]
                                    msg = {f"{did}": 1 if state[0] == "on" or state[0] == "start" else (0 if state[0] == "off"  else "1"), 'speed': int(speeds[0])}
                                    print(topic, msg)
                                    # mqtt.publish(topic, str(msg))
                        else:
                            print("Speed not found")
                            print(f"Ok boss, I am turning {state[0]} {room_name}'s {device_type}")
                            data = datas.get_device_details_by_type(room_name, device_type)
                            for x in data:
                                pid = x["product_id"]
                                topic = f"onwords/{pid}/status"
                                did = x["device_id"]
                                msg = {f"{did}": 1 if state[0] == "on" or state[0] == "start" else 0}
                                print(topic, msg)
                                # mqtt.publish(topic, str(msg))
            else:
                print(f"Ok boss, I am turning {state[0]} {room_name}")
                data = f.get_device_details_by_room_name(room_name)
                for x in data:
                    pid = x["product_id"]
                    topic = f"onwords/{pid}/status"
                    did = x["device_id"]
                    msg = {f"{did}": 1 if state[0] == "on" else 0}
                    print(topic, msg)
                    # mqtt.publish(topic, str(msg))
    elif devices_name:
        str(device_name)
        print(f"ok boss, I am turning {state[0]} {devices_name}")
        data = datas.get_device_details_by_devices_name(devices_name)
        device_type = data[0]['type']
        print("Device Type:", device_type)  
        if device_type == "fan":
            if speed:
                if speed_count:
                        print(f"ok boss, I am {state[0]} the {devices_name} {speed[0]} to {speed_count[0]} ")
                        for x in data:  
                            pid = x["product_id"]
                            topic = f"onwords/{pid}/status"
                            did = x["device_id"]
                            
                            if speed_count[0] == "low":
                                msg = {f"{did}": 1 if state[0] == "on" else (0 if state[0] == "off" else 1), 'speed': 1}
                                
                            elif speed_count[0] == "medium":
                                msg = {f"{did}": 1 if state[0] == "on" else (0 if state[0] == "off" else 1), 'speed': 3}

                            elif speed_count[0] == "high":
                                msg = {f"{did}": 1 if state[0] == "on" else (0 if state[0] == "off" else 1), 'speed': 5}
                            else:
                                msg = {f"{did}": 1 if state[0] == "on" else (0 if state[0] == "off" else 1), 'speed': int(speed_count[0])}

                            print(topic,msg)
                            
                            #mqtt.publish(topic,str(msg))
                    
                else:
                    print(f"ok boss, I am {state[0]} the {devices_name} speed-{speeds[0]} ")
                
                    for x in data:  
                        pid = x["product_id"]
                        topic = f"onwords/{pid}/status"
                        did = x["device_id"]
                        
                        msg = {f"{did}": 1 if state[0] == "on" else (0 if state[0] == "off" else "1"), 'speed': int(speeds[0])}

                        print(topic,msg)
                        
                        #mqtt.publish(topic,str(msg))
            else:
                print(f"ok boss, I am turning {state[0]} {devices_name}")

                for x in data:
                    pid = x["product_id"]
                    topic = f"onwords/{pid}/status"
                    did = x["device_id"]
                    msg = {f"{did}": 1 if state[0]=="on" else 0}

                    print(topic,msg)
                    
                    #mqtt.publish(topic,str(msg))
        
        else:

            for x in data:
                pid = x["product_id"]
                topic = f"onwords/{pid}/status"
                did = x["device_id"]
                msg = {f"{did}": 1 if state[0]=="on" else 0}

                print(topic,msg)
                
                #mqtt.publish(topic,str(msg))
        
    else:  
        if device:
            for dev in device:
                if dev in ['lights', 'light', 'bulb']:
                    device = "light"
                    print(f"ok boss, I am turning {state[0]} All Room's {device}")
                    data = datas.get_home_device_details_by_type_(device)
                    for x in data:
                        pid = x["product_id"]
                        topic = f"onwords/{pid}/status"
                        did = x["device_id"]
                        msg = {f"{did}": 1 if state[0]=="on" else 0}

                        print(topic,msg)
                        
                        #mqtt.publish(topic,str(msg))
                elif dev in ['fans', 'fan']:
                    device = "fan"
                    if speed:
                        if speed_count:
                                print(f"ok boss, I am {state[0]} the All room's {device} {speed[0]} to {speed_count[0]} ")
                                data = datas.get_home_device_details_by_type_(device)
                                
                                for x in data:
                                    
                                    pid = x["product_id"]
                                    topic = f"onwords/{pid}/status"
                                    did = x["device_id"]
                                    
                                    if speed_count[0] == "low":   
                                        msg = {f"{did}": 1 if state[0] == "on" else (0 if state[0] == "off" else 1), 'speed': 1}
                                        
                                    elif speed_count[0] == "medium": 
                                        msg = {f"{did}": 1 if state[0] == "on" else (0 if state[0] == "off" else 1), 'speed': 3}

                                    elif speed_count[0] == "high":  
                                        msg = {f"{did}": 1 if state[0] == "on" else (0 if state[0] == "off" else 1), 'speed': 5}
                                    else:
                                        msg = {f"{did}": 1 if state[0] == "on" else (0 if state[0] == "off" else 1), 'speed': int(speed_count[0])}

                                    print(topic,msg)
                                    
                                    #mqtt.publish(topic,str(msg))
                        else:
                            print(f"ok boss, I am {state[0]} the All room's {device} speed-{speeds[0]} ")
                            data = datas.get_home_device_details_by_type_(device)
                            
                            for x in data:
                                
                                pid = x["product_id"]
                                topic = f"onwords/{pid}/status"
                                did = x["device_id"]
                                
                                msg = {f"{did}": 1 if state[0] == "on" else (0 if state[0] == "off" else "1"), 'speed': int(speeds[0])}

                                print(topic,msg)
                                
                                #mqtt.publish(topic,str(msg))
                    
                            
                    else:
                        print(f"ok boss, I am turning {state[0]} All room's {device}")
                        data = datas.get_home_device_details_by_type_(device)
                        for x in data:
                            pid = x["product_id"]
                            topic = f"onwords/{pid}/status"
                            did = x["device_id"]
                            msg = {f"{did}": 1 if state[0] == "on" or state[0] == "start" else 0}

                            print(topic,msg)
                            
                            #mqtt.publish(topic,str(msg))
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






