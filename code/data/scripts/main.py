from Grupp1 import main as Grupp1main
from Grupp2 import main as Grupp2main
import button_input
import statParser
import math
import nmath

time = 0
time_speeds = [0.1, 0.25, 0.5, 1, 2, 4, 7, 10, 25, 50, 100, 150, 200]
selected_time = 3

pause_button = button_input.ButtonInput(demo.IsPdown)
speed_up     = button_input.ButtonInput(demo.IsUpdown)
speed_down   = button_input.ButtonInput(demo.IsDowndown)
left_mouse   = button_input.ButtonInput(demo.IsLeftMouseDown)
right_mouse  = button_input.ButtonInput(demo.IsRightMouseDown)

paused = False
statParser.loadStats()

# Runs once every frame
def NebulaUpdate():
    global paused

    if pause_button.pressed():
        paused = not paused
        if paused:
            print("Paused")
        else:
            print("Unpaused")

    if speed_up.pressed() and selected_time < len(time_speeds) -1:
        selected_time += 1
        print("Time: " + str(time_speeds[selected_time]) + "x")
        demo.SetTimeFactor(time_speeds[selected_time])

    if speed_down.pressed() and selected_time > 0:
        selected_time -= 1
        print("Time: " + str(time_speeds[selected_time]) + "x")
        demo.SetTimeFactor(time_speeds[selected_time])

    if paused:
        return

    Grupp1main.NebulaUpdate()
    Grupp2main.NebulaUpdate()
    

# Runs one every frame when it's time to draw
def NebulaDraw():
    Grupp1main.NebulaDraw()
    Grupp2main.NebulaDraw()

