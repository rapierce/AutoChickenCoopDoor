# Automatic Chicken Coop Door Opener Beta 0.1

# Import Libraries
from tkinter import *
from tkinter import ttk 
#  import RPi.GPIO as GPIO
import time
import threading
from datetime import datetime

door_Status_Var = ""
time_Open_Close = ""
current_Time = (datetime.now().strftime('%I:%M:%S %p'))


# Defining Functions for turning Time Settings on and off

def enable_Disable_Time_Setting():
    if time_Open_Close.get() == 0:
        disable_Time_Functions()
    else:
        enable_Time_Functions()

def disable_Time_Functions():
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
    apply_Time_Button['state'] = DISABLED
    
    if time_Open_Close.get() == 0:
        change_Time_Button['state'] = DISABLED
        set_Open_Label.pack_forget() 
        set_Close_Label.pack_forget() 
        set_Open_Time_Label.pack_forget()
        set_Close_Time_Label.pack_forget()
    

def enable_Time_Functions():
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
    change_Time_Button['state'] = NORMAL
    apply_Time_Button['state'] = NORMAL
    set_Open_Label.pack(side=LEFT) 
    set_Close_Label.pack(side=LEFT) 
    set_Open_Time_Label.pack(side=LEFT)
    set_Close_Time_Label.pack(side=LEFT)

def format_Time():
    var_Time_Format = ":"
    open_Hour = var_Open_Hour.get()
    open_Minute = var_Open_Minute.get()
    open_AM_PM = var_Open_Am_Pm.get()
    time_Open_String_Concat = open_Hour + var_Time_Format + open_Minute + open_AM_PM
    parsed_Open_Time = datetime.strptime(time_Open_String_Concat, '%I:%M%p')
    formatted_Open_Time.set(datetime.strftime(parsed_Open_Time, '%I:%M%p'))

    close_Hour = var_Close_Hour.get()
    close_Minute = var_Close_Minute.get()
    close_AM_PM = var_Close_Am_Pm.get()
    time_Close_String_Concat = close_Hour + var_Time_Format + close_Minute + close_AM_PM
    parsed_Close_Time = datetime.strptime(time_Close_String_Concat, '%I:%M%p')
    formatted_Close_Time.set(datetime.strftime(parsed_Close_Time, '%I:%M%p'))

    disable_Time_Functions()


   

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
window.geometry('350x450')
window.configure()


# Define Frames for Window
main_Frame1 = Frame(window)
main_Frame1.pack(padx=10, pady=5)

main_Frame2 = Frame(window)
main_Frame2.pack(padx=10, pady=5)

main_Frame3 = Frame(window)
main_Frame3.pack(padx=10, pady=5)

main_Frame4 = Frame(window)
main_Frame4.pack(padx=10, pady=5)

main_Frame5 = Frame(window)
main_Frame5.pack(padx=10, pady=5)

main_Frame6 = Frame(window)
main_Frame6.pack(padx=10, pady=5)

main_Frame7 = Frame(window)
main_Frame7.pack(padx=10, pady=5)

main_Frame8 = Frame(window)
main_Frame8.pack(padx=10, pady=5)

main_Frame9 = Frame(window)
main_Frame9.pack(padx=10, pady=5)

main_Frame10 = Frame(window)
main_Frame10.pack(padx=10, pady=5)


# Define Variables
# Door Status Variable
door_Status_Var = StringVar()

# Set Variable for Open/Close Time Checkbox
time_Open_Close = IntVar()
time_Open_Close.set(0)

# Set Variables for Open/Close Time Settings
var_Open_Hour = StringVar()
var_Open_Minute = StringVar()
var_Close_Hour = StringVar()
var_Close_Minute = StringVar()
formatted_Open_Time = StringVar()
formatted_Close_Time = StringVar()
var_Open_Hour.set("6")
var_Open_Minute.set("00")
var_Close_Hour.set("8")
var_Close_Minute.set("00")

# Set Variables for AM/PM Radio Buttons
var_Open_Am_Pm = StringVar()
var_Close_Am_Pm = StringVar()
var_Open_Am_Pm.set("AM")
var_Close_Am_Pm.set("PM")

#create header label
header_Label = Label (main_Frame1, text="Choose Open or Close Coop", font="none 12 bold") 
header_Label.pack(pady=15)

