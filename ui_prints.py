# ui_prints.py
"""
Функции для отображения интерфейса.
"""

import os
import sys

# Активируем ANSI цвета для Windows
if sys.platform == "win32":
    os.system("")

class Colors:
    # Минимальные цвета
    TITLE = '\033[1;36m'      # Бирюзовый только для заголовков
    INPUT = '\033[1;33m'      # Желтый только для ввода
    ERROR = '\033[1;31m'      # Красный только для ошибок
    RESET = '\033[0m'
    WHITE = '\033[38;5;223m'      # Белый для дополнительных элементов
    INP = '\033[1;38;5;214m'
    # Правила - с белым цветом
    BIRTH = ''     # Белый для birth
    SURVIVAL = ''   # Белый для survival

C = Colors()


def gaide():
    """Display help information"""
    print(f"""
{C.TITLE}= HELP ={C.RESET}

{C.WHITE}[CTRL + R]{C.RESET}  -   Random grid
{C.WHITE}[CTRL + C]{C.RESET}  -   Clear
{C.WHITE}[CTRL + F]{C.RESET}  -   FullScreen  
{C.WHITE}[CTRL + V]{C.RESET}  -   Toggle VSync

{C.WHITE}[SPACE]{C.RESET}  -   Toggle Pause and Play
{C.WHITE}[RIGHT]{C.RESET}  -   Next frame (when paused)

{C.WHITE}[ESC]{C.RESET}  -   Exit

{C.WHITE}[BACKSPACE]{C.RESET}  -  Clear input
{C.WHITE}[ARROW LEFT]{C.RESET}  -  Back

Commands:
{C.WHITE}[r]{C.RESET}  -   go to Rule editing menu

  In Rule menu:
    {C.WHITE}[b]{C.RESET} → {C.WHITE}[number]{C.RESET}  -   Birth Rule toggle
    {C.WHITE}[s]{C.RESET} → {C.WHITE}[number]{C.RESET}  -   Survival Rule toggle
    {C.WHITE}[p]{C.RESET} → {C.WHITE}[n]{C.RESET}/{C.WHITE}[p]{C.RESET}  -   Next or prev preset
    {C.WHITE}[p]{C.RESET} → {C.WHITE}[number]{C.RESET} → {C.WHITE}[ENTER]{C.RESET}  -   Select preset

{C.WHITE}[s]{C.RESET}  -   go to settings menu

  In setting menu:
    {C.WHITE}[f]{C.RESET} → {C.WHITE}[number]{C.RESET} → {C.WHITE}[ENTER]{C.RESET}  -   Set FPS limit
    {C.WHITE}[z]{C.RESET} → {C.WHITE}[number]{C.RESET} → {C.WHITE}[ENTER]{C.RESET}  -   Set cell size
    {C.WHITE}[d]{C.RESET} → {C.WHITE}[number]{C.RESET} → {C.WHITE}[ENTER]{C.RESET}  -   Set density of spawn(ctrl + R)
    {C.WHITE}[r]{C.RESET} → {C.WHITE}[a]{C.RESET} → {C.WHITE}[number]{C.RESET}  -   Set mode of render active cells
    {C.WHITE}[r]{C.RESET} → {C.WHITE}[n]{C.RESET} → {C.WHITE}[number]{C.RESET}  -   Set mode of render non active cells
    {C.WHITE}[u]{C.RESET}  -  Toggle show/hide user interface

{C.WHITE}[p]{C.RESET}  -   go to Patterns (state og grid)

  In patterns menu:
    {C.WHITE}[ENTER]{C.RESET}  -   Apply current pattern 
    {C.WHITE}[number]{C.RESET} → {C.WHITE}[ENTER]{C.RESET}  -   Set type (shape)
    {C.WHITE}[s]{C.RESET} → {C.WHITE}[number]{C.RESET} → {C.WHITE}[ENTER]{C.RESET}  -   Set Size
    {C.WHITE}[v]{C.RESET} → {C.WHITE}[number]{C.RESET} → {C.WHITE}[ENTER]{C.RESET}  -   Set Second Value

{C.WHITE}[h]{C.RESET}  -   Show this help

""")


def print_rule_s():
    """Print survival rule"""
    from rules import RuleManager
    rules = RuleManager.get_current_rules()
    rule_length = RuleManager.get_rule_length()
    print(f"{C.SURVIVAL}Survival:{C.RESET} ", end="")
    for i in range(rule_length):
        if rules.survival[i]:
            print(f"{C.WHITE}{i}{C.RESET}", end=" ")
    print()


def print_rule_b():
    """Print birth rule"""
    from rules import RuleManager
    rules = RuleManager.get_current_rules()
    rule_length = RuleManager.get_rule_length()
    print(f"{C.BIRTH}Birth:{C.RESET} ", end="")
    for i in range(rule_length):
        if rules.birth[i]:
            print(f"{C.WHITE}{i}{C.RESET}", end=" ")
    print()


def print_rule():
    """Print current rule with visualization"""
    from rules import RuleManager
    rules = RuleManager.get_current_rules()
    rule_length = RuleManager.get_rule_length()
    
    b_s = ""
    s_s = ""
    
    for i in range(rule_length):
        if rules.birth[i]:
            b_s += f"{C.WHITE}█{C.RESET}"
        else: 
            b_s += f"{C.WHITE} {C.RESET}"
        
        if rules.survival[i]:
            s_s += f"{C.WHITE}█{C.RESET}"
        else: 
            s_s += f"{C.WHITE} {C.RESET}"
    
    print(f"""
rule: ({rules.name})
           012345678
  {C.BIRTH}birth:{C.RESET}   {b_s}
  {C.SURVIVAL}survival:{C.RESET}{s_s}
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
  Type: {_type}
  Size: {size}
  Second Value: {value}
""")


def print_help():
    """Print input help prompt"""
    print(f"\n\n\n\n\n{C.WHITE}type h to help \n-=-=-=- new input -=-=-=-{C.RESET}")


def print_input(current_input, input_buffer, preset_index=None, preset_name=None):
    """Print current input state and prompts"""
    if current_input == "":
        return
    
    if current_input == "r":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[b]{C.RESET} - birth,  {C.WHITE}[s]{C.RESET} - survival,  {C.WHITE}[p]{C.RESET} - preset\n\n{C.INP}=>  Rule:    {C.RESET}", end="")
    elif current_input == "r b":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[number]{C.RESET} - toggle\n\n{C.INP}=>  Rule:  ", end="")
        print_rule_b()
    elif current_input == "r s":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[number]{C.RESET} - toggle\n\n{C.INP}=> Rule:  ", end="")
        print_rule_s()
    elif current_input == "r p":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[number]{C.RESET} - select,  {C.WHITE}[n]{C.RESET} - next,  {C.WHITE}[p]{C.RESET} - prev\n\n{C.INP}=>  Rule:  Preset:    {input_buffer}{C.RESET}", end="")
    elif current_input == "s":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[f]{C.RESET} - FPS,  {C.WHITE}[z]{C.RESET} - cell size,  {C.WHITE}[d]{C.RESET} - density,  {C.WHITE}[u]{C.RESET} - ui hide/show,  {C.WHITE}[r]{C.RESET} - render mode\n\n{C.INP}=>  Settings:    {C.RESET}\n", end="")
    elif current_input == "s r":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[a]{C.RESET} - set render mode for active,  {C.WHITE}[n]{C.RESET} - set render mode for non active,  \n\n{C.INP}=>  Settings:  Render Mode:    {C.RESET}\n", end="")
    elif current_input == "s r a":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[number]{C.RESET}  -   select Render Mode,  \n\n{C.INP}=>  Settings:  Render Mode:  Active:    {C.RESET}\n", end="")
    elif current_input == "s r n":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[number]{C.RESET}  -   select Render Mode,  \n\n{C.INP}=>  Settings:  Render Mode:  Non Active:    {C.RESET}\n", end="")
    elif current_input == "s f":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[number]{C.RESET} - set\n\n{C.INP}=>  Settings:  FPS Limit:    {input_buffer} {C.RESET}", end="")
    elif current_input == "s z":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[number]{C.RESET} - set\n\n{C.INP}=>  Settings:  Cell Size:    {input_buffer} {C.RESET}", end="")
    elif current_input == "s d":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[number]{C.RESET} - set\n\n{C.INP}=>  Settings:  Density Of Spawn:    {input_buffer} {C.RESET}", end="")
    elif current_input == "p":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[ENTER]{C.RESET} - Apply;   Options: {C.WHITE}[number]{C.RESET} - Set Type,  {C.WHITE}[s]{C.RESET} - Set Size,  {C.WHITE}[v]{C.RESET} - Second Value\n\n{C.INP}=>  Patterns:    {input_buffer}{C.RESET}", end="")
    elif current_input == "p s":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[number]{C.RESET} - Set Size Of Patterns\n\n{C.INP}=>  Patterns:  Size:    {input_buffer}{C.RESET}", end="")
    elif current_input == "p v":
        print(f"{C.INPUT}enter:{C.RESET}    {C.WHITE}[number]{C.RESET} - Set Second Patterns Value\n\n{C.INP}=>  Patterns:  Second Value:    {input_buffer}{C.RESET}", end="")
    print()


def print_message(message):
    """Print general message"""
    print(f"\n{C.INPUT}>>{C.RESET}   {message}")


def print_error(message):
    """Print error message"""
    print(f"\n{C.ERROR}>>   Error:{C.RESET} {message}")


def print_preset_info(preset_index, preset_name, action="Selected"):
    """Print preset information"""
    print(f"\n{C.INPUT}>>{C.RESET}   {action} preset:  ({preset_index}) {preset_name}")