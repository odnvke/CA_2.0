# statistics.py (добавляем недостающие функции)
import time
from collections import deque

# Глобальные переменные статистики
frame_count = 0
fps = 0
fps_frame_count = 0
fps_last_time = time.time()
start_time = time.time()
last_ui_update = 0
ui_update_interval = 0.3

# Тайминги для текущего кадра
current_frame_timings = {'total': 0, 'grid': 0, 'render': 0, 'ui_update': 0}
frame_start_time = 0
timing_history = deque(maxlen=60)

def start_frame():
    """Начало измерения времени кадра"""
    global frame_start_time
    frame_start_time = time.time()

def end_frame():
    """Завершение измерения времени кадра"""
    global current_frame_timings
    frame_time = (time.time() - frame_start_time) * 1000
    current_frame_timings['total'] = frame_time
    
    # Добавляем в историю
    timing_history.append(current_frame_timings.copy())
    
    # Сбрасываем для следующего кадра

def update_fps():
    global fps, fps_frame_count, fps_last_time, frame_count
    frame_count += 1
    fps_frame_count += 1
    
    current_time = time.time()
    if current_time - fps_last_time >= 0.3:
        fps = fps_frame_count / (current_time - fps_last_time)
        fps_frame_count = 0
        fps_last_time = current_time
        return True
    return False

def should_update_ui():
    global last_ui_update
    current_time = time.time()
    if current_time - last_ui_update >= ui_update_interval:
        last_ui_update = current_time
        return True
    return False

def start_timing():
    return time.time()

def end_timing(start_time):
    return (time.time() - start_time) * 1000

def set_timing(timing_type, duration):
    current_frame_timings[timing_type] = duration

def get_stats():
    return {
        'fps': fps,
        'frame_count': frame_count,
        'total_time': time.time() - start_time,
        'timings': current_frame_timings.copy()
    }

def get_avg_timing(timing_type):
    if not timing_history:
        return 0
    return sum(t[timing_type] for t in timing_history) / len(timing_history)