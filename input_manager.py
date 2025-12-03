# input_manager.py
import pyglet
from config import preset, preset_count, set_val_of_rule, set_rule_from_preset
from app_state import AppState
from ui_prints import (
    gaide, print_rule_s, print_rule_b, print_rule, 
    print_settings, print_help, print_input,
    print_message, print_error, print_preset_info
)

# Константы для клавиш
_KEY_MAP = {
    'H': pyglet.window.key.H,
    'R': pyglet.window.key.R,
    'C': pyglet.window.key.C,
    'SPACE': pyglet.window.key.SPACE,
    'F': pyglet.window.key.F,
    'V': pyglet.window.key.V,
    'RIGHT': pyglet.window.key.RIGHT,
    'ESCAPE': pyglet.window.key.ESCAPE,
    'BACKSPACE': pyglet.window.key.BACKSPACE,
    'ENTER': pyglet.window.key.ENTER,
    'LEFT': pyglet.window.key.LEFT,
    'A': pyglet.window.key.A,
    'S': pyglet.window.key.S,
    'P': pyglet.window.key.P,
    'Z': pyglet.window.key.Z,
    'D': pyglet.window.key.D,
    'B': pyglet.window.key.B,
    'N': pyglet.window.key.N,
    'U': pyglet.window.key.U,
    'PERIOD': pyglet.window.key.PERIOD
}

_NUMBERS = [
    pyglet.window.key._0, pyglet.window.key._1, pyglet.window.key._2,
    pyglet.window.key._3, pyglet.window.key._4, pyglet.window.key._5,
    pyglet.window.key._6, pyglet.window.key._7, pyglet.window.key._8,
    pyglet.window.key._9
]

_MODIFIERS = {
    'CTRL': 18,
    'SHIFT': 16
}

# Callback-функции (будут установлены из main.py)
_callbacks = {
    'random_grid': None,
    'clear_grid': None,
    'toggle_pause': None,
    'create_pattern': None,
    'resize_grid_fast': None,
    'update_fps_settings': None,
    'create_grid': None
}

def init_callbacks(callbacks_dict):
    """Инициализировать callback-функции"""
    global _callbacks
    _callbacks.update(callbacks_dict)

# ------------------------------------------------------------------------------
# INPUT PROCESSING FUNCTIONS
# ------------------------------------------------------------------------------

def process_global_shortcut(symbol, modifiers):
    """Process global keyboard shortcuts"""
    if symbol == _KEY_MAP['R'] and modifiers == _MODIFIERS['CTRL']:
        return 'reset'
    elif symbol == _KEY_MAP['C'] and modifiers == _MODIFIERS['CTRL']:
        return 'clear'
    elif symbol == _KEY_MAP['SPACE']:
        return 'pause'
    elif symbol == _KEY_MAP['F'] and modifiers == _MODIFIERS['CTRL']:
        return 'toggle_fullscreen'
    elif symbol == _KEY_MAP['V'] and modifiers == _MODIFIERS['CTRL']:
        AppState.vsync_enabled = not AppState.vsync_enabled
        print_message(f"VSync {'enabled' if AppState.vsync_enabled else 'disabled'}")
        return 'vsync_changed'
    elif symbol == _KEY_MAP['RIGHT'] and modifiers == _MODIFIERS['SHIFT']:
        return 'next_frame'
    elif symbol == _KEY_MAP['ESCAPE']:
        print("exit")
        pyglet.app.exit()
        return False
    elif symbol == _KEY_MAP['H']:
        gaide()
        return False
    
    return None

def handle_enter_key():
    """Process Enter key for confirming inputs"""
    if AppState.current_input == "s f" and AppState.input_buffer:
        try:
            AppState.target_fps = float(AppState.input_buffer)
            AppState.input_buffer = ""
            print_message(f"Target FPS set to {AppState.target_fps}")
            return 'fps_changed'
        except ValueError:
            print_error("Invalid FPS value")
 
    elif AppState.current_input == "s z" and AppState.input_buffer:
        try:
            AppState.cell_size = max(0, float(AppState.input_buffer))
            AppState.input_buffer = ""
            print_message(f"Cell size set to {AppState.cell_size} pixels")
            return 'cell_size_changed'
        except ValueError:
            print_error("Invalid cell size")
            AppState.reset_input()
            
    elif AppState.current_input == "s d" and AppState.input_buffer:
        try:
            AppState.random_density = max(0, min(100, float(AppState.input_buffer)))
            AppState.input_buffer = ""
            print_message(f"Random density set to {AppState.random_density}%")
        except ValueError:
            print_error("Invalid density value")
            AppState.reset_input()

    elif AppState.current_input == "r p" and AppState.input_buffer:
        try:
            preset_index = int(AppState.input_buffer)
            preset_index = max(1, min(preset_count, preset_index))
            AppState.preset_index = preset_index
            print_help()
            print_preset_info(preset_index, preset[preset_index]['name'])
            set_rule_from_preset(preset_index)
            print_rule()
            print_input(AppState.current_input, AppState.input_buffer)
            AppState.input_buffer = ""
        except ValueError:
            print_error("Invalid preset num")
            AppState.reset_input()
    
    return None

