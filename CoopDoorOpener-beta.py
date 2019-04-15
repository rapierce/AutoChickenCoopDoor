# Automatic Chicken Coop Door Opener Beta 0.1

# Import Libraries
from tkinter import *
from tkinter import ttk 
# import RPi.GPIO as GPIO
import time
import threading
from datetime import datetime

# Setting Global Variables
door_Status_Var = ""
time_Open_Close = ""
timer_Thread_Switch = True
open_Coop_Check_Switch = True
door_In_Operation = False
first_Time_Run = True


# Defining Functions

# Retrieves and returns current time
def get_Current_Time():
    curr_Time = datetime.now()
    return curr_Time

# Enables or Disables Time functions when checkbox is clicked or unclicked
def enable_Disable_Time_Setting():
    global timer_Thread_Switch
    global door_In_Operation
    timer_Thread_Switch = False
    if time_Open_Close.get() == 0 or door_In_Operation == True:
        disable_Time_Functions()
    else:
        enable_Time_Functions()

# Sets time_Thread_Switch variable to true and starts the Open/Close timers
def set_Timer_Thread():
    global timer_Thread_Switch
    timer_Thread_Switch = True
    timer_Thread = threading.Thread(target=format_Time)
    timer_Thread.daemon = True
    timer_Thread.start()

# Disables Timer Function when timer Checkbox isn't clicked and after setting times
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
    change_Time_Button.pack()
    apply_Time_Button.pack_forget()
    
    if time_Open_Close.get() == 0:
        change_Time_Button.pack_forget()
        set_Open_Label.pack_forget() 
        set_Close_Label.pack_forget() 
        set_Open_Time_Label.pack_forget()
        set_Close_Time_Label.pack_forget()
        door_Schedule_Off_Label.pack_forget()
        set_Countdown_Label.pack_forget()
    

# Enables timer settings to set times for Open/Close
def enable_Time_Functions():
    change_Time_Button.pack_forget()
    apply_Time_Button.pack()
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

# This function runs if the manual Open/Close buttons are selected and the Coop door is off it's schedule
#    if the door doesn't manually get swtiched back to the schedule, the door will ignore it's next scheduled operation 
#       and continue normal schedule.
def coop_Check_Switch_Loop(clos_Time, op_Time):
    global open_Coop_Check_Switch
    global door_In_Operation
    global timer_Thread_Switch
    door_Schedule_Off_Label.pack_forget()
    set_Countdown_Label.pack_forget()
    total_Seconds = 1

    while door_In_Operation == True:
        pass
    if timer_Thread_Switch == True and open_Coop_Check_Switch == False:
        while timer_Thread_Switch == True and open_Coop_Check_Switch == False and total_Seconds !=0:
            label_Door_Status['fg'] = 'red'
            schedule_Off_Var.set('Open Coop to continue schedule')
            door_Schedule_Off_Label.pack()


            current_Time = get_Current_Time()
            calc_Close_Time = clos_Time - current_Time

            total_Seconds = calc_Close_Time.seconds
            calc_Hours, remainder = divmod(total_Seconds, 3600)
            calc_Minutes, calc_Seconds = divmod(remainder, 60)

            formatted_Calc_Time.set('Normal Operations will resume in {0:02}:{1:02}:{2:02}'.format(calc_Hours, calc_Minutes, calc_Seconds))
            set_Countdown_Label.pack()

            time.sleep(.5)
            door_Schedule_Off_Label.pack_forget()
            time.sleep(.5)

    elif timer_Thread_Switch == True and open_Coop_Check_Switch == True:
        while open_Coop_Check_Switch == True and timer_Thread_Switch == True and total_Seconds !=0:
            label_Door_Status['fg'] = 'red'
            schedule_Off_Var.set('Close Coop to continue schedule')
            door_Schedule_Off_Label.pack()

            current_Time = get_Current_Time()
            calc_Close_Time = op_Time - current_Time

            total_Seconds = calc_Close_Time.seconds
            calc_Hours, remainder = divmod(total_Seconds, 3600)
            calc_Minutes, calc_Seconds = divmod(remainder, 60)

            formatted_Calc_Time.set('Normal Operations will resume in {0:02}:{1:02}:{2:02}'.format(calc_Hours, calc_Minutes, calc_Seconds))
            set_Countdown_Label.pack()

            time.sleep(.5)
            door_Schedule_Off_Label.pack_forget()
            time.sleep(.5)

    set_Countdown_Label.pack_forget()
    enable_Disable_Time_Setting()

