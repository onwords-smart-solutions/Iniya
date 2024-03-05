import f
import word_db
from smart_home import smart_home

@f.time_decorator
def process_command(command):
    uid = "3BoUcBC6ARWdtXfPHQstFaIPzum1"
    command = command.lower()
    command_words  = command.split()
    bigrams_command_words = f.generate_bigrams(command)

    print(f"Bigrams = {bigrams_command_words}")

    control_words = [word for word in command_words if word in word_db.controll_words]


    # print(control_words)
    # print(device_words)

    if control_words:
        smart_home(uid="3BoUcBC6ARWdtXfPHQstFaIPzum1",command=command_words,bigrams_command=bigrams_command_words)

    else:
        pass



