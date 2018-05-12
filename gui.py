import socket
import select
import sys
import json

import threading

from Tkinter import *
import RPi.GPIO as GPIO
import time

#GUI

GPIO.setmode(GPIO.BCM)

pir = 21

GPIO.setup(pir,GPIO.IN)

d=open("password.txt", 'w')

class Password(object):
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.passWord = StringVar()
        f = open("password.txt", 'r')
        self.passWord.set(f.readline())
        self.text = StringVar()
        self.text.set("SET PASSWORD: ")
        label = Label(frame, textvariable=self.text)
        label.grid(row = 0)
        entry = Entry(frame, textvariable=self.passWord)
        entry.grid(row=0, column=1)
        self.button = Button(frame, text="Confirm", command=self.Confirm)
        self.button.grid(row = 0, column =3)
    def Confirm(self):
        d=open("password.txt", 'w')
        d.write(self.passWord.get())

#relays 1 and 2 are reserved for security sistem
#1 is buzzer
#2 is led

class ArmButton(object):
    def __init__(self, textbutton, master, status=False, toggleState=False, relays=[1, 2]):
        frame = Frame(master)
        frame.pack()
        self.status = {True: "STATUS: ON",
                       False: "STATUS: OFF"}
        self.toggleState = toggleState
        self.button = Button(frame, text=textbutton, command = clt.send_command({"button1": not self.toggleStatus,
                                                                                 "button2": RL[1].deviceStatus,
                                                                                 "button3": RL[2].deviceStatus,
                                                                                 "button4": RL[3].deviceStatus,
                                                                                 "button5": RL[4].deviceStatus,
                                                                                 "button6": RL[5].deviceStatus,}))
        self.button.grid(row = 2)
        self.text = StringVar()
        self.text.set(self.status[self.toggleState])
        self.label = Label(frame, textvariable = self.text)
        self.label.grid(row = 2, column = 1)

    '''
    def toggle(self):
        print 1
        self.toggleState = not self.toggleState
        self.text.set(self.status[self.toggleState])
        if self.toggleState:
            print 2
            my_thread = threading.Thread(target=self.startem,args=())
            my_thread.start()

    def sensor(self):
        print 3
        time.sleep(2)
        while 1:
            
            if GPIO.input(pir):
                print 4
                return True
                
            if self.toggleState==False:
                return False

    def startem(self):
        if self.sensor()==True:
            RELAY.relayON(0, 2)
            RELAY.relayON(0, 1)
            time.sleep(5)
            RELAY.relayOFF(0, 2)
            RELAY.relayOFF(0, 1)
        else:
            pass
    '''
    
class GuiButton(object):
    def __init__(self, relay, textbutton, master,  status = False):
        frame = Frame(master)
        frame.pack()
        self.relay = relay
        self.status = {True: "STATUS: ON",
                       False: "STATUS: OFF"}
        self.deviceStatus = status
        self.text = StringVar()
        self.text.set(self.status[self.deviceStatus])
        self.button = Button(frame, text=textbutton, command = self.send)
        self.button.grid(row = relay+1)
        self.label = Label(frame, textvariable = self.text)
        self.label.grid(row = relay+1, column = 1)
    '''
    def toggle(self):
        RELAY.relayTOGGLE(0, self.relay)
        self.deviceStatus = not self.deviceStatus
        self.text.set(self.status[self.deviceStatus])
    '''
    def send(self):
        clt.send_command({"button1": RL[0].toggleStatus,
                            "button2": if self.relay==2 not RL[1].deviceStatus else RL[1].deviceStatus,
                            "button3": if self.relay==3 not RL[2].deviceStatus else RL[2].deviceStatus,
                            "button4": if self.relay==4 not RL[3].deviceStatus else RL[3].deviceStatus,
                            "button5": if self.relay==5 not RL[4].deviceStatus else RL[4].deviceStatus,
                            "button6": if self.relay==6 not RL[5].deviceStatus else RL[5].deviceStatus,})


class Relay(object):
    def __init__(self, relayNum, root):
        
        self.relays=[]
        self.relays.append(ArmButton("Alarm", root))
        for i in range(3, 8):
            self.relays.append(GuiButton(i, 'Relay '+str(i), root))

#Client

class Client(object):
    
    MAX_RECV_BYTES = 1024

    def __init__(self, server_address):
        self.clien_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ""
        try:
            self.client_socket.connect(server_address)
        except socket.error as serr:
            print ""
            sys.exit(1)
        else:
            print""
        self.inputs = [ sys.stdin , self.client_socket ]

    def send_command(self, command):
        try:
            self.client_socket.send(json.dumps(command))
        except IOError as ierr:
            print""
            sys.exit(1)

    def recv_status(self, sock):
        try:
            recv_status = sock.recv(Client.MAX_RECV_BYTES)
        except IOError as ierr:
            sys.exit(1)
        else:
            return json.loads(recv_status)

    def connect_forever(self):
        while 1:
            try:
                readable, writeable, exception = select.select(self.inputs, [], [])
                for sock in readable:
                    if sock == self.client_socket:
                        status = self.recv_status(sock)
                        RL[1].toggleStatus = status["button1"]
                        for i in range(2,7):
                            RL[i].deviceStatus = status["button"+str(i)]
            except KeyboardInterrupt as kerr:
                self.client_socket.close()
                sys.exit(0)

clt = Client(())
client_thread = threading.Thread(target=clt.connect_forever,args=())


root = Tk()
root.attributes('-fullscreen', True)
p = Password(root)
RL = Relay(7, root)

root.mainloop()