def process_menu_navigation(symbol):
    """Process menu navigation keys"""
    if symbol == _KEY_MAP['R'] and AppState.current_input == "":
        AppState.current_input = "r"
        AppState.input_buffer = ""
        print_help()
        print_rule()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif symbol == _KEY_MAP['R'] and AppState.current_input == "s":
        AppState.current_input = "s r"
        AppState.input_buffer = ""
        print_help()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif symbol == _KEY_MAP['S'] and AppState.current_input == "":
        AppState.current_input = "s"
        AppState.input_buffer = ""
        print_help()
        print_settings(AppState.target_fps, AppState.vsync_enabled, 
                      AppState.cell_size, AppState.random_density)
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif symbol == _KEY_MAP['S'] and AppState.current_input == "r":
        AppState.current_input = "r s"
        AppState.input_buffer = ""
        print_help()
        print_rule()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif symbol == _KEY_MAP['P'] and AppState.current_input == "":
        AppState.current_input = "p"
        AppState.input_buffer = ""
        print_help()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif symbol == _KEY_MAP['P'] and AppState.current_input == "r":
        AppState.current_input = "r p"
        AppState.input_buffer = ""
        print_help()
        print_rule()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    
    return False

def process_submenu_navigation(symbol):
    """Process submenu navigation"""
    if symbol == _KEY_MAP['F'] and AppState.current_input == "s":
        AppState.current_input = "s f"
        AppState.input_buffer = ""
        print_help()
        print_rule()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif symbol == _KEY_MAP['Z'] and AppState.current_input == "s":
        AppState.current_input = "s z"
        AppState.input_buffer = ""
        print_help()
        print_rule()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif symbol == _KEY_MAP['D'] and AppState.current_input == "s":
        AppState.current_input = "s d"
        AppState.input_buffer = ""
        print_help()
        print_rule()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif symbol == _KEY_MAP['B'] and AppState.current_input == "r":
        AppState.current_input = "r b"
        AppState.input_buffer = ""
        print_help()
        print_rule()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif symbol == _KEY_MAP['A'] and AppState.current_input == "s r":
        AppState.current_input = "s r a"
        print_help()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif symbol == _KEY_MAP['N'] and AppState.current_input == "s r":
        AppState.current_input = "s r n"
        print_help()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    
    return False

def handle_preset_navigation(symbol):
    """Handle preset navigation"""
    if symbol == _KEY_MAP['P'] and AppState.current_input == "r p":
        AppState.preset_index -= 1
        if AppState.preset_index < 1:
            AppState.preset_index = preset_count
        print_help()
        set_rule_from_preset(AppState.preset_index)
        print_preset_info(AppState.preset_index, preset[AppState.preset_index]['name'], "Switched to prev")
        print_rule()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif symbol == _KEY_MAP['N'] and AppState.current_input == "r p":
        AppState.preset_index += 1
        if AppState.preset_index > preset_count:
            AppState.preset_index = 1
        set_rule_from_preset(AppState.preset_index)
        print_help()
        print_preset_info(AppState.preset_index, preset[AppState.preset_index]['name'], "Switched to next")
        print_rule()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    
    return False

