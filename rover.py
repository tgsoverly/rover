from adafruit_motorkit import MotorKit
from picamera import PiCamera
from Hologram.HologramCloud import HologramCloud

from time import sleep
import time
import tkinter
import os


camera = PiCamera()

front_kit = MotorKit(address=0x60)
middle_kit = MotorKit(address=0x61)
rear_kit = MotorKit(address=0x62)

right_motors = [front_kit.motor1, middle_kit.motor1,rear_kit.motor1]
left_motors = [front_kit.motor3, middle_kit.motor3,rear_kit.motor3]

max_speed = 0.90

device_key = os.environ['HOLOGRAM_DEVICE_KEY']
hologram = HologramCloud({'devicekey': device_key}, network='cellular')
result = hologram.network.connect()
if result == False:
  print(' Failed to connect to cell network')

commands = []

def run_command():
  print("running command")
  received_commands = hologram.popReceivedMessage()
  commands.extend(received_commands.split())
  enter_pressed()

hologram.event.subscribe('message.received', run_command) 

def set_side_speed(side, speed):
    set_speed=speed
    motors=right_motors
    
    if side=='left':
        set_speed=-speed
        motors=left_motors

    for motor in motors:
        motor.throttle=set_speed
    
def forward():
    set_side_speed("left", max_speed)
    set_side_speed("right", max_speed)
    time.sleep(2.0)
    set_side_speed("left", 0)
    set_side_speed("right", 0)

def left():
    set_side_speed("left", -max_speed)
    set_side_speed("right", max_speed)
    time.sleep(1.0)
    set_side_speed("left", 0)
    set_side_speed("right", 0)

def reverse():
    set_side_speed("left", -max_speed)
    set_side_speed("right", -max_speed)
    time.sleep(2.0)
    set_side_speed("left", 0)
    set_side_speed("right", 0)

def right():
    set_side_speed("left", max_speed)
    set_side_speed("right", -max_speed)
    time.sleep(1.0)
    set_side_speed("left", 0)
    set_side_speed("right", 0)

def picture():
    camera.start_preview()
    sleep(5)
    camera.capture('/home/pi/Desktop/image.jpg')
    camera.stop_preview()


def forward_pressed():
    commands.append("forward")

def reverse_pressed():
    commands.append("reverse")
    
def left_pressed():
    commands.append("left")

def right_pressed():
    commands.append("right")

def picture_pressed():
    commands.append("picture")

def enter_pressed():
    print(commands)
    for command in commands:
        if command=="forward" or command=='f':
            forward()
        if command=="reverse" or command=='b':
            reverse()
        if command=="left" or command=='l':
            left()
        if command=="right" or command=='r':
            right()
        if  command=="picture" or command=='p':
            picture()  
    commands.clear()

window = tkinter.Tk()
window.title("GUI")

button_height=2
button_width=15

b1 = tkinter.Button(window, text = "forward", command = forward_pressed, height= button_height,width=button_width)
b1.grid(row=0, column=1)

b2 = tkinter.Button(window, text = "reverse", command = reverse_pressed, height= button_height,width=button_width)
b2.grid(row=2, column=1)

b3=tkinter.Button(window, text = "left", command = left_pressed, height= button_height,width=button_width)
b3.grid(row=1, column=0)

b4=tkinter.Button(window, text = "right", command = right_pressed, height= button_height,width=button_width)
b4.grid(row=1, column=2)

b5=tkinter.Button(window, text = "enter", command = enter_pressed, height= button_height,width=button_width)
b5.grid(row=1, column=1)

b6=tkinter.Button(window, text = "picture", command = picture_pressed, height= button_height,width=button_width)
b6.grid(row=0, column=0)

window.mainloop()
