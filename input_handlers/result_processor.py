# input_handlers/result_processor.py
"""
Обработка результатов выполнения команд
"""

import pyglet
from app_state import AppState
from rules import RuleManager
from ui_prints import (
    gaide, print_help, print_rule, 
    print_settings, print_patterns, print_message,
    print_preset_info, print_input
)


class ResultProcessor:
    """Обрабатывает результаты выполнения команд"""
    
    def __init__(self, callbacks=None):
        self.callbacks = callbacks or {}
    
    def process(self, result_type, data):
        """Обрабатывает результат команды"""
        if result_type == 'reset' and 'random_grid' in self.callbacks:
            AppState.force_redraw = True
            self.callbacks['random_grid'](AppState.random_density)
            return True

        elif result_type == 'pattern_apply' and 'create_pattern' in self.callbacks:
            self.callbacks['create_pattern'](4)  # 4 - параметр для create_pattern
            return True

        elif result_type == 'clear' and 'clear_grid' in self.callbacks:
            AppState.force_redraw = True
            self.callbacks['clear_grid']()
            return True
            
        elif result_type == 'toggle_fullscreen' and AppState.window:
            AppState.window.set_fullscreen(not AppState.window.fullscreen)
            return True
            
        elif result_type == 'vsync_changed':
            AppState.vsync_enabled = data.get('vsync_enabled', False)
            if AppState.window:
                AppState.window.set_vsync(AppState.vsync_enabled)
            print_message(data.get('message', ''))
            return True
            
        elif result_type == 'pause' and 'toggle_pause' in self.callbacks:
            self.callbacks['toggle_pause']()
            return True
            
        elif result_type == 'next_frame':
            AppState.single_step = True
            return True
            
        elif result_type == 'exit':
            print("exit")
            pyglet.app.exit()
            return False
            
        elif result_type == 'help':
            gaide()
            return False
            
        elif result_type == 'navigate':
            new_input = data.get('new_input', '')
            if new_input:
                AppState.current_input = new_input
                AppState.input_buffer = ""
                self._show_menu_info(new_input)
            return False
            
        elif result_type == 'ui_toggle':
            AppState.ui_visible = not AppState.ui_visible
            print_message(f"UI {'shown' if AppState.ui_visible else 'hidden'}")
            return True
            
        elif result_type == 'next_preset':
            preset_count = RuleManager.get_preset_count()
            AppState.preset_index = (AppState.preset_index % preset_count) + 1
            success = RuleManager.load_preset(AppState.preset_index)
            if success:
                print_help()
                preset = RuleManager.get_preset(AppState.preset_index)
                print_preset_info(AppState.preset_index, preset.name, action="Next preset")
                print_rule()
            return False
            
        elif result_type == 'prev_preset':
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
            return False
            
        elif result_type == 'mode1' and 'resize_grid_fast' in self.callbacks:
            self.callbacks['resize_grid_fast'](
                int(AppState.window_width / AppState.cell_size),
                int(AppState.window_height / AppState.cell_size),
                mode1=AppState.render_mode_active,
                mode2=AppState.render_mode_inactive
            )
            return True
            
        elif result_type == 'mode2' and 'resize_grid_fast' in self.callbacks:
            self.callbacks['resize_grid_fast'](
                int(AppState.window_width / AppState.cell_size),
                int(AppState.window_height / AppState.cell_size),
                mode1=AppState.render_mode_active,
                mode2=AppState.render_mode_inactive
            )
            return True
            
        elif result_type == 'pattern_apply' and 'create_pattern' in self.callbacks:
            self.callbacks['create_pattern'](4)
            return True
            
        elif result_type == 'fps_changed' and 'update_fps_settings' in self.callbacks:
            self.callbacks['update_fps_settings']()
            return True
            
        elif result_type == 'cell_size_changed' and 'create_grid' in self.callbacks:
            self.callbacks['create_grid']()
            return True
        
        return False
    
    def _show_menu_info(self, new_input):
        """Показывает информацию о меню"""
        if new_input == "r":
            print_help()
            print_rule()
            print_input(AppState.current_input, AppState.input_buffer)
        elif new_input == "s":
            print_help()
            print_settings(AppState.target_fps, AppState.vsync_enabled,
                         AppState.cell_size, AppState.random_density)
            print_input(AppState.current_input, AppState.input_buffer)
        elif new_input == "p":
            print_help()
            print_patterns(AppState.patterns_type, AppState.patterns_size,
                         AppState.patterns_second_value)
            print_input(AppState.current_input, AppState.input_buffer)
        elif new_input == "r b":
            print_help()
            print_rule()
            print_input(AppState.current_input, AppState.input_buffer)
        elif new_input == "r s":
            print_help()
            print_rule()
            print_input(AppState.current_input, AppState.input_buffer)
        elif new_input == "r p":
            print_help()
            print_rule()
            print_input(AppState.current_input, AppState.input_buffer)
        elif new_input == "s f":
            print_help()
            print_settings(AppState.target_fps, AppState.vsync_enabled,
                        AppState.cell_size, AppState.random_density)
            print_input(AppState.current_input, AppState.input_buffer) 
        elif new_input == "s z":
            print_help()
            print_settings(AppState.target_fps, AppState.vsync_enabled,
                         AppState.cell_size, AppState.random_density)
            print_input(AppState.current_input, AppState.input_buffer)
        elif new_input == "s d":
            print_help()
            print_settings(AppState.target_fps, AppState.vsync_enabled,
                         AppState.cell_size, AppState.random_density)
            print_input(AppState.current_input, AppState.input_buffer)
        elif new_input == "s r":
            print_help()
            print_settings(AppState.target_fps, AppState.vsync_enabled,
                         AppState.cell_size, AppState.random_density)
            print_input(AppState.current_input, AppState.input_buffer)
        elif new_input == "s r a":
            print_help()
            print_input(AppState.current_input, AppState.input_buffer)
        elif new_input == "s r n":
            print_help()
            print_input(AppState.current_input, AppState.input_buffer)
        elif new_input == "p s":
            print_help()
            print_patterns(AppState.patterns_type, AppState.patterns_size,
                         AppState.patterns_second_value)
            print_input(AppState.current_input, AppState.input_buffer)
        elif new_input == "p v":
            print_help()
            print_patterns(AppState.patterns_type, AppState.patterns_size,
                         AppState.patterns_second_value)
            print_input(AppState.current_input, AppState.input_buffer)