#  Format time function sets all the time formats and runs the scheduled operation at on it's time schedule
def format_Time():
    global timer_Thread_Switch
    global open_Coop_Check_Switch
    global door_In_Operation
    disable_Time_Functions()
    current_Time = get_Current_Time()

    # Pull variables from Open/Close timeset spinbox
    open_Hour = var_Open_Hour.get()
    open_Minute = var_Open_Minute.get()
    open_AM_PM = var_Open_Am_Pm.get()
    close_Hour = var_Close_Hour.get()
    close_Minute = var_Close_Minute.get()
    close_AM_PM = var_Close_Am_Pm.get()
    var_Second = "00" # Added for seconds
    total_Seconds = 1
    
    # Formatting variables received from Open/Close time set spinbox
    time_String_Open_Concat = open_Hour + open_Minute + var_Second + open_AM_PM
    time_String_Close_Concat = close_Hour + close_Minute + var_Second + close_AM_PM
    parsed_Open_Time = datetime.strptime(time_String_Open_Concat, '%I%M%S%p')
    parsed_Close_Time = datetime.strptime(time_String_Close_Concat, '%I%M%S%p')
    formatted_Open_Time = datetime.strftime(parsed_Open_Time, '%H:%M:%S')
    open_Time_Twelve_Hour.set(datetime.strftime(parsed_Open_Time, '%I:%M:%S%p'))
    formatted_Close_Time = datetime.strftime(parsed_Close_Time, '%H:%M:%S')
    close_Time_Twelve_Hour.set(datetime.strftime(parsed_Close_Time, '%I:%M:%S%p'))
    formatted_Current_Time = datetime.strftime(current_Time, '%H:%M:%S')

    while door_In_Operation == True:
        pass

    if formatted_Current_Time < formatted_Close_Time and formatted_Current_Time > formatted_Open_Time \
        or formatted_Current_Time > formatted_Close_Time and formatted_Close_Time < formatted_Open_Time \
            and formatted_Current_Time > formatted_Open_Time or formatted_Current_Time < formatted_Close_Time \
                and formatted_Close_Time < formatted_Open_Time:

        if timer_Thread_Switch == True and open_Coop_Check_Switch == False:
            coop_Timer_Loop_Thread = threading.Thread(target=coop_Check_Switch_Loop(parsed_Close_Time, parsed_Open_Time))
            coop_Timer_Loop_Thread.daemon = True
            coop_Timer_Loop_Thread.start()
        else:    
            while total_Seconds != 0 and timer_Thread_Switch == True and open_Coop_Check_Switch == True:
                door_Schedule_Off_Label.pack_forget()
                current_Time = get_Current_Time()
                calc_Close_Time = parsed_Close_Time - current_Time
                formatted_Current_Time = datetime.strftime(current_Time, '%H:%M:%S')

                total_Seconds = calc_Close_Time.seconds
                calc_Hours, remainder = divmod(total_Seconds, 3600)
                calc_Minutes, calc_Seconds = divmod(remainder, 60)

                formatted_Calc_Time.set('Time till Close {0:02}:{1:02}:{2:02}'.format(calc_Hours, calc_Minutes, calc_Seconds))
                set_Countdown_Label.pack()

                time.sleep(1)

            if timer_Thread_Switch == True and open_Coop_Check_Switch == True:
                close_Coop()
            elif timer_Thread_Switch == True and open_Coop_Check_Switch == False:
                set_Countdown_Label.pack_forget()
                coop_Timer_Loop_Thread = threading.Thread(target=coop_Check_Switch_Loop(parsed_Close_Time, parsed_Open_Time))
                coop_Timer_Loop_Thread.daemon = True
                coop_Timer_Loop_Thread.start()

    else:
        if timer_Thread_Switch == True and open_Coop_Check_Switch == True:
            coop_Timer_Loop_Thread = threading.Thread(target=coop_Check_Switch_Loop(parsed_Close_Time, parsed_Open_Time))
            coop_Timer_Loop_Thread.daemon = True
            coop_Timer_Loop_Thread.start()
        else:
            while total_Seconds != 0 and timer_Thread_Switch == True and open_Coop_Check_Switch == False:
                door_Schedule_Off_Label.pack_forget()
                current_Time = get_Current_Time()
                calc_Open_Time = parsed_Open_Time - current_Time
                formatted_Current_Time = datetime.strftime(current_Time, '%H:%M:%S')

                total_Seconds = calc_Open_Time.seconds
                calc_Hours, remainder = divmod(total_Seconds, 3600)
                calc_Minutes, calc_Seconds = divmod(remainder, 60)

                formatted_Calc_Time.set('Time till Open {0:02}:{1:02}:{2:02}'.format(calc_Hours, calc_Minutes, calc_Seconds))
                set_Countdown_Label.pack()

                time.sleep(1)

            if timer_Thread_Switch == True and open_Coop_Check_Switch == False:
                open_Coop()
            elif timer_Thread_Switch == True and open_Coop_Check_Switch == True:
                set_Countdown_Label.pack_forget()
                coop_Timer_Loop_Thread = threading.Thread(target=coop_Check_Switch_Loop(parsed_Close_Time, parsed_Open_Time))
                coop_Timer_Loop_Thread.daemon = True
                coop_Timer_Loop_Thread.start()

