# input_manager.py
import pyglet
from rules import RuleManager
from app_state import AppState
from ui_prints import (
    gaide, print_rule_s, print_rule_b, print_rule, 
    print_settings, print_help, print_input,
    print_message, print_error, print_preset_info, print_patterns
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
    'CTRL': pyglet.window.key.MOD_CTRL,      # 64
    'SHIFT': pyglet.window.key.MOD_SHIFT,    # 1
    'ALT': pyglet.window.key.MOD_ALT         # 8
}

# Callback-функции
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

def process_global_shortcut(symbol, modifiers):
    """Process global keyboard shortcuts"""
    # CTRL комбинации
    if modifiers & _MODIFIERS['CTRL']:
        if symbol == _KEY_MAP['R']:
            AppState.force_redraw = True
            return 'reset'
        elif symbol == _KEY_MAP['C']:
            AppState.force_redraw = True
            return 'clear'
        elif symbol == _KEY_MAP['F']:
            return 'toggle_fullscreen'
        elif symbol == _KEY_MAP['V']:
            AppState.vsync_enabled = not AppState.vsync_enabled
            print_message(f"VSync {'enabled' if AppState.vsync_enabled else 'disabled'}")
            return 'vsync_changed'
    
    # Одиночные клавиши
    if symbol == _KEY_MAP['SPACE']:
        return 'pause'
    elif symbol == _KEY_MAP['RIGHT'] and AppState.paused:
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
            AppState.current_input = "s"
            AppState.target_fps = float(AppState.input_buffer)
            AppState.input_buffer = ""
            print_message(f"Target FPS set to {AppState.target_fps}")
            print_input(AppState.current_input, AppState.input_buffer)
            return 'fps_changed'
        except ValueError:
            print_error("Invalid FPS value")
            AppState.reset_input()
 
    elif AppState.current_input == "s z" and AppState.input_buffer:
        try:
            AppState.current_input = "s"
            AppState.cell_size = max(0.01, float(AppState.input_buffer))
            AppState.input_buffer = ""
            print_message(f"Cell size set to {AppState.cell_size} pixels")
            print_input(AppState.current_input, AppState.input_buffer)
            return 'cell_size_changed'
        except ValueError:
            print_error("Invalid cell size")
            AppState.reset_input()
    elif AppState.current_input == "s d" and AppState.input_buffer:
        try:
            AppState.current_input = "s"
            AppState.random_density = max(0, min(100, float(AppState.input_buffer)))
            AppState.input_buffer = ""
            print_message(f"Random density set to {AppState.random_density}%")
            print_input(AppState.current_input, AppState.input_buffer)
        except ValueError:
            print_error("Invalid density value")
            AppState.reset_input()
    elif AppState.current_input == "p":
        if AppState.input_buffer:
            try:
                AppState.patterns_type = max(0, min(32, int(AppState.input_buffer)))
                AppState.input_buffer = ""
                print_message(f"Type Of Patterns  {AppState.patterns_type}")
                print_input(AppState.current_input, AppState.input_buffer)
            except ValueError:
                print_error("Invalid Patterns value")
                AppState.reset_input()
        else: 
            #print("Pattern Set")
            return "pattern_" 
    elif AppState.current_input == "p s" and AppState.input_buffer:
        try:
            AppState.patterns_size = max(-10000, min(10000, float(AppState.input_buffer)))
            AppState.input_buffer = ""
            AppState.current_input = "p"
            print_message(f"Size Of Patterns  {AppState.patterns_size}\n")
            print_input(AppState.current_input, AppState.input_buffer)
        except ValueError:
            print_error("Invalid Size Patterns value")
            AppState.reset_input()
    elif AppState.current_input == "p v" and AppState.input_buffer:
        try:
            AppState.current_input = "p"
            AppState.patterns_second_value = max(-10000, min(10000, float(AppState.input_buffer)))
            AppState.input_buffer = ""
            print_message(f"Second Value Of Patterns  {AppState.patterns_second_value}")
            print_input(AppState.current_input, AppState.input_buffer)
        except ValueError:
            print_error("Invalid Second Patterns value")
            AppState.reset_input()
    elif AppState.current_input == "r p" and AppState.input_buffer:
        try:
            preset_index = int(AppState.input_buffer)
            preset_count = RuleManager.get_preset_count()
            
            if 1 <= preset_index <= preset_count:
                AppState.preset_index = preset_index
                
                success = RuleManager.load_preset(preset_index)
                if success:
                    print_help()
                    preset = RuleManager.get_preset(preset_index)
                    print_preset_info(preset_index, preset.name)
                    print_rule()
                else:
                    print_error(f"Preset {preset_index} not found")
                print_input(AppState.current_input, AppState.input_buffer)
                AppState.input_buffer = ""
            else:
                print_error(f"Invalid preset number (must be 1-{preset_count})")
                AppState.reset_input()
        except ValueError:
            print_error("Invalid preset number")
            AppState.reset_input()
    
    return None

