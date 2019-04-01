# Automatic Chicken Coop Door Opener Beta 0.1

# Import Libraries
from tkinter import *
from tkinter import ttk 
#  import RPi.GPIO as GPIO
import time
import threading

door_Status_Var = ""
time_Open_Close = ""


# Defining Functions for turning Time Settings on and off

def time_Setting():
    if time_Open_Close.get() == 0:
        input_Open_Hour['state'] = DISABLED
        input_Open_Minute['state'] = DISABLED
        am_Open_Radiobutton['state'] = DISABLED
        pm_Open_Radiobutton['state'] = DISABLED
        input_Open_Label['fg'] ='gray'
        input_Close_Hour['state'] = DISABLED
        input_Close_Minute['state'] = DISABLED
        am_Close_Radiobutton['state'] = DISABLED
        pm_Close_Radiobutton['state'] = DISABLED
        input_Close_Label['fg'] ='gray'
        set_Open_Label.pack_forget() 
        set_Close_Label.pack_forget() 
        
    else:
        input_Open_Hour['state'] = NORMAL
        input_Open_Minute['state'] = NORMAL
        am_Open_Radiobutton['state'] = NORMAL
        pm_Open_Radiobutton['state'] = NORMAL
        input_Open_Label['fg'] ='black'
        input_Close_Hour['state'] = NORMAL
        input_Close_Minute['state'] = NORMAL
        am_Close_Radiobutton['state'] = NORMAL
        pm_Close_Radiobutton['state'] = NORMAL
        input_Close_Label['fg'] ='black'
        set_Open_Label.pack() 
        set_Close_Label.pack() 


   

# Defining Functions for Opening and Closing Coop door
def open_Coop():
    global door_Status_Var

    # Set buttons to DISABLE till operation ends
    open_Button['state'] = DISABLED
    close_Button['state'] = DISABLED

    # Show Door Progress Bar
    door_Progress.pack(pady=10)

    # Set Label variables to current status of Coop Door
    door_Status_Var.set("Opening Coop Door")
    label_Door_Status['fg'] = "red"

    # Start set_Open_Relay_On in new thread to avoid window lockup
    t_Open = threading.Thread(target=set_Open_Relay_On)
    t_Open.start()

def close_Coop():
    global door_Status_Var

    # Set buttons to DISABLE till operation ends
    open_Button['state'] = DISABLED
    close_Button['state'] = DISABLED

    # Set Label variables to current status of Coop Door
    door_Status_Var.set("Closing Coop Door")
    label_Door_Status['fg'] = "red"

    # Show Progress bar
    door_Progress.pack(pady=10)

    # Start set_Close_Relay_On in new thread to avoid window lockup
    t_Close = threading.Thread(target=set_Close_Relay_On)
    t_Close.start()

def set_Open_Relay_On():
    global door_Status_Var
    
    # 
    # GPIO.setmode(GPIO.BCM)

    # # init pin numbers
    # pin_Open = [6]

    # # set mode default state is 'low'
    # GPIO.setup(pin_Open, GPIO.OUT) 
   
    # # Activate Open Relay to High (High turns Relay on)
    # GPIO.output(pin_Open, GPIO.HIGH)     # Activate Open relay
    
    # Start Timer for duration actuator will be activated
    timer = 0
    bar_Status = 0
    while timer <= 50:
        timer = timer + .5
        bar_Status = bar_Status +1
        door_Progress['value'] = bar_Status
        time.sleep(.5)

    # set Open relay back to low (Turns Relay off)
    # GPIO.output(pin_Open, GPIO.LOW)

    # Reset GPIO settings
    # GPIO.cleanup()

    # Set Label Variables defining current state of Coop Door
    door_Status_Var.set("Coop Door is Open")
    label_Door_Status['fg'] = "green"
    status_Bar['text'] = "Coop Status = Open"

    # Turn Button Status back to NORMAL Operation
    open_Button['state'] = NORMAL
    close_Button['state'] = NORMAL

    # Hide Door Progress Bar
    door_Progress.pack_forget()

def set_Close_Relay_On():
    global door_Status_Var
    # 
    # GPIO.setmode(GPIO.BCM)

    # # # init pin numbers
    # pin_Close = [22]

    # # # set mode default state is 'low'
    # GPIO.setup(pin_Close, GPIO.OUT)
   
    # # # Activate Close Relay to High
    # GPIO.output(pin_Close, GPIO.HIGH)      # Activate Close relay

    # Start Timer for duration actuator will be activated
    timer = 0
    bar_Status = 0
    while timer <= 50:
        timer = timer + .5
        bar_Status = bar_Status + 1
        door_Progress['value'] = bar_Status
        time.sleep(.5)

    # set Close relay back to low (off)
    # GPIO.output(pin_Close, GPIO.LOW)

    # Reset GPIO settings
    # GPIO.cleanup()

    # Set Label variables defining the current state of Coop Door
    door_Status_Var.set("Coop Door is Closed")
    label_Door_Status['fg'] = "green"
    status_Bar['text'] = "Coop Status = Closed"

    # Turn Button Status back to NORMAL Operation
    open_Button['state'] = NORMAL
    close_Button['state'] = NORMAL

    # Hide Progress bar
    door_Progress.pack_forget()