# Defining Functions for Opening and Closing Coop door
def open_Coop():
    global door_Status_Var
    global open_Coop_Check_Switch
    global door_In_Operation
    global first_Time_Run
    open_Coop_Check_Switch = True
    door_In_Operation = True

    # Set buttons to DISABLE till operation ends
    open_Button['state'] = DISABLED
    close_Button['state'] = DISABLED

    # Show Door Progress Bar
    door_Progress.pack(pady=10)

    # Set Label variables to current status of Coop Door
    if first_Time_Run == True:
        door_Status_Var.set('Calibrating Coop Door')
    else:
        door_Status_Var.set("Opening Coop Door")
    label_Door_Status['fg'] = "red"
    set_Countdown_Label.pack_forget()
    door_Schedule_Off_Label.pack_forget()

    # Start set_Open_Relay_On in new thread to avoid window lockup
    t_Open = threading.Thread(target=set_Open_Relay_On)
    t_Open.start()

def close_Coop():
    global door_Status_Var
    global open_Coop_Check_Switch
    global door_In_Operation
    open_Coop_Check_Switch = False
    door_In_Operation = True

    # Set buttons to DISABLE till operation ends
    open_Button['state'] = DISABLED
    close_Button['state'] = DISABLED

    # Set Label variables to current status of Coop Door
    door_Status_Var.set("Closing Coop Door")
    label_Door_Status['fg'] = "red"
    set_Countdown_Label.pack_forget()
    door_Schedule_Off_Label.pack_forget()

    # Show Progress bar
    door_Progress.pack(pady=10)

    # Start set_Close_Relay_On in new thread to avoid window lockup
    t_Close = threading.Thread(target=set_Close_Relay_On)
    t_Close.start()

# Function to open coop door
def set_Open_Relay_On():
    global door_Status_Var
    global door_In_Operation
    global first_Time_Run
    
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
    while timer <= 5:
        timer = timer + 1
        bar_Status = bar_Status +1
        door_Progress['value'] = bar_Status
        time.sleep(1)

    # set Open relay back to low (Turns Relay off)
    # GPIO.output(pin_Open, GPIO.LOW)

    # Reset GPIO settings
    # GPIO.cleanup()

    # Set Label Variables defining current state of Coop Door
    door_Status_Var.set("Coop Door is Open")
    label_Door_Status['fg'] = "green"
    status_Bar['text'] = "Coop Status = Open"

    # Turn Button Status back to NORMAL Operation
    open_Button['state'] = DISABLED
    close_Button['state'] = NORMAL

    # Hide Door Progress Bar
    door_Progress.pack_forget()

    # Set door in operation variable to False
    door_In_Operation = False
    first_Time_Run = False

    if time_Open_Close.get() == 1:
        set_Timer_Thread()

# Function to close coop door
def set_Close_Relay_On():
    global door_Status_Var
    global door_In_Operation
    
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
    while timer <= 5:
        timer = timer + 1
        bar_Status = bar_Status + 1
        door_Progress['value'] = bar_Status
        time.sleep(1)

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
    close_Button['state'] = DISABLED

    # Hide Progress bar
    door_Progress.pack_forget()

    # Set door_In_Operation variable to false
    door_In_Operation = False
    
    if time_Open_Close.get() == 1:
        set_Timer_Thread()



# Main Window
window = Tk()
window.title("Automatic Chicken Coop Door")
window.geometry('400x525')
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

main_Frame11 = Frame(window)
main_Frame11.pack(padx=10, pady=5)

# Define Variables
# Door Status Variable
door_Status_Var = StringVar()
schedule_Off_Var = StringVar()

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
open_Time_Twelve_Hour = StringVar()
close_Time_Twelve_Hour = StringVar()
formatted_Calc_Time = StringVar()

# Default variable settins
var_Open_Hour.set('06')
var_Open_Minute.set('00')
var_Close_Hour.set('08')
var_Close_Minute.set('00')

# Set Variables for AM/PM Radio Buttons
var_Open_Am_Pm = StringVar()
var_Close_Am_Pm = StringVar()
var_Open_Am_Pm.set('AM')
var_Close_Am_Pm.set('PM')

#create header label
header_Label = Label (main_Frame1, text='Choose Open or Close Coop', font='none 12 bold') 
header_Label.pack(pady=15)

