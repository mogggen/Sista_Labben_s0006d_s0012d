import Grupp1.path_manager as path_manager

import nmath, demo
import button_input

y_button = button_input.ButtonInput(demo.IsYDown)

path = path_manager.instance.create_path(nmath.Float2(0,0), nmath.Float2(10,100), lambda : print("Done"))

def NebulaUpdate():
    if not path.is_done:
        if y_button.pressed():
            path_manager.instance.step_path(path)
            print("Y")

def NebulaDraw():
    path.algorithm.visualize(path)