def process_numeric_input(symbol):
    """Process numeric key input"""
    if symbol in _NUMBERS:
        num = _NUMBERS.index(symbol)
        
        # Rule editing (single digits) - переключение правил
        if AppState.current_input == "r b":
            if 0 <= num <= 8:
                RuleManager.set_rule_value('B', num)
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return None
            else:
                print_error(f"Invalid number: {num} (must be 0-8)")
                return None
                
        elif AppState.current_input == "r s":
            if 0 <= num <= 8:
                RuleManager.set_rule_value('S', num)
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return None
            else:
                print_error(f"Invalid number: {num} (must be 0-8)")
                return None

        # Render modes
        elif AppState.current_input == "s r a":
            AppState.render_mode_active = max(min(num, 5), 0)
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

    
    # Multi-digit number input
    if symbol in _NUMBERS or symbol == _KEY_MAP['PERIOD']:
        if AppState.current_input in ["s f", "s z", "s d", "r p", "p s", "p v"]:
            if symbol in _NUMBERS:
                AppState.input_buffer += str(_NUMBERS.index(symbol))
            elif symbol == _KEY_MAP['PERIOD']:
                AppState.input_buffer += "."
            
            if AppState.current_input in ["s f", "s z", "s d"]:
                print_help()
                print_settings(AppState.target_fps, AppState.vsync_enabled, 
                            AppState.cell_size, AppState.random_density)
                print_input(AppState.current_input, AppState.input_buffer)
            elif AppState.current_input == "r p":
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
            elif AppState.current_input in ["p s", "p v"]:
                print_help()
                print_patterns(AppState.patterns_type, AppState.patterns_size, AppState.patterns_second_value)
                print_input(AppState.current_input, AppState.input_buffer)
            return None

                # Start patterns
        elif AppState.current_input == "p":
            AppState.input_buffer += str(_NUMBERS.index(symbol))
            print_help()
            print_patterns(AppState.patterns_type, AppState.patterns_size, AppState.patterns_second_value)
            print_input(AppState.current_input, AppState.input_buffer)

    return None

def handle_backspace():
    """Обработка Backspace - удаление символов"""
    if AppState.input_buffer:
        # Удаляем последний символ из буфера
        AppState.input_buffer = AppState.input_buffer[:-1]
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    else:
        # Если буфер пуст, очищаем весь ввод
        AppState.reset_input()
        print_message("Input cleared")
        print_help()
        print_input(AppState.current_input, AppState.input_buffer)
        return True

def handle_left_arrow():
    """Обработка Left arrow - навигация назад по меню"""
    # Навигация назад по меню с очисткой буфера
    if AppState.current_input in ["r", "p", "s"]:
        AppState.reset_input()
        print_help()
        print("\n <= Back to menu")
        print_input(AppState.current_input, AppState.input_buffer)
        return True
    if AppState.current_input in ["p s", "p v"]:
        AppState.current_input = "p"
        print_help()
        print("\n <= Back to patterns menu")
        print_patterns(AppState.patterns_type, AppState.patterns_size, AppState.patterns_second_value)
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
        AppState.input_buffer = ""
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

