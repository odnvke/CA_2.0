# ui_prints.py
"""
Функции для отображения интерфейса, помощи и другой информации.
"""

def gaide():
    """Display help information"""
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
    """Print survival rule"""
    from config import _RULE_S
    for i in range(len(_RULE_S)):
        if _RULE_S[i]:
            print(i, end=" ")


def print_rule_b():
    """Print birth rule"""
    from config import _RULE_B
    for i in range(len(_RULE_B)):
        if _RULE_B[i]:
            print(i, end=" ")


def print_rule():
    """Print current rule with visualization"""
    from config import _RULE_B, _RULE_S
    s_s = ""
    b_s = ""
    for i in range(0, 9):
        if _RULE_B[i]:
            b_s += "█"
        else: 
            b_s += " "
        if _RULE_S[i]:
            s_s += "█"
        else: 
            s_s += " "
        
    print(f"""
rule:
           012345678
  birth:   {b_s}
  survival:{s_s}
""")


def print_settings(target_fps, vsync_enabled, cell_size, random_density):
    """Print current settings"""
    fps_str = "Unlimited" if target_fps == 0 else f"{target_fps} FPS"
    vsync_str = 'Enabled' if vsync_enabled else 'disabled'
    
    print(f"""
Current Settings:
  Target FPS: {target_fps} ({fps_str})
  VSync: {vsync_str}
  Cell Size: {cell_size} pixels
  Random Density: {random_density}%
""")


def print_help():
    """Print input help prompt"""
    print("\n\n\n\n\n    type h to help\n  -=-=-=- new input -=-=-=-")


def print_input(current_input, input_buffer, preset_index=None, preset_name=None):
    """Print current input state and prompts"""
    if current_input == "":
        return
    
    if current_input == "r":
        print("enter:    [b] - birth,  [s] - survival,  [p] - preset\n\n  =>  Rule:    ", end="")
    elif current_input == "r b":
        print("enter:    [number] - toggle\n\n  =>  Rule:  Birth:    ", end="")
        print_rule_b()
    elif current_input == "r s":
        print("enter:    [number] - toggle\n\n  => Rule:  Survival:    ", end="")
        print_rule_s()
    elif current_input == "r p":
        print(f"enter:    [number] - select,  [n] - next,  [p] - prev\n\n  =>  Rule:  Preset:    {input_buffer}", end="")
    elif current_input == "s":
        print("enter:    [f] - FPS,  [z] - cell size,  [d] - density,  [u] - ui hide/show,  [r] - render mode\n\n  =>  Settings:    \n", end="")
    elif current_input == "s r":
        print("enter:    [a] - set render mode for active,  [n] - set render mode for non active(не работает),  \n\n  =>  Settings:  Render Mode:    \n", end="")
    elif current_input == "s r a":
        print("enter:    [number]  -   select Render Mode,  \n\n  =>  Settings:  Render Mode:  Active:    \n", end="")
    elif current_input == "s r n":
        print("enter:    [number]  -   select Render Mode,  \n\n  =>  Settings:  Render Mode:  Non Active:    \n", end="")
    elif current_input == "s f":
        print(f"enter:    [number] - set\n\n  =>  Settings:  FPS Limit:    {input_buffer} ", end="")
    elif current_input == "s z":
        print(f"enter:    [number] - set\n\n  =>  Settings:  Cell Size:    {input_buffer} ", end="")
    elif current_input == "s d":
        print(f"enter:    [number] - set\n\n  =>  Settings:  Density Of Spawn:    {input_buffer} ", end="")
    elif current_input == "p":
        print("enter:    [number] - set (1 (single), 2 (2x2), 3 (cross), 4 (glider), 5 (spaceship))\n\n  =>  Set State Of Grid:    ", end="")
    
    print()


def print_message(message):
    """Print general message"""
    print(f"\n   >>   {message}")


def print_error(message):
    """Print error message"""
    print(f"\n   >>   Error: {message}")


def print_preset_info(preset_index, preset_name, action="Selected"):
    """Print preset information"""
    print(f"\n   >>   {action} preset:  ({preset_index}) {preset_name}")