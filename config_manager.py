# config_manager.py
import json
import os
from pathlib import Path
from typing import Dict, Any
from app_state import AppState
from rules import RuleManager

DEFAULT_CONFIG = {
    "window": {
        "width": 500,
        "height": 500,
        "resizeble": True
    },
    "simulation": {
        "target_fps": 20,
        "vsync_enabled": False,
        "cell_size": 3,
        "random_density": 30,
        "preset_index": 1
    },
    "rendering": {
        "render_mode_active": 5,
        "render_mode_inactive": 0,
        "ui_visible": True
    },
    "patterns": {
        "patterns_type": 1,
        "patterns_size": 11.0,
        "patterns_second_value": 1.0
    }
}

CONFIG_FILE = "config.json"

def load_config() -> Dict[str, Any]:
    """Загрузить конфигурацию из JSON файла"""
    config_path = Path(CONFIG_FILE)
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"Конфигурация загружена из {CONFIG_FILE}")
            return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка загрузки конфигурации: {e}")
            print("Используются настройки по умолчанию")
            return DEFAULT_CONFIG.copy()
    else:
        print(f"Файл конфигурации {CONFIG_FILE} не найден")
        print("Создан файл с настройками по умолчанию")
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any] = None) -> bool:
    """Сохранить текущую конфигурацию в JSON файл"""
    if config is None:
        config = get_current_config()
    
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"Конфигурация сохранена в {CONFIG_FILE}")
        return True
    except IOError as e:
        print(f"Ошибка сохранения конфигурации: {e}")
        return False

def get_current_config() -> Dict[str, Any]:
    """Получить текущую конфигурацию из AppState"""
    return {
        "window": {
            "width": AppState.window_width,
            "height": AppState.window_height,
            "resizeble": AppState.lock_window
        },
        "simulation": {
            "target_fps": AppState.target_fps,
            "vsync_enabled": AppState.vsync_enabled,
            "cell_size": AppState.cell_size,
            "random_density": AppState.random_density,
            "preset_index": AppState.preset_index
        },
        "rendering": {
            "render_mode_active": AppState.render_mode_active,
            "render_mode_inactive": AppState.render_mode_inactive,
            "ui_visible": AppState.ui_visible
        },
        "patterns": {
            "patterns_type": AppState.patterns_type,
            "patterns_size": AppState.patterns_size,
            "patterns_second_value": AppState.patterns_second_value
        }
    }

def apply_config(config: Dict[str, Any]) -> None:
    """Применить конфигурацию к AppState"""
    try:
        # Основные настройки окна
        AppState.window_width = config.get("window", {}).get("width", DEFAULT_CONFIG["window"]["width"])
        AppState.window_height = config.get("window", {}).get("height", DEFAULT_CONFIG["window"]["height"])
        AppState.lock_window = config.get("window", {}).get("resizeble", DEFAULT_CONFIG["window"]["resizeble"])

        # Настройки симуляции
        sim_config = config.get("simulation", {})
        AppState.target_fps = sim_config.get("target_fps", DEFAULT_CONFIG["simulation"]["target_fps"])
        AppState.vsync_enabled = sim_config.get("vsync_enabled", DEFAULT_CONFIG["simulation"]["vsync_enabled"])
        AppState.cell_size = sim_config.get("cell_size", DEFAULT_CONFIG["simulation"]["cell_size"])
        AppState.random_density = sim_config.get("random_density", DEFAULT_CONFIG["simulation"]["random_density"])
        AppState.preset_index = sim_config.get("preset_index", DEFAULT_CONFIG["simulation"]["preset_index"])
        
        # Загружаем пресет правил
        RuleManager.load_preset(AppState.preset_index)
        
        # Настройки рендеринга
        render_config = config.get("rendering", {})
        AppState.render_mode_active = render_config.get("render_mode_active", DEFAULT_CONFIG["rendering"]["render_mode_active"])
        AppState.render_mode_inactive = render_config.get("render_mode_inactive", DEFAULT_CONFIG["rendering"]["render_mode_inactive"])
        AppState.ui_visible = render_config.get("ui_visible", DEFAULT_CONFIG["rendering"]["ui_visible"])
        
        # Настройки паттернов
        patterns_config = config.get("patterns", {})
        AppState.patterns_type = patterns_config.get("patterns_type", DEFAULT_CONFIG["patterns"]["patterns_type"])
        AppState.patterns_size = patterns_config.get("patterns_size", DEFAULT_CONFIG["patterns"]["patterns_size"])
        AppState.patterns_second_value = patterns_config.get("patterns_second_value", DEFAULT_CONFIG["patterns"]["patterns_second_value"])
        
        print("Конфигурация успешно применена")
        
    except Exception as e:
        print(f"Ошибка применения конфигурации: {e}")
        print("Используются настройки по умолчанию")
        apply_config(DEFAULT_CONFIG)

def reset_to_defaults() -> None:
    """Сбросить настройки к значениям по умолчанию"""
    apply_config(DEFAULT_CONFIG)
    save_config(DEFAULT_CONFIG)
    print("Настройки сброшены к значениям по умолчанию")