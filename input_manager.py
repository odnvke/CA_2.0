# input_manager.py
import pyglet
from config import _RULE_S, _RULE_B, preset, preset_count, set_val_of_rule, set_rule_from_preset

inp = ""
p_inp = inp
preset_i = 0
input_buffer = ""

# Settings
target_fps = 0
vsync_enabled = False
cell_size = 3
random_density = 30
_mode1 = 0
_mode2 = 0
_UI = True

def gaide():
    print("""




  ================================= HELP ================================= 

    [CTRL + R]  -   Random grid
    [CTRL + C]  -   Clear
    [CTRL + F]  -   FullScreen  
    [CTRL + V]  -   Toggle VSync

    [SPACE]  -   Toggle Pause and Play
    [RIGHT]  -   Next frame (when paused)

    [ESC]  -   Exit

    [BACKSPACE]  -  Clear input
    [ARROW LEFT]  -  Back

    Commands:
    [r]  -   go to Rule editing menu

    In Rule menu:
        [b] → [number]  -   Birth Rule toggle
        [s] → [number]  -   Survival Rule toggle
        [p] → [n]/[p]  -   Next or prev preset
        [p] → [number] → [ENTER]  -   Select preset

    [s]  -   go to settings menu

    In setting menu:
        [f] → [number] → [ENTER]  -   Set FPS limit
        [z] → [number] → [ENTER]  -   Set cell size
        [d] → [number] → [ENTER]  -   Set density of spawn(ctrl + R)
        [r] → [a] → [number]  -   Set mode of render active cells
        [r] → [n] → [number]  -   Set mode of render non active cells
        [u]  -  Toggel show/hide user interface

    [p] → [number]  -   Set state of grid


    
    [h]  -   Show this help

""")

def print_rule_s():
    from config import _RULE_S
    for i in range(len(_RULE_S)):
        if _RULE_S[i]:
            print(i, end=" ")

def print_rule_b():
    from config import _RULE_B
    for i in range(len(_RULE_B)):
        if _RULE_B[i]:
            print(i, end=" ")

def print_rule():
    from config import _RULE_B, _RULE_S
    s_s = ""
    b_s = ""
    for i in range(0, 9):
        if _RULE_B[i]:
            b_s += "█"
        else: b_s += " "
        if _RULE_S[i]:
            s_s += "█"
        else: s_s += " "
        
    print(f"""
rule:
           012345678
  birth:   {b_s}
  survival:{s_s}
""")

def print_settings():
    fps_str = "Unlimited" if target_fps == 0 else f"{target_fps} FPS"
    print(f"""
Current Settings:
  Target FPS: {target_fps} ({fps_str})
  VSync: {'Enabled' if vsync_enabled else 'disabled'}
  Cell Size: {cell_size} pixels
  Random Density: {random_density}%
""")

def print_help():
    print("\n\n\n\n\n    type h to help\n  -=-=-=- new input -=-=-=-")

def print_input():
    global inp, p_inp, input_buffer
    
    
    if inp == "":
        pass
    else:
        #print(f"Current input: {inp}")
        
        if inp == "r":
            print("enter:    [b] - birth,  [s] - survival,  [p] - preset\n\n  =>  Rule:    ", end="")
        elif inp == "r b":
            print("enter:    [number] - toggle\n\n  =>  Rule:  Birth:    ", end="")
            print_rule_b()
        elif inp == "r s":
            print("enter:    [number] - toggle\n\n  => Rule:  Survival:    ", end="")
            print_rule_s()
        elif inp == "r p":
            print(f"enter:    [number] - select,  [n] - next,  [p] - prev\n\n  =>  Rule:  Preset:    {input_buffer}", end="")
        elif inp == "s":
            print("enter:    [f] - FPS,  [z] - cell size,  [d] - density,  [u] - ui hide/show,  [r] - render mode\n\n  =>  Settings:    \n", end="")
        elif inp == "s r":
            print("enter:    [a] - set render mode for active,  [n] - set render mode for non active(не работает),  \n\n  =>  Settings:  Render Mode:    \n", end="")
        elif inp == "s r a":
            print("enter:    [number]  -   select Render Mode,  \n\n  =>  Settings:  Render Mode:  Active:    \n", end="")
        elif inp == "s r n":
            print("enter:    [number]  -   select Render Mode,  \n\n  =>  Settings:  Render Mode:  Non Active:    \n", end="")
        elif inp == "s f":
            print(f"enter:    [number] - set\n\n  =>  Settings:  FPS Limit:    {input_buffer} ", end="")
        elif inp == "s z":
            print(f"enter:    [number] - set\n\n  =>  Settings:  Cell Size:    {input_buffer} ", end="")
        elif inp == "s d":
            print(f"enter:    [number] - set\n\n  =>  Settings:  Density Of Spawn:    {input_buffer} ", end="")
        elif inp == "p":
            print("enter:    [number] - set (1 (single), 2 (2x2), 3 (cross), 4 (glider), 5 (spaceship))\n\n  =>  Set State Of Grid:    ", end="")
        
        print()