#create Open and Close Buttons
open_Button = Button(main_Frame1, text='Open Coop', width=10, command=open_Coop) 
open_Button.pack(side=LEFT, padx=15)
close_Button = Button(main_Frame1, text='Close Coop', width=10, command=close_Coop) 
close_Button.pack(side=LEFT, padx=15)

# Setup Variable and Checkbox.  Checkbox to enable "open and close" time settings
time_Check_Button = Checkbutton(main_Frame3, text = 'Click to set time Operation', variable=time_Open_Close, \
    command = enable_Disable_Time_Setting)
time_Check_Button.pack(side=BOTTOM, fill=X)

# Setup Labels, Spinbox, and Radio Buttons to receive time inputs for opening the Coop
input_Open_Label = Label(main_Frame4, text='Set time to open coop ', font='none 12', fg='black')
input_Open_Label.pack(side=LEFT, ipadx=3, pady=5)
input_Open_Hour = ttk.Spinbox(main_Frame4, from_ =1, to=12, format='%02.0f', textvariable = var_Open_Hour, \
     width=4, wrap=True) 
input_Open_Hour.config(background = 'white')
input_Open_Hour.pack(side=LEFT, pady=5)      
input_Open_Minute = ttk.Spinbox(main_Frame4, from_=00, to=59, format='%02.0f', textvariable = var_Open_Minute, \
     width=4, wrap=True) 
input_Open_Minute.pack(side=LEFT, pady=5) 

am_Open_Radiobutton = ttk.Radiobutton(main_Frame4, variable=var_Open_Am_Pm, value='AM', text='AM') 
am_Open_Radiobutton.pack(side=TOP, padx=5)
pm_Open_Radiobutton = ttk.Radiobutton(main_Frame4, variable=var_Open_Am_Pm, value='PM', text='PM') 
pm_Open_Radiobutton.pack(side=BOTTOM, padx=5)

# Setup Labels, Spinbox, and Radio Buttons to receive time inputs for closing the Coop
input_Close_Label = Label(main_Frame5, fg='black', text='Set time to Close coop ', font='none 12')
input_Close_Label.pack(side=LEFT, pady=5)
input_Close_Hour = ttk.Spinbox(main_Frame5, from_=1, to=12, format='%02.0f', textvariable = var_Close_Hour, \
    width=4, wrap=True) 
input_Close_Hour.pack(side=LEFT, pady=5)   
input_Close_Minute = ttk.Spinbox(main_Frame5, from_=00, to=59, format='%02.0f', textvariable = var_Close_Minute, \
     width=4, wrap=True) 
input_Close_Minute.pack(side=LEFT, pady=5) 

am_Close_Radiobutton = ttk.Radiobutton(main_Frame5, variable=var_Close_Am_Pm, value='AM', text='AM') 
am_Close_Radiobutton.pack(side=TOP, padx=5)
pm_Close_Radiobutton = ttk.Radiobutton(main_Frame5, variable=var_Close_Am_Pm, value='PM', text='PM') 
pm_Close_Radiobutton.pack(side=BOTTOM, padx=5)

change_Time_Button = Button(main_Frame6, text='Set Times', width=10, command=enable_Disable_Time_Setting) 
apply_Time_Button = Button(main_Frame6, text='Apply', width=10, command=set_Timer_Thread) 

# Set Labels for time set and countdown timer for next Open/Close Operation
set_Open_Label = Label(main_Frame7, text='The Coop will Open at ')
set_Open_Time_Label = Label(main_Frame7, textvariable = open_Time_Twelve_Hour)              
set_Close_Label = Label(main_Frame8, text='The Coop will Close at ')      
set_Close_Time_Label = Label(main_Frame8, textvariable = close_Time_Twelve_Hour)

set_Countdown_Label = Label(main_Frame9, textvariable = formatted_Calc_Time, font='none 12 bold', fg='green')

# Door Status Label
label_Door_Status = Label (main_Frame10, textvariable=door_Status_Var, font='none 14 bold', fg='red')
label_Door_Status.pack()

# Progress Bar Defined, but not turned on
door_Progress = ttk.Progressbar(main_Frame10, orient=HORIZONTAL,length=100, mode='determinate')

# Message warning door is in opposite status of the Open/Close timer
door_Schedule_Off_Label = Label (main_Frame11, textvariable=schedule_Off_Var, font = 'none 12 bold', fg = 'red')

# Calibration Cycle 
if first_Time_Run == True:
    open_Coop()

# Call time_Setting function to enable or disable time settings operation
enable_Disable_Time_Setting()

#create status bar
status_Bar = Label(window, text="Coop Status = Unknown", relief=SUNKEN, anchor=W)
status_Bar.pack(side=BOTTOM, fill=X)

# Run main loop
window.mainloop()
