import word_db, f
from smart_home import smart_home

def process_command(command,uid):
    command = command.lower()
    command_words  = command.split()
    bigrams_command_words = f.generate_bigrams(command)
    control_words = [word for word in command_words if word in word_db.controll_words]
    if control_words:
        smart_home(uid,command=command_words,bigrams_command=bigrams_command_words)
    else:
        pass