# Main Window
window = Tk()
window.title("Automatic Chicken Coop Door")
window.geometry('350x400')
window.configure()


# Define Frames for Window
top_Frame = Frame(window)
top_Frame.pack(padx=15, pady=15)

middle_Upper_Frame = Frame(window)
middle_Upper_Frame.pack(padx=15, pady=15)

middle_Lower_Frame = Frame(window)
middle_Lower_Frame.pack(padx=15, pady=15)

bottom_Frame = Frame(window)
bottom_Frame.pack(padx=15, pady=15)

# define Door Status
door_Status_Var = StringVar()
var_Open_Am_Pm = StringVar()
var_Open_Am_Pm.set("AM")
var_Close_Am_Pm = StringVar()
var_Close_Am_Pm.set("PM")

#create header label
header_Label = Label (top_Frame, text="Choose Open or Close Coop", font="none 12 bold") 
header_Label.pack(pady=15)

#create Open and Close Buttons
open_Button = Button(top_Frame, text="Open Coop", width=10, command=open_Coop) 
open_Button.pack(side=LEFT, padx=15)
close_Button = Button(top_Frame, text="Close Coop", width=10, command=close_Coop) 
close_Button.pack(side=LEFT, padx=15)

# Door Status Label
label_Door_Status = Label (bottom_Frame, textvariable=door_Status_Var, font="none 14 bold", fg="red")
label_Door_Status.pack()

# Progress Bar Defined, but not turned on
door_Progress = ttk.Progressbar(bottom_Frame, orient=HORIZONTAL,length=100, mode='determinate')

# Setup Variable and Checkbox.  Checkbox to enable "open and close" time settings
time_Open_Close = IntVar()
time_Open_Close.set(0)
time_Check_Button = Checkbutton(middle_Upper_Frame, text="Choose to set operation times", \
    variable=time_Open_Close, command = time_Setting)
time_Check_Button.pack()

# Set Variables and default values for Open and Closing times.
var_Open_Hour = StringVar()
var_Open_Minute = StringVar()
var_Close_Hour = StringVar()
var_Close_Minute = StringVar()

var_Open_Hour.set("6")
var_Open_Minute.set("00")
var_Close_Hour.set("8")
var_Close_Minute.set("00")

# Setup Labels and receive time inputs for opening the Coop
input_Open_Label = Label(middle_Upper_Frame, text="Set time to open coop  ", font="none 12", fg="black")
input_Open_Label.pack(side=LEFT, pady=5)
input_Open_Hour = ttk.Spinbox(middle_Upper_Frame, from_ = "1", to= "12",textvariable = var_Open_Hour, \
     width=4, wrap=True) 
input_Open_Hour.pack(side=LEFT, pady=5)      
input_Open_Minute = ttk.Spinbox(middle_Upper_Frame, values= ["00", "15", "30", "45"], textvariable = var_Open_Minute, \
     width=4, wrap=True) 
input_Open_Minute.pack(side=LEFT, pady=5) 

am_Open_Radiobutton = ttk.Radiobutton(middle_Upper_Frame, variable=var_Open_Am_Pm, value="AM", text="AM") 
am_Open_Radiobutton.pack(side=TOP, padx=5)
pm_Open_Radiobutton = ttk.Radiobutton(middle_Upper_Frame, variable=var_Open_Am_Pm, value="PM", text="PM") 
pm_Open_Radiobutton.pack(side=BOTTOM, padx=5)

# Setup Labels and receive time inputs for opening the Coop
input_Close_Label = Label(middle_Lower_Frame, fg="black", text="Set time to Close coop  ", font="none 12")
input_Close_Label.pack(side=LEFT, pady=5)
input_Close_Hour = ttk.Spinbox(middle_Lower_Frame, from_ = "1", to= "12", textvariable = var_Close_Hour, \
    width=4, wrap=True) 
input_Close_Hour.pack(side=LEFT, pady=5)   
input_Close_Minute = ttk.Spinbox(middle_Lower_Frame, values= ["00", "15", "30", "45"], textvariable = var_Close_Minute, \
     width=4, wrap=True) 
input_Close_Minute.pack(side=LEFT, pady=5) 

am_Close_Radiobutton = ttk.Radiobutton(middle_Lower_Frame, variable=var_Close_Am_Pm, value="AM", text="AM") 
am_Close_Radiobutton.pack(side=TOP, padx=5)
pm_Close_Radiobutton = ttk.Radiobutton(middle_Lower_Frame, variable=var_Close_Am_Pm, value="PM", text="PM") 
pm_Close_Radiobutton.pack(side=BOTTOM, padx=5)

set_Open_Label = Label(bottom_Frame, text="The Coop will Open at ")
set_Open_Label.pack()        
set_Close_Label = Label(bottom_Frame, text="The Coop will Close at ")
set_Close_Label.pack()       

time_Setting()

# test_Time_Variable = Label (bottom_Frame, textvariable=time_Open_Close) .pack()

#create status bar
status_Bar = Label(window, text="Coop Status (unknown)", relief=SUNKEN, anchor=W)
status_Bar.pack(side=BOTTOM, fill=X)

# Run main loop
window.mainloop()
