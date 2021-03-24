import button_input
import statParser
import fog_of_war
import resourcemanger
import math
import nmath
import enum

time = 0
time_speeds = [0.1, 0.25, 0.5, 1, 2, 4, 7, 10, 25, 50, 100, 150, 200]
selected_time = 3

pause_button = button_input.ButtonInput(demo.IsPdown)
speed_up     = button_input.ButtonInput(demo.IsUpdown)
speed_down   = button_input.ButtonInput(demo.IsDowndown)
left_mouse   = button_input.ButtonInput(demo.IsLeftMouseDown)
right_mouse  = button_input.ButtonInput(demo.IsRightMouseDown)
switch_ui    = button_input.ButtonInput(demo.IsQdown)

paused = False

statParser.loadStats()
fog_of_war.init(350,350)

class SelectedGroup(enum.Enum):
    Grupp1 = 0
    Grupp2 = 1
    Ingen  = 2

from Grupp1 import main as Grupp1main
from Grupp2 import main as Grupp2main

selected_group = SelectedGroup.Ingen

# Runs once every frame
def NebulaUpdate():
    global selected_time, selected_group
    global paused

    if pause_button.pressed():
        paused = not paused
        if paused:
            print("Paused")
            demo.SetTimeFactor(0)
        else:
            print("Unpaused")
            demo.SetTimeFactor(time_speeds[selected_time])

    if speed_up.pressed() and selected_time < len(time_speeds) -1:
        selected_time += 1
        print("Time: " + str(time_speeds[selected_time]) + "x")
        demo.SetTimeFactor(time_speeds[selected_time])

    if speed_down.pressed() and selected_time > 0:
        selected_time -= 1
        print("Time: " + str(time_speeds[selected_time]) + "x")
        demo.SetTimeFactor(time_speeds[selected_time])

    if switch_ui.pressed():
        selected_group = SelectedGroup((selected_group.value+1)%3)
    
    if selected_group == SelectedGroup.Ingen:
        if left_mouse.pressed():
            p = demo.RayCastMousePos()
            p.x = round(p.x)
            p.y += 0.5
            p.z = round(p.z)
            radius = 12
            for x in range(-radius, radius+1):
                for y in range(-radius, radius+1):
                    if (x**2 + y**2) < radius**2:
                        fog_of_war.grupp1.uncloud(round(p.x-x),round(p.z-y))
    
        if right_mouse.pressed():
            p = demo.RayCastMousePos()
            
            face_idx = navMesh.findInNavMeshIndex(nmath.Float2(p.x, p.z))
            face = navMesh.getFace(face_idx)

            print("--- Face: ", face_idx)

            print("edge: ", face)
            he = navMesh.getHalfEdge(face)
            print("neighbour: ", he.neighbourEdge)
            print("vertex: ", he.vertIdx)
            face = he.nextEdge
            print("edge: ", face)
            he = navMesh.getHalfEdge(face)
            print("neighbour: ", he.neighbourEdge)
            print("vertex: ", he.vertIdx)
            face = he.nextEdge
            print("edge: ", face)
            he = navMesh.getHalfEdge(face)
            print("neighbour: ", he.neighbourEdge)
            print("vertex: ", he.vertIdx)
            face = he.nextEdge

    if paused:
        return

    Grupp1main.NebulaUpdate()
    Grupp2main.NebulaUpdate()

    fog_of_war.visual.apply_cloud_changes()
    

# Runs one every frame when it's time to draw
def NebulaDraw():
    p = demo.RayCastMousePos()

    if selected_group == SelectedGroup.Grupp1:
        Grupp1main.NebulaDraw(p)
        p.x = round(p.x)
        p.y += 0.5
        p.z = round(p.z)
        demo.DrawBox(p, 1, nmath.Vec4(0,0,1,1))

    elif selected_group == SelectedGroup.Grupp2:
        Grupp2main.NebulaDraw(p)
        p.x = round(p.x)
        p.y += 0.5
        p.z = round(p.z)
        demo.DrawBox(p, 1, nmath.Vec4(1,0,0,1))

    else:
        p.x = round(p.x)
        p.y += 0.5
        p.z = round(p.z)
        demo.DrawBox(p, 1, nmath.Vec4(0,1,0,1))
        
    imgui.Begin("Cursor", None, 0)
    imgui.Text("X: " + str(p.x))
    imgui.Text("Z: " + str(p.z))
    imgui.Text(str(selected_group))
    imgui.End()



