# input_handlers/special_keys.py
"""
Обработка специальных клавиш (Backspace, Enter, Left)
ТОЧНАЯ копия оригинальной логики
"""

from app_state import AppState
from rules import RuleManager
from ui_prints import (
    print_help, print_input, print_message, 
    print_error, print_preset_info, print_rule,
    print_settings, print_patterns
)


class SpecialKeysHandler:
    """Обработчик специальных клавиш"""
    
    def __init__(self, callbacks=None):
        self.callbacks = callbacks or {}
    
    def handle_backspace(self):
        """ТОЧНАЯ копия оригинального handle_backspace()"""
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
    
    def handle_enter(self):
        """ТОЧНАЯ копия оригинального handle_enter_key()"""
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
                return True
                
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
                return True
                
        elif AppState.current_input == "s d" and AppState.input_buffer:
            try:
                AppState.current_input = "s"
                AppState.random_density = max(0, min(100, float(AppState.input_buffer)))
                AppState.input_buffer = ""
                print_message(f"Random density set to {AppState.random_density}%")
                print_input(AppState.current_input, AppState.input_buffer)
                return True
            except ValueError:
                print_error("Invalid density value")
                AppState.reset_input()
                return True
                
        elif AppState.current_input == "p":
            if AppState.input_buffer:
                try:
                    AppState.patterns_type = max(0, min(32, int(AppState.input_buffer)))
                    AppState.input_buffer = ""
                    print_message(f"Type Of Patterns {AppState.patterns_type}")
                    print_input(AppState.current_input, AppState.input_buffer)
                    return True
                except ValueError:
                    print_error("Invalid Patterns value")
                    AppState.reset_input()
                    return True
            else: 
                # Применяем паттерн
                return "pattern_apply"
                
        elif AppState.current_input == "p s" and AppState.input_buffer:
            try:
                AppState.patterns_size = max(-10000, min(10000, float(AppState.input_buffer)))
                AppState.input_buffer = ""
                AppState.current_input = "p"
                print_message(f"Size Of Patterns {AppState.patterns_size}\n")
                print_input(AppState.current_input, AppState.input_buffer)
                return True
            except ValueError:
                print_error("Invalid Size Patterns value")
                AppState.reset_input()
                return True
                
        elif AppState.current_input == "p v" and AppState.input_buffer:
            try:
                AppState.current_input = "p"
                AppState.patterns_second_value = max(-10000, min(10000, float(AppState.input_buffer)))
                AppState.input_buffer = ""
                print_message(f"Second Value Of Patterns {AppState.patterns_second_value}")
                print_input(AppState.current_input, AppState.input_buffer)
                return True
            except ValueError:
                print_error("Invalid Second Patterns value")
                AppState.reset_input()
                return True
                
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
                    else:
                        print_error(f"Preset {preset_index} not found")
                    print_input(AppState.current_input, AppState.input_buffer)
                    AppState.input_buffer = ""
                    return True
                else:
                    print_error(f"Invalid preset number (must be 1-{preset_count})")
                    AppState.reset_input()
                    return True
            except ValueError:
                print_error("Invalid preset number")
                AppState.reset_input()
                return True
        
        return None
    
    def handle_left_arrow(self):
        """ТОЧНАЯ копия оригинального handle_left_arrow()"""
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