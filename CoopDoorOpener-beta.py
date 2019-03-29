# Automatic Chicken Coop Door Opener Beta 0.1

# Import Tkinter Libraries
from tkinter import *
import RPi.GPIO as GPIO
import time
import threading

door_Status_Var = ""

# Defining Functions for Opening and Closing Coop door
def open_Coop():
    global door_Status_Var

    # Set Label variables to current status of Coop Door
    door_Status_Var.set("Opening Coop Door")
    label_Door_Status['fg'] = "red"

    # Start set_Open_Relay_On in new thread to avoid window lockup
    t1 = threading.Thread(target=set_Open_Relay_On)
    t1.start()

def close_Coop():
    global door_Status_Var

    # Set Label variables to current status of Coop Door
    door_Status_Var.set("Closing Coop Door")
    label_Door_Status['fg'] = "red"

    # Start set_Close_Relay_On in new thread to avoid window lockup
    t1 = threading.Thread(target=set_Close_Relay_On)
    t1.start()

def set_Open_Relay_On():
    global door_Status_Var
    
    # 
    GPIO.setmode(GPIO.BCM)

    # init pin numbers
    pin_Open = [6]
    pin_Close = [22]

    # set mode default state is 'low'
    GPIO.setup(pin_Open, GPIO.OUT) 
    GPIO.setup(pin_Close, GPIO.OUT)
   
    # Activate Close Relay to Low and Open Relay to High (High turns Relay on)
    GPIO.output(pin_Close, GPIO.LOW)     # Turn off Close Relay
    time.sleep(2)                        # This insures close relay is off before turning on Open relay
    GPIO.output(pin_Open, GPIO.HIGH)      # Activate Open relay
    
    # Start Timer for duration actuator will be activated
    timer = 0
    while timer <= 10:
        timer = timer + 1
        time.sleep(1)

    # set Open relay back to low (Turns Relay off)
    GPIO.output(pin_Open, GPIO.LOW)

    # Reset GPIO settings
    GPIO.cleanup()

    # Set Label Variables defining current state of Coop Door
    door_Status_Var.set("Coop Door is Open")
    label_Door_Status['fg'] = "green"
    statusbar['text'] = "Coop Status = Open"

def set_Close_Relay_On():
    global door_Status_Var
    # 
    GPIO.setmode(GPIO.BCM)

    # # init pin numbers
    pin_Open = [6]
    pin_Close = [22]

    # # set mode default state is 'low'
    GPIO.setup(pin_Open, GPIO.OUT) 
    GPIO.setup(pin_Close, GPIO.OUT)
   
    # # Activate Relay to High
    GPIO.output(pin_Open, GPIO.LOW)        # Turn off Open Relay
    time.sleep(2)                          # This insures Open relay is off before turning on Close relay
    GPIO.output(pin_Close, GPIO.HIGH)      # Activate Close relay

    # Start Timer for duration actuator will be activated
    timer = 0
    while timer <= 10:
        timer = timer + 1
        time.sleep(1)

    # set Close relay back to low (off)
    GPIO.output(pin_Close, GPIO.LOW)

    # Reset GPIO settings
    GPIO.cleanup()

    # Set Label variables defining the current state of Coop Door
    door_Status_Var.set("Coop Door is Closed")
    label_Door_Status['fg'] = "green"
    statusbar['text'] = "Coop Status = Closed"

# Main Window
window = Tk()
window.title("Automatic Chicken Coop Door")
window.iconbitmap(r'WiFiChicken.ico')
window.geometry('350x350')
window.configure()

# Define Frames for Window
top_Frame = Frame(window)
top_Frame.pack(padx=15, pady=15)

middle_Frame = Frame(window)
middle_Frame.pack(padx=15, pady=15)

# define Door Status
door_Status_Var = StringVar()

#create header label
header_Label = Label (top_Frame, text="Choose Open or Close Coop", font="none 12 bold") 
header_Label.pack(pady=15)

#create Open and Close Buttons
openButton = Button(middle_Frame, text="Open Coop", width=10, command=open_Coop) 
openButton.pack(side=LEFT, padx=15)
closeButton = Button(middle_Frame, text="Close Coop", width=10, command=close_Coop) 
closeButton.pack(side=LEFT, padx=15)

# Door Status Label
label_Door_Status = Label (window, textvariable=door_Status_Var, font="none 14 bold", fg="red")
label_Door_Status.pack()

#create status bar
statusbar = Label(window, text="Coop Status (unknown)", relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

# Run main loop
window.mainloop()