#create Open and Close Buttons
open_Button = Button(main_Frame1, text="Open Coop", width=10, command=open_Coop) 
open_Button.pack(side=LEFT, padx=15)
close_Button = Button(main_Frame1, text="Close Coop", width=10, command=close_Coop) 
close_Button.pack(side=LEFT, padx=15)

# Setup Variable and Checkbox.  Checkbox to enable "open and close" time settings
time_Check_Button = Checkbutton(main_Frame3, variable=time_Open_Close, command = enable_Disable_Time_Setting)
time_Check_Label = Label(main_Frame3, text = "Click to set time Operation")
time_Check_Button.pack(side=LEFT)
time_Check_Label.pack(side=LEFT)

# Setup Labels, Spinbox, and Radio Buttons to receive time inputs for opening the Coop
input_Open_Label = Label(main_Frame4, text="Set time to open coop ", font="none 12", fg="black")
input_Open_Label.pack(side=LEFT, ipadx=3, pady=5)
input_Open_Hour = ttk.Spinbox(main_Frame4, from_ = "1", to= "12",textvariable = var_Open_Hour, \
     width=4, wrap=True) 
input_Open_Hour.pack(side=LEFT, pady=5)      
input_Open_Minute = ttk.Spinbox(main_Frame4, from_=00, to=59, format="%02.0f", textvariable = var_Open_Minute, \
     width=4, wrap=True) 
input_Open_Minute.pack(side=LEFT, pady=5) 

am_Open_Radiobutton = ttk.Radiobutton(main_Frame4, variable=var_Open_Am_Pm, value="AM", text="AM") 
am_Open_Radiobutton.pack(side=TOP, padx=5)
pm_Open_Radiobutton = ttk.Radiobutton(main_Frame4, variable=var_Open_Am_Pm, value="PM", text="PM") 
pm_Open_Radiobutton.pack(side=BOTTOM, padx=5)

# Setup Labels, Spinbox, and Radio Buttons to receive time inputs for closing the Coop
input_Close_Label = Label(main_Frame5, fg="black", text="Set time to Close coop ", font="none 12")
input_Close_Label.pack(side=LEFT, pady=5)
input_Close_Hour = ttk.Spinbox(main_Frame5, from_ = "1", to= "12", textvariable = var_Close_Hour, \
    width=4, wrap=True) 
input_Close_Hour.pack(side=LEFT, pady=5)   
input_Close_Minute = ttk.Spinbox(main_Frame5, from_=00, to=59, format="%02.0f", textvariable = var_Close_Minute, \
     width=4, wrap=True) 
input_Close_Minute.pack(side=LEFT, pady=5) 

am_Close_Radiobutton = ttk.Radiobutton(main_Frame5, variable=var_Close_Am_Pm, value="AM", text="AM") 
am_Close_Radiobutton.pack(side=TOP, padx=5)
pm_Close_Radiobutton = ttk.Radiobutton(main_Frame5, variable=var_Close_Am_Pm, value="PM", text="PM") 
pm_Close_Radiobutton.pack(side=BOTTOM, padx=5)

change_Time_Button = Button(main_Frame6, text="Set Times", width=10, command=enable_Disable_Time_Setting) 
change_Time_Button.pack(side=LEFT, padx=15)
apply_Time_Button = Button(main_Frame6, text="Apply", width=10, command=format_Time) 
apply_Time_Button.pack(side=LEFT, padx=15)

# Set Labels for time set and countdown timer for next Open/Close Operation
set_Open_Label = Label(main_Frame7, text="The Coop will Open at ")
set_Open_Time_Label = Label(main_Frame7, textvariable = formatted_Open_Time)              
set_Close_Label = Label(main_Frame8, text="The Coop will Close at ")      
set_Close_Time_Label = Label(main_Frame8, textvariable = formatted_Close_Time)

# Door Status Label
label_Door_Status = Label (main_Frame10, textvariable=door_Status_Var, font="none 14 bold", fg="red")
label_Door_Status.pack()

# Progress Bar Defined, but not turned on
door_Progress = ttk.Progressbar(main_Frame10, orient=HORIZONTAL,length=100, mode='determinate')

# Call time_Setting function to enable or disable time settings operation
enable_Disable_Time_Setting()

#create status bar
status_Bar = Label(window, text="Coop Status = Unknown", relief=SUNKEN, anchor=W)
status_Bar.pack(side=BOTTOM, fill=X)

print (current_Time)

# Run main loop
window.mainloop()