numbers = [pyglet.window.key._0, pyglet.window.key._1, pyglet.window.key._2, pyglet.window.key._3, pyglet.window.key._4, pyglet.window.key._5, pyglet.window.key._6, pyglet.window.key._7, pyglet.window.key._8, pyglet.window.key._9]

def on_key_press(symbol, modifiers):
    global inp, numbers, preset_i, preset, set_rule_from_preset, _RULE_B, _RULE_S
    global target_fps, cell_size, random_density, input_buffer, _UI, _mode1, _mode2

    from config import _RULE_B, _RULE_S

    if symbol == pyglet.window.key.H:
        gaide()
        return False
    
    # Global shortcuts
    if symbol == pyglet.window.key.R and modifiers == 18:
        return 'reset'
    elif symbol == pyglet.window.key.C and modifiers == 18:
        return 'clear'
    elif symbol == pyglet.window.key.SPACE:
        return 'pause'
    elif symbol == pyglet.window.key.F and modifiers == 18:
        return 'toggle_fullscreen'
    elif symbol == pyglet.window.key.V and modifiers == 18:
        global vsync_enabled
        vsync_enabled = not vsync_enabled
        print(f"   >>   VSync {'enabled' if vsync_enabled else 'disabled'}")
        return 'vsync_changed'
    elif symbol == pyglet.window.key.RIGHT and modifiers == 16:
        return 'next_frame'
    elif symbol == pyglet.window.key.ESCAPE:
            print("exit")
            pyglet.app.exit()
            return False

    if modifiers == 16:
        if symbol == pyglet.window.key.BACKSPACE:
            inp = ""
            input_buffer = ""
            print("\n   >>   Input cleared")
            return False
            


        elif symbol == pyglet.window.key.ENTER or symbol == pyglet.window.key.SPACE:
            # Обработка ввода многозначных чисел
            if inp == "s f" and input_buffer:
                try:
                    inp = "s f"
                    target_fps = float(input_buffer)
                    input_buffer = ""
                    print(f"\n   >>   Target FPS set to {target_fps}")
                    return 'fps_changed'
                except ValueError:
                    print("\n   >>   Invalid FPS value")
 
            elif inp == "s z" and input_buffer:
                try:
                    cell_size = max(0, float(input_buffer))
                    print(f"\n   >>   Cell size set to {cell_size} pixels")
                    inp = "s z"
                    input_buffer = ""
                    return 'cell_size_changed'
                except ValueError:
                    print("\n   >>   Invalid cell size")
                    inp = ""
                    input_buffer = ""
                    
            elif inp == "s d" and input_buffer:
                try:
                    random_density = max(0, min(100, float(input_buffer)))
                    print(f"\n   >>   Random density set to {random_density}%")
                    inp = "s d"
                    input_buffer = ""
                except ValueError:
                    print("\n   >>   Invalid density value")
                    inp = ""
                    input_buffer = ""

            elif inp == "r p" and input_buffer:
                try:
                    preset_i = int(input_buffer)
                    preset_i = max(1, min(preset_count, preset_i))
                    print_help()
                    print(f"\n   >>   Selected preset:  ({preset_i}) {preset[preset_i]['name']}")
                    set_rule_from_preset(preset_i)
                    print_rule()
                    print_input()
                    inp = "r p"
                    input_buffer = ""
                except ValueError:
                    print("\n   >>   Invalid preset num")
                    inp = ""
                    input_buffer = ""
            return False

        elif symbol == pyglet.window.key.A:
            if inp == "s r":
                inp = "s r a"
                print_help()
                print_input()
                return False

        elif symbol == pyglet.window.key.R:
            if inp == "":
                inp = "r"
                input_buffer = ""
                print_help()
                print_rule()
                print_input()
                return False
            if inp == "s":
                inp = "s r"
                input_buffer = ""
                print_help()
                print_input()
                return False
                
        elif symbol == pyglet.window.key.S:
            if inp == "":
                inp = "s"
                input_buffer = ""
                print_help()
                print_settings()
                print_input()
                return False
            if inp == "r":
                inp = "r s"
                input_buffer = ""
                print_help()
                print_rule()
                print_input()
                return False
                
        elif symbol == pyglet.window.key.P:
            if inp == "":
                inp = "p"
                input_buffer = ""
                print_help()
                print_input()
                return False
            elif inp == "r":
                inp = "r p"
                input_buffer = ""
                print_help()
                print_rule()
                print_input()
                return False
            if inp == "r p":
                preset_i -= 1
                if preset_i < 0: preset_i = preset_count-1
                print_help()
                set_rule_from_preset(preset_i)
                print(f"\n   >>   Switched to prev preset ({preset_i}): {preset[preset_i]['name']}")
                print_rule()
                print_input()
                return False

        elif symbol == pyglet.window.key.F:
            if inp == "s":
                inp = "s f"
                input_buffer = ""
                print_help()
                print_rule()
                print_input()
                return False
                
        elif symbol == pyglet.window.key.Z:
            if inp == "s":
                inp = "s z"
                input_buffer = ""
                print_help()
                print_rule()
                print_input()
                return False
                
        elif symbol == pyglet.window.key.D:
            if inp == "s":
                inp = "s d"
                input_buffer = ""
                print_help()
                print_rule()
                print_input()
                return False
                
        elif symbol == pyglet.window.key.B:
            if inp == "r":
                inp = "r b"
                input_buffer = ""
                print_help()
                print_rule()
                print_input()
                return False
                
                
        elif symbol == pyglet.window.key.N:
            if inp == "r p":
                preset_i = ((preset_i) % preset_count) + 1
                set_rule_from_preset(preset_i)
                print_help()
                print(f"\n   >>   Switched to next preset ({preset_i}): {preset[preset_i]['name']}")
                print_rule()
                print_input()
                return False
            if inp == "s r":
                inp = "s r n"
                print_help()
                print_input()
                return False
        
        elif symbol == pyglet.window.key.U:
            if inp == "s":
                _UI = not _UI
                print("   >>   ui visible toggled")
                return "changed ui visible"

        elif symbol in numbers:
            num = numbers.index(symbol)
            
            # Rule editing (однозначные числа)
            if inp == "r b":
                #from config import sosed_count
                #if -1 < num <= sosed_count:
                if True:
                    set_val_of_rule(1, num)
                    print_help()
                    print_rule()
                    print_input()
                    print_rule_b()
                    inp = "r b"
                    return False
                
            elif inp == "r s":
                from config import sosed_count
                if -1 < num <= sosed_count:
                    set_val_of_rule(0, num)
                    print_help()
                    print_rule()
                    print_input()
                    print_rule_s()
                    inp = "r s"
                    return False

            elif inp == "s r a":
                _mode1 = max(min(num, 2), 0)
                inp = "s r a"
                print_help()
                print_input()
                print(f"\n   >>   set render mode for active:{_mode1}")
                return "mode1"

            elif inp == "s r n":
                _mode2 = max(min(num, 1), 0)
                inp = "s r n"
                print_help()
                print_input()
                print(f"\n   >>   set render mode for non active:{_mode2}")
                return "mode2"

            # Start patterns (однозначные числа)
            elif inp == "p":
                if num in [1, 2, 3, 4, 5]:
                    inp = "p"
                    return f'pattern_{num}'            

        if symbol in numbers or symbol == pyglet.window.key.PERIOD:
            if inp in ["s f", "s z", "s d",  "r p"]:
                if symbol == pyglet.window.key.PERIOD:
                    input_buffer += "."
                else: 
                    input_buffer += str(num)
                if inp in ["s f", "s z", "s d"]:
                    print_help()
                    print_settings()
                    print_input()
                elif inp == "r p":
                    print_help()
                    print_rule()
                    print_input()                   
                return False

            
        elif symbol == pyglet.window.key.LEFT:
            if inp in ["r", "p", "s"]:
                inp = ""
                input_buffer = ""
                print_help()
                print("\n <= Back to menu")
                print_input()
                return False
            if inp in ["r b", "r s"]:
                inp = "r"
                input_buffer = ""
                print_help()
                print("\n <= Back to rule menu")
                print_rule()
                print_input()
                return False
            elif inp == "r p":
                inp = "r"
                input_buffer = ""
                print_help()
                print("\n <= Back to rule menu")
                print_rule()
                print_input()
                return False
            elif inp in ["s f", "s z", "s d", "s r"]:
                if input_buffer:
                    input_buffer = input_buffer[:-1]
                    print_input()
                else:
                    inp = "s"
                    input_buffer = ""
                    print_help()
                    print("\n <= Back to rule menu")
                    print_rule()
                    print_input()
                return False
            elif inp in ["s r a", "s r n"]:
                inp = "s r"
                print_help()
                print("\n <= Back to select Render Mode")
                print_input()
                return False
            elif inp == "":
                print_help()
                print_input()
                print("\n   >>   we in root  -  try input [r], [s], [p] or [h]")
                return False
        print_help()
        print_input()
    return False

def on_mouse_press(x, y, button, modifiers):
    return False

def on_mouse_release(x, y, button, modifiers):
    return False

def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    return False

def on_mouse_scroll(x, y, scroll_x, scroll_y):
    return False

def get_settings():
    return {
        'target_fps': target_fps,
        'vsync_enabled': vsync_enabled,
        'cell_size': cell_size,
        'random_density': random_density
    }