def on_key_press(symbol, modifiers):
    """Main key press handler"""
    # Check global shortcuts first
    shortcut_result = process_global_shortcut(symbol, modifiers)
    if shortcut_result is not None:
        return _handle_shortcut_result(shortcut_result)
    
    # Handle Backspace - удаление символов
    if symbol == _KEY_MAP['BACKSPACE']:
        handle_backspace()
        return False
    
    # Handle Left arrow - навигация назад
    if symbol == _KEY_MAP['LEFT']:
        handle_left_arrow()
        return False
    
    # Handle Enter key
    if symbol == _KEY_MAP['ENTER']:
        enter_result = handle_enter_key()
        if enter_result is not None:
            return _handle_shortcut_result(enter_result)
        return False
    
    # Menu navigation (без модификаторов)
    if modifiers == 0:
        # Основное меню - только когда нет активного ввода
        if not AppState.current_input:
            if symbol == _KEY_MAP['R']:
                AppState.current_input = "r"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif symbol == _KEY_MAP['S']:
                AppState.current_input = "s"
                AppState.input_buffer = ""
                print_help()
                print_settings(AppState.target_fps, AppState.vsync_enabled, 
                             AppState.cell_size, AppState.random_density)
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif symbol == _KEY_MAP['P']:
                AppState.current_input = "p"
                AppState.input_buffer = ""
                print_help()
                print_patterns(AppState.patterns_type, AppState.patterns_size, AppState.patterns_second_value)
                print_input(AppState.current_input, AppState.input_buffer)
                return False
        
        # Меню правил (r -> ...)
        elif AppState.current_input == "r":
            if symbol == _KEY_MAP['B']:
                AppState.current_input = "r b"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif symbol == _KEY_MAP['S']:
                AppState.current_input = "r s"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif symbol == _KEY_MAP['P']:
                AppState.current_input = "r p"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
        
        # Меню настроек (s -> ...)
        elif AppState.current_input == "s":
            if symbol == _KEY_MAP['F']:
                AppState.current_input = "s f"
                AppState.input_buffer = ""
                print_help()
                print_settings(AppState.target_fps, AppState.vsync_enabled, 
                             AppState.cell_size, AppState.random_density)
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif symbol == _KEY_MAP['Z']:
                AppState.current_input = "s z"
                AppState.input_buffer = ""
                print_help()
                print_settings(AppState.target_fps, AppState.vsync_enabled, 
                             AppState.cell_size, AppState.random_density)
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif symbol == _KEY_MAP['D']:
                AppState.current_input = "s d"
                AppState.input_buffer = ""
                print_help()
                print_settings(AppState.target_fps, AppState.vsync_enabled, 
                             AppState.cell_size, AppState.random_density)
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif symbol == _KEY_MAP['R']:  # <-- КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: R в меню s
                AppState.current_input = "s r"
                AppState.input_buffer = ""
                print_help()
                print_settings(AppState.target_fps, AppState.vsync_enabled, 
                             AppState.cell_size, AppState.random_density)
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif symbol == _KEY_MAP['U']:
                AppState.ui_visible = not AppState.ui_visible
                print_message(f"UI {'shown' if AppState.ui_visible else 'hidden'}")
                print_help()
                print_input(AppState.current_input, AppState.input_buffer)
                return "ui_toggle"
        
        # Меню рендера (s r -> ...)
        elif AppState.current_input == "s r":
            if symbol == _KEY_MAP['A']:
                AppState.current_input = "s r a"
                AppState.input_buffer = ""
                print_help()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif symbol == _KEY_MAP['N']:
                AppState.current_input = "s r n"
                AppState.input_buffer = ""
                print_help()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
        
        # Переключение пресетов (r p -> n/p)
        elif AppState.current_input == "r p":
            if symbol == _KEY_MAP['N']:
                # Следующий пресет
                preset_count = RuleManager.get_preset_count()
                AppState.preset_index = (AppState.preset_index % preset_count) + 1
                success = RuleManager.load_preset(AppState.preset_index)
                if success:
                    print_help()
                    preset = RuleManager.get_preset(AppState.preset_index)
                    print_preset_info(AppState.preset_index, preset.name, action="Next preset")
                    print_rule()
                    print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif symbol == _KEY_MAP['P']:
                # Предыдущий пресет
                preset_count = RuleManager.get_preset_count()
                new_index = AppState.preset_index - 1
                if new_index < 1:
                    new_index = preset_count
                AppState.preset_index = new_index
                success = RuleManager.load_preset(AppState.preset_index)
                if success:
                    print_help()
                    preset = RuleManager.get_preset(AppState.preset_index)
                    print_preset_info(AppState.preset_index, preset.name, action="Previous preset")
                    print_rule()
                    print_input(AppState.current_input, AppState.input_buffer)
                return False
        elif AppState.current_input == "p":
            if symbol == _KEY_MAP["S"]:
                AppState.current_input = "p s"
                print_help()
                print_patterns(AppState.patterns_type, AppState.patterns_size, AppState.patterns_second_value)
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            if symbol == _KEY_MAP["V"]:
                AppState.current_input = "p v"
                print_help()
                print_patterns(AppState.patterns_type, AppState.patterns_size, AppState.patterns_second_value)
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            

    # SHIFT комбинации для альтернативного входа в подменю
    if modifiers & _MODIFIERS['SHIFT']:
        if not AppState.current_input:
            # Основное меню с SHIFT
            return False
        elif AppState.current_input == "r":
            if symbol == _KEY_MAP['B']:
                AppState.current_input = "r b"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif symbol == _KEY_MAP['S']:
                AppState.current_input = "r s"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
            elif symbol == _KEY_MAP['P']:
                AppState.current_input = "r p"
                AppState.input_buffer = ""
                print_help()
                print_rule()
                print_input(AppState.current_input, AppState.input_buffer)
                return False
    
    # Numeric input без SHIFT (для цифр 0-9)
    if modifiers == 0 and symbol in _NUMBERS or symbol == _KEY_MAP["PERIOD"]:
        numeric_result = process_numeric_input(symbol)
        if numeric_result is not None:
            return _handle_numeric_result(numeric_result)
    
    return False

