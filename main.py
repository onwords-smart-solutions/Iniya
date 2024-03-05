import iniya

while 1:
    command = input("Enter the command : ")
    # command = "turn on the lights"
    iniya.process_command(command)
    # input()