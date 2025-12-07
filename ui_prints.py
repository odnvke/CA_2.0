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

    [p]  -   go to Patterns (state og grid)

    In patterns menu:
        [ENTER]  -   Apply current pattern 
        [number] → [ENTER]  -   Set type (shape)
        [s] → [number] → [ENTER]  -   Set Size
        [v] → [number] → [ENTER]  -   Set Second Value


    [h]  -   Show this help

""")


def print_rule_s():
    """Print survival rule"""
    from rules import RuleManager
    rules = RuleManager.get_current_rules()
    rule_length = RuleManager.get_rule_length()  # Исправлено
    for i in range(rule_length):
        if rules.survival[i]:
            print(i, end=" ")
    print()


def print_rule_b():
    """Print birth rule"""
    from rules import RuleManager
    rules = RuleManager.get_current_rules()
    rule_length = RuleManager.get_rule_length()  # Исправлено
    for i in range(rule_length):
        if rules.birth[i]:
            print(i, end=" ")
    print()


def print_rule():
    """Print current rule with visualization"""
    from rules import RuleManager
    rules = RuleManager.get_current_rules()
    rule_length = RuleManager.get_rule_length()  # Исправлено
    
    b_s = ""
    s_s = ""
    
    for i in range(rule_length):  # Исправлено
        if rules.birth[i]:
            b_s += "█"
        else: 
            b_s += " "
        
        if rules.survival[i]:
            s_s += "█"
        else: 
            s_s += " "
    
    print(f"""
rule: ({rules.name})
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

def print_patterns(_type, size, value):
    """Print current settings"""
    print(f"""
Current Patterns Settings:
  Typy: {_type}
  Size: {size}
  Second Value: {value}
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
        print(f"enter:    [ENTER] - Apply;   Options: [number] - Set Type,  [s] - Set Size,  [v] - Second Value\n\n  =>  Patterns:    {input_buffer}", end="")
    elif current_input == "p s":
        print(f"enter:    [number] - Set Size Of Patterns\n\n  =>  Patterns:  Size:    {input_buffer}", end="")
    elif current_input == "p v":
        print(f"enter:    [number] - Set Second Patterns Value\n\n  =>  Patterns:  Second Value:    {input_buffer}", end="")
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