def _handle_shortcut_result(result):
    """Обработка результатов сочетаний клавиш"""
    if isinstance(result, str) and result.startswith('pattern_') and _callbacks['create_pattern']:
        _callbacks['create_pattern'](4)
        return result
    elif result == 'reset' and _callbacks['random_grid']:
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
        AppState.window.set_vsync(AppState.vsync_enabled)
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
    elif result == 'ui_toggle':
        # UI visibility toggled
        return result
    
    return result

def _handle_numeric_result(result):
    """Обработка результатов числового ввода"""
    if result is None:
        return None
    
    elif result == "mode1" and _callbacks['resize_grid_fast']:
        _callbacks['resize_grid_fast'](
            int(AppState.window_width / AppState.cell_size),
            int(AppState.window_height / AppState.cell_size),
            mode1=AppState.render_mode_active,
            mode2=AppState.render_mode_inactive
        )
        return result
    elif result == "mode2" and _callbacks['resize_grid_fast']:
        _callbacks['resize_grid_fast'](
            int(AppState.window_width / AppState.cell_size),
            int(AppState.window_height / AppState.cell_size),
            mode1=AppState.render_mode_active,
            mode2=AppState.render_mode_inactive
        )
        return result
    
    return result

def get_settings():
    """Get current settings (for backward compatibility)"""
    return {
        'target_fps': AppState.target_fps,
        'vsync_enabled': AppState.vsync_enabled,
        'cell_size': AppState.cell_size,
        'random_density': AppState.random_density
    }