def process_numeric_input(symbol):
    """Process numeric key input"""
    if symbol in _NUMBERS:
        num = _NUMBERS.index(symbol)
        
        # Rule editing (single digits)
        if AppState.current_input == "r b":
            if 0 <= num <= 8:
                set_val_of_rule(1, num)
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                print_rule_b()
                return None
            else:
                print_error(f"Invalid number: {num} (must be 0-8)")
                return None
                
        elif AppState.current_input == "r s":
            from config import sosed_count
            if 0 <= num <= 8:
                set_val_of_rule(0, num)
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                print_rule_s()
                return None
            else:
                print_error(f"Invalid number: {num} (must be 0-8)")
                return None

        elif AppState.current_input == "s r a":
            AppState.render_mode_active = max(min(num, 2), 0)
            print_help()
            print_input(AppState.current_input, AppState.input_buffer)
            print_message(f"set render mode for active:{AppState.render_mode_active}")
            return "mode1"

        elif AppState.current_input == "s r n":
            AppState.render_mode_inactive = max(min(num, 1), 0)
            print_help()
            print_input(AppState.current_input, AppState.input_buffer)
            print_message(f"set render mode for non active:{AppState.render_mode_inactive}")
            return "mode2"

        # Start patterns (однозначные числа)
        elif AppState.current_input == "p":
            if num in [1, 2, 3, 4, 5]:
                return f'pattern_{num}'
            else:
                print_error(f"Invalid pattern number: {num} (must be 1-5)")
                return None
    
    # Multi-digit number input
    if symbol in _NUMBERS or symbol == _KEY_MAP['PERIOD']:
        if AppState.current_input in ["s f", "s z", "s d", "r p"]:
            if symbol == _KEY_MAP['PERIOD']:
                AppState.input_buffer += "."
            else: 
                AppState.input_buffer += str(_NUMBERS.index(symbol) if symbol in _NUMBERS else 0)
            
            # Обновляем отображение
            if AppState.current_input in ["s f", "s z", "s d"]:
                print_help()
                print_settings(AppState.target_fps, AppState.vsync_enabled, 
                             AppState.cell_size, AppState.random_density)
                print_input(AppState.current_input, AppState.input_buffer)
            elif AppState.current_input == "r p":
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
            return None
    
    return None

def handle_back_navigation(symbol):
    """Handle back navigation (left arrow)"""
    if AppState.current_input in ["r", "p", "s"]:
        AppState.reset_input()
        print_help()
        print("\n <= Back to menu")
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif AppState.current_input in ["r b", "r s"]:
        AppState.current_input = "r"
        AppState.input_buffer = ""
        print_help()
        print("\n <= Back to rule menu")
        print_rule()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif AppState.current_input == "r p":
        AppState.current_input = "r"
        AppState.input_buffer = ""
        print_help()
        print("\n <= Back to rule menu")
        print_rule()
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif AppState.current_input in ["s f", "s z", "s d", "s r"]:
        if AppState.input_buffer:
            AppState.input_buffer = AppState.input_buffer[:-1]
            print_input(AppState.current_input, AppState.input_buffer)
        else:
            AppState.current_input = "s"
            AppState.input_buffer = ""
            print_help()
            print("\n <= Back to settings menu")
            print_settings(AppState.target_fps, AppState.vsync_enabled, 
                          AppState.cell_size, AppState.random_density)
            print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif AppState.current_input in ["s r a", "s r n"]:
        AppState.current_input = "s r"
        print_help()
        print("\n <= Back to select Render Mode")
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    elif AppState.current_input == "":
        print_help()
        print_input(AppState.current_input, AppState.input_buffer)
        print("\n   >>   we in root  -  try input [r], [s], [p] or [h]")
        return True
    
    return False

# ------------------------------------------------------------------------------
# MAIN EVENT HANDLER
# ------------------------------------------------------------------------------

def on_key_press(symbol, modifiers):
    """Main key press handler"""
    # Check global shortcuts first
    shortcut_result = process_global_shortcut(symbol, modifiers)
    if shortcut_result is not None:
        return _handle_shortcut_result(shortcut_result)
    
    # Handle shift modifier input
    if modifiers == _MODIFIERS['SHIFT']:
        if symbol == _KEY_MAP['BACKSPACE']:
            AppState.reset_input()
            print_message("Input cleared")
            return False
            
        elif symbol == _KEY_MAP['ENTER'] or symbol == _KEY_MAP['SPACE']:
            enter_result = handle_enter_key()
            if enter_result is not None:
                return _handle_shortcut_result(enter_result)
            return False

        elif symbol == _KEY_MAP['A']:
            if AppState.current_input == "s r":
                AppState.current_input = "s r a"
                print_help()
                print_input(AppState.current_input, AppState.input_buffer)
                return False

        elif symbol == _KEY_MAP['R']:
            if AppState.current_input == "":
                AppState.current_input = "r"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            if AppState.current_input == "s":
                AppState.current_input = "s r"
                AppState.input_buffer = ""
                print_help()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
                
        elif symbol == _KEY_MAP['S']:
            if AppState.current_input == "":
                AppState.current_input = "s"
                AppState.input_buffer = ""
                print_help()
                print_settings(AppState.target_fps, AppState.vsync_enabled, 
                             AppState.cell_size, AppState.random_density)
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            if AppState.current_input == "r":
                AppState.current_input = "r s"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
                
        elif symbol == _KEY_MAP['P']:
            if AppState.current_input == "":
                AppState.current_input = "p"
                AppState.input_buffer = ""
                print_help()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif AppState.current_input == "r":
                AppState.current_input = "r p"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False

        elif symbol == _KEY_MAP['F']:
            if AppState.current_input == "s":
                AppState.current_input = "s f"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
                
        elif symbol == _KEY_MAP['Z']:
            if AppState.current_input == "s":
                AppState.current_input = "s z"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
                
        elif symbol == _KEY_MAP['D']:
            if AppState.current_input == "s":
                AppState.current_input = "s d"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
                
        elif symbol == _KEY_MAP['B']:
            if AppState.current_input == "r":
                AppState.current_input = "r b"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
                
        elif symbol == _KEY_MAP['N']:
            if AppState.current_input == "r p":
                AppState.preset_index += 1
                if AppState.preset_index > preset_count:
                    AppState.preset_index = 1
                set_rule_from_preset(AppState.preset_index)
                print_help()
                print_preset_info(AppState.preset_index, preset[AppState.preset_index]['name'], "Switched to next")
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            if AppState.current_input == "s r":
                AppState.current_input = "s r n"
                print_help()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
        
        elif symbol == _KEY_MAP['U']:
            if AppState.current_input == "s":
                AppState.toggle_ui_visibility()
                print_message("ui visible toggled")
                return "changed ui visible"

        # Numeric input
        numeric_result = process_numeric_input(symbol)
        if numeric_result is not None:
            if numeric_result is not None and numeric_result != False:
                return _handle_numeric_result(numeric_result)
            
        # Multi-digit input update
        if symbol in _NUMBERS or symbol == _KEY_MAP['PERIOD']:
            if AppState.current_input in ["s f", "s z", "s d", "r p"]:
                return False

        # Back navigation
        if symbol == _KEY_MAP['LEFT']:
            if handle_back_navigation(symbol):
                return False
        
        print_help()
        print_input(AppState.current_input, AppState.input_buffer)
    
    return False

def _handle_shortcut_result(result):
    """Обработка результатов сочетаний клавиш"""
    if result == 'reset' and _callbacks['random_grid']:
        _callbacks['random_grid'](AppState.random_density)
        return result
    elif result == 'clear' and _callbacks['clear_grid']:
        _callbacks['clear_grid']()
        return result
    elif result == 'pause' and _callbacks['toggle_pause']:
        _callbacks['toggle_pause']()
        return result
    elif result == 'toggle_fullscreen' and AppState.window:
        AppState.window.set_fullscreen(not AppState.window.fullscreen)
        return result
    elif result == 'vsync_changed' and AppState.window:
        AppState.window.set_vsync(not AppState.window.vsync)
        return result
    elif result == 'fps_changed' and _callbacks['update_fps_settings']:
        _callbacks['update_fps_settings']()
        return result
    elif result == 'cell_size_changed' and _callbacks['create_grid']:
        _callbacks['create_grid']()
        return result
    elif result == 'next_frame':
        AppState.single_step = True
        return result
    
    return result

def _handle_numeric_result(result):
    """Обработка результатов числового ввода"""
    if result is None:
        return None
    
    if isinstance(result, str) and result.startswith('pattern_') and _callbacks['create_pattern']:
        pattern_type = int(result.split('_')[1])
        _callbacks['create_pattern'](pattern_type)
        return result
    elif result == "mode1" and _callbacks['resize_grid_fast']:
        _callbacks['resize_grid_fast'](AppState.window_width, AppState.window_height, 
                                      mode1=AppState.render_mode_active)
        return result
    elif result == "mode2" and _callbacks['resize_grid_fast']:
        _callbacks['resize_grid_fast'](AppState.window_width, AppState.window_height, 
                                      mode2=AppState.render_mode_inactive)
        return result
    
    return result

# ------------------------------------------------------------------------------
# MOUSE HANDLERS
# ------------------------------------------------------------------------------

def on_mouse_press(x, y, button, modifiers):
    return False

def on_mouse_release(x, y, button, modifiers):
    return False

def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    return False

def on_mouse_scroll(x, y, scroll_x, scroll_y):
    return False

def get_settings():
    """Get current settings (for backward compatibility)"""
    return {
        'target_fps': AppState.target_fps,
        'vsync_enabled': AppState.vsync_enabled,
        'cell_size': AppState.cell_size,
        'random_density': AppState.random_density
    }