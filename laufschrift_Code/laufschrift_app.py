import warnings
warnings.filterwarnings("ignore")

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import sys
import logging

logging.getLogger('werkzeug').setLevel(logging.ERROR)

import pygame
import time
from flask import Flask, render_template, request, jsonify
import threading
from urllib.parse import unquote
import ctypes
import subprocess
import json
import atexit

# =============================================================================
# Windows API Konstanten
# =============================================================================

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Window Position Flags
HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_SHOWWINDOW = 0x0040
SWP_NOACTIVATE = 0x0010

# ShowWindow Flags
SW_MINIMIZE = 6
SW_RESTORE = 9
SW_SHOW = 5
SW_SHOWNA = 8

# Power Management
ES_AWAYMODE_REQUIRED = 0x00000040
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002
ES_SYSTEM_REQUIRED = 0x00000001

# =============================================================================
# Pfade für EXE
# =============================================================================

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    template_folder = os.path.join(sys._MEIPASS, 'templates')
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    template_folder = 'templates'

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

app = Flask(__name__, template_folder=template_folder)

# =============================================================================
# Konfiguration
# =============================================================================

DEFAULT_CONFIG = {
    "text": "Willkommen!",
    "brightness": 230,
    "speed": 3,
    "red": 255,
    "green": 255,
    "blue": 255,
    "mode": "scroll",
    "repeat": 1,
    "duration": 10,
    "textsize": "mittel",
    "position": "oben",
    "direction": "rtl",
    "priority": "normal",
    "transparency": 0,
    "bar_height": 65,
    "port": 5000,
    "prevent_sleep_while_visible": False
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(loaded)
                return config
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_config():
    config = {
        "text": text,
        "brightness": brightness,
        "speed": speed,
        "red": red,
        "green": green,
        "blue": blue,
        "mode": mode,
        "repeat": repeat_count,
        "duration": duration,
        "textsize": textsize,
        "position": position,
        "direction": direction,
        "priority": priority,
        "transparency": transparency,
        "bar_height": bar_height,
        "port": port,
        "prevent_sleep_while_visible": prevent_sleep_while_visible
    }
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except:
        pass

config = load_config()

# =============================================================================
# Globale Variablen
# =============================================================================

text = config["text"]
brightness = config["brightness"]
speed = config["speed"]
red = config["red"]
green = config["green"]
blue = config["blue"]
mode = config["mode"]
repeat_count = config["repeat"]
duration = config["duration"]
textsize = config["textsize"]
position = config["position"]
direction = config["direction"]
priority = config["priority"]
transparency = config["transparency"]
bar_height = config["bar_height"]
port = config["port"]
prevent_sleep_while_visible = config.get("prevent_sleep_while_visible", False)

is_visible = False
is_paused = False
is_minimized = True
running = True
hwnd = None
screen = None
clock = None
current_window_position = None
power_keep_awake_active = False

# Bildschirmgröße
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)


def allow_windows_sleep():
    """Gibt eventuelle Wake-Requests frei, damit Bildschirm/PC schlafen duerfen."""
    global power_keep_awake_active
    try:
        kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    except Exception:
        pass
    power_keep_awake_active = False


def prevent_windows_sleep():
    """Verhindert optional waehrend aktiver Anzeige den Sleep-Modus."""
    global power_keep_awake_active
    try:
        kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
        )
        power_keep_awake_active = True
    except Exception:
        pass


def update_power_state():
    """Synchronisiert den Windows-Energiesparstatus mit der aktuellen Anzeige."""
    if is_visible and prevent_sleep_while_visible:
        prevent_windows_sleep()
    else:
        allow_windows_sleep()


atexit.register(allow_windows_sleep)

# =============================================================================
# Fenster-Funktionen - IMMER IM VORDERGRUND
# =============================================================================

def get_y_position():
    """Berechnet Y-Position basierend auf Position-String."""
    global position, SCREEN_HEIGHT, bar_height
    if position == "unten":
        return SCREEN_HEIGHT - bar_height
    elif position == "mitte":
        return (SCREEN_HEIGHT - bar_height) // 2
    return 0

def force_foreground(hwnd):
    """Erzwingt das Fenster in den absoluten Vordergrund."""
    if not hwnd:
        return
    
    # Methode 1: SetWindowPos mit TOPMOST
    y = get_y_position()
    user32.SetWindowPos(
        hwnd, 
        HWND_TOPMOST,
        0, y, SCREEN_WIDTH, bar_height,
        SWP_SHOWWINDOW
    )
    
    # Methode 2: Fenster aktivieren
    user32.ShowWindow(hwnd, SW_RESTORE)
    user32.ShowWindow(hwnd, SW_SHOW)
    
    # Methode 3: Fokus setzen
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    
    # Methode 4: Nochmal TOPMOST setzen (doppelt hält besser)
    user32.SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        0, y, SCREEN_WIDTH, bar_height,
        SWP_SHOWWINDOW
    )

def create_window():
    """Erstellt das Pygame-Fenster an der richtigen Position."""
    global screen, hwnd, clock, current_window_position
    
    y = get_y_position()
    current_window_position = position
    
    # Fensterposition VOR dem Erstellen setzen
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'0,{y}'
    
    # Pygame initialisieren falls noch nicht geschehen
    if not pygame.get_init():
        pygame.init()
    
    # Display neu initialisieren
    pygame.display.quit()
    pygame.display.init()
    
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, bar_height), 
        pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWSURFACE
    )
    pygame.display.set_caption("Laufschrift")
    
    if clock is None:
        clock = pygame.time.Clock()
    
    # Kurz warten damit Windows das Fenster erstellt
    time.sleep(0.1)
    
    # Handle holen
    hwnd = pygame.display.get_wm_info()['window']
    
    # Fenster in den ABSOLUTEN Vordergrund bringen
    force_foreground(hwnd)
    
    # Transparenz setzen
    set_transparency_level(transparency)

def init_pygame():
    """Initialisiert Pygame beim Start."""
    global clock
    pygame.init()
    clock = pygame.time.Clock()
    create_window()

def minimize_window():
    """Fenster minimieren."""
    global hwnd
    if hwnd:
        user32.ShowWindow(hwnd, SW_MINIMIZE)

def restore_window():
    """Fenster wiederherstellen und in den Vordergrund bringen."""
    global current_window_position, hwnd
    
    # Prüfen ob Position geändert wurde
    if current_window_position != position:
        # Fenster neu erstellen an neuer Position
        create_window()
    else:
        # Fenster in den Vordergrund bringen
        if hwnd:
            force_foreground(hwnd)
            set_transparency_level(transparency)

def set_transparency_level(percent):
    """Setzt die Fenstertransparenz."""
    global hwnd
    if not hwnd:
        return
    
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x80000
    LWA_ALPHA = 2
    
    style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED)
    
    alpha = int(255 * (100 - percent) / 100)
    alpha = max(20, min(255, alpha))
    
    user32.SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA)

def keep_on_top():
    """Hält das Fenster während der Anzeige im Vordergrund."""
    global hwnd
    if hwnd:
        y = get_y_position()
        user32.SetWindowPos(
            hwnd,
            HWND_TOPMOST,
            0, y, SCREEN_WIDTH, bar_height,
            SWP_SHOWWINDOW | SWP_NOACTIVATE
        )

# =============================================================================
# Text-Funktionen
# =============================================================================

def get_font():
    sizes = {"klein": 36, "mittel": 50, "gross": 72}
    return pygame.font.SysFont("Arial", sizes.get(textsize, 50), bold=True)

def get_color():
    factor = brightness / 255.0
    return (
        min(255, int(red * factor)),
        min(255, int(green * factor)),
        min(255, int(blue * factor))
    )

def display_text_scroll():
    """Scrollender Text."""
    global is_visible, screen, clock
    
    font = get_font()
    color = get_color()
    text_surface = font.render(text, True, color)
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    y = (bar_height - text_height) // 2
    
    background = pygame.Surface((SCREEN_WIDTH, bar_height))
    background.fill((0, 0, 0))
    
    # Frame-Counter für periodisches TOPMOST
    frame_count = 0
    
    for rep in range(repeat_count):
        if not is_visible:
            return
        
        if direction == "rtl":
            x = float(SCREEN_WIDTH)
            speed_dir = -1
        else:
            x = float(-text_width)
            speed_dir = 1
        
        last_time = pygame.time.get_ticks()
        
        while is_visible:
            current_time = pygame.time.get_ticks()
            delta = (current_time - last_time) / 1000.0
            last_time = current_time
            
            if is_paused:
                clock.tick(30)
                last_time = pygame.time.get_ticks()
                continue
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            screen.blit(background, (0, 0))
            screen.blit(text_surface, (int(x), y))
            pygame.display.flip()
            
            # Alle 30 Frames: Fenster im Vordergrund halten
            frame_count += 1
            if frame_count >= 30:
                keep_on_top()
                frame_count = 0
            
            pixels_per_second = speed * 100
            x += speed_dir * pixels_per_second * delta
            
            if direction == "rtl" and x < -text_width:
                break
            if direction == "ltr" and x > SCREEN_WIDTH:
                break
            
            clock.tick(60)
        
        if rep < repeat_count - 1 and is_visible:
            time.sleep(0.2)
    
    is_visible = False

def display_text_static():
    """Statischer Text."""
    global is_visible, screen, clock
    
    font = get_font()
    color = get_color()
    text_surface = font.render(text, True, color)
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    
    x = (SCREEN_WIDTH - text_width) // 2
    y = (bar_height - text_height) // 2
    
    frame = pygame.Surface((SCREEN_WIDTH, bar_height))
    frame.fill((0, 0, 0))
    frame.blit(text_surface, (x, y))
    
    frame_count = 0
    
    for rep in range(repeat_count):
        if not is_visible:
            return
        
        start_time = time.time()
        
        while is_visible and (time.time() - start_time) < duration:
            if is_paused:
                start_time += 0.033
                clock.tick(30)
                continue
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            screen.blit(frame, (0, 0))
            pygame.display.flip()
            
            # Alle 30 Frames: Fenster im Vordergrund halten
            frame_count += 1
            if frame_count >= 30:
                keep_on_top()
                frame_count = 0
            
            clock.tick(30)
        
        if rep < repeat_count - 1 and is_visible:
            time.sleep(0.2)
    
    is_visible = False

def display_text():
    if mode == "scroll":
        display_text_scroll()
    else:
        display_text_static()

# =============================================================================
# Pygame Haupt-Loop
# =============================================================================

def pygame_loop():
    global running, is_visible, is_minimized

    allow_windows_sleep()
    
    init_pygame()
    time.sleep(0.3)
    minimize_window()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        if is_visible:
            if is_minimized:
                restore_window()
                is_minimized = False
                time.sleep(0.1)
            update_power_state()
            display_text()
            update_power_state()
        else:
            if screen:
                screen.fill((0, 0, 0))
                pygame.display.flip()
            if not is_minimized:
                minimize_window()
                is_minimized = True
            update_power_state()
            time.sleep(0.05)
    
    allow_windows_sleep()
    pygame.quit()

# =============================================================================
# Flask Routes
# =============================================================================

@app.route('/', methods=['GET', 'POST'])
def index():
    global text, brightness, speed, red, green, blue
    global mode, repeat_count, duration, textsize, position
    global direction, priority, transparency, is_visible, prevent_sleep_while_visible
    
    if request.method == 'POST':
        text = request.form.get('text', text)
        brightness = int(request.form.get('brightness', brightness))
        speed = int(request.form.get('speed', speed))
        red = int(request.form.get('red', red))
        green = int(request.form.get('green', green))
        blue = int(request.form.get('blue', blue))
        mode = request.form.get('mode', mode)
        repeat_count = int(request.form.get('repeat', repeat_count))
        duration = int(request.form.get('duration', duration))
        textsize = request.form.get('textsize', textsize)
        position = request.form.get('position', position)
        direction = request.form.get('direction', direction)
        priority = request.form.get('priority', priority)
        transparency = int(request.form.get('transparency', transparency))
        prevent_sleep_while_visible = request.form.get('prevent_sleep_while_visible', '0').lower() in ['1', 'true', 'on', 'yes']
        is_visible = True
        update_power_state()
        save_config()
        return "OK"
    
    return render_template('index.html',
        text=text, brightness=brightness, speed=speed,
        red=red, green=green, blue=blue, mode=mode,
        repeat=repeat_count, duration=duration, textsize=textsize,
        position=position, direction=direction, priority=priority,
        transparency=transparency,
        prevent_sleep_while_visible=prevent_sleep_while_visible
    )

# ✅ NEU: POST /text (für lange Texte - KEINE Limits!)
@app.route('/text', methods=['POST'])
def api_text_post():
    global text, is_visible
    
    # Text aus POST-Body lesen
    text = request.form.get('text', '') or request.form.get('value', '')
    
    if not text:
        # Falls JSON gesendet wurde
        try:
            json_data = request.get_json(silent=True)
            if json_data:
                text = json_data.get('text', '') or json_data.get('value', '')
        except:
            pass
    
    if text:
        is_visible = True
        update_power_state()
        save_config()
        return f"OK: {len(text)} chars received"
    
    return "Error: No text provided", 400

# ✅ NEU: GET /text?value=... (Query-Parameter, bis ~2000 Zeichen)
@app.route('/text', methods=['GET'])
def api_text_query():
    global text, is_visible
    
    text = request.args.get('value', '') or request.args.get('text', '')
    
    if text:
        is_visible = True
        update_power_state()
        save_config()
        return f"OK: {len(text)} chars"
    
    return "Error: Use /text?value=YourText or POST /text", 400

# Alte Methode: GET /text/... (Fallback, limitiert bei langen URLs)
@app.route('/text/<path:new_text>')
def api_text_path(new_text):
    global text, is_visible
    text = unquote(new_text)
    is_visible = True
    update_power_state()
    return "OK"

@app.route('/brightness/<int:val>')
def api_brightness(val):
    global brightness
    brightness = max(0, min(255, val))
    save_config()
    return "OK"

@app.route('/speed/<int:val>')
def api_speed(val):
    global speed
    speed = max(1, min(15, val))
    save_config()
    return "OK"

@app.route('/red/<int:val>')
def api_red(val):
    global red
    red = max(0, min(255, val))
    save_config()
    return "OK"

@app.route('/green/<int:val>')
def api_green(val):
    global green
    green = max(0, min(255, val))
    save_config()
    return "OK"

@app.route('/blue/<int:val>')
def api_blue(val):
    global blue
    blue = max(0, min(255, val))
    save_config()
    return "OK"

@app.route('/mode/<string:val>')
def api_mode(val):
    global mode
    if val.lower() in ["scroll", "static"]:
        mode = val.lower()
        save_config()
        return "OK"
    return "Fehler", 400

@app.route('/repeat/<int:val>')
def api_repeat(val):
    global repeat_count
    repeat_count = max(1, min(10, val))
    save_config()
    return "OK"

@app.route('/duration/<int:val>')
def api_duration(val):
    global duration
    duration = max(1, min(300, val))
    save_config()
    return "OK"

@app.route('/textsize/<string:val>')
def api_textsize(val):
    global textsize
    if val.lower() in ["klein", "mittel", "gross"]:
        textsize = val.lower()
        save_config()
        return "OK"
    return "Fehler", 400

@app.route('/position/<string:val>')
def api_position(val):
    global position
    if val.lower() in ["oben", "mitte", "unten"]:
        position = val.lower()
        save_config()
        return "OK"
    return "Fehler", 400

@app.route('/direction/<string:val>')
def api_direction(val):
    global direction
    if val.lower() in ["ltr", "rtl"]:
        direction = val.lower()
        save_config()
        return "OK"
    return "Fehler", 400

@app.route('/priority/<string:val>')
def api_priority(val):
    global priority
    if val.lower() in ["normal", "hoch", "kritisch"]:
        priority = val.lower()
        save_config()
        return "OK"
    return "Fehler", 400

@app.route('/transparency/<int:val>')
def api_transparency(val):
    global transparency
    transparency = max(0, min(95, val))
    save_config()
    return "OK"

@app.route('/pause')
def api_pause():
    global is_paused
    is_paused = True
    return "OK"

@app.route('/resume')
def api_resume():
    global is_paused
    is_paused = False
    return "OK"

@app.route('/shutdown')
def api_shutdown():
    def do_shutdown():
        time.sleep(3)
        if os.name == 'nt':
            subprocess.call(['shutdown', '/s', '/t', '1'])
        else:
            subprocess.call(['shutdown', '-h', 'now'])
    threading.Thread(target=do_shutdown, daemon=True).start()
    return "OK"

@app.route('/sleepmode/<string:val>')
def api_sleepmode(val):
    global prevent_sleep_while_visible
    prevent_sleep_while_visible = val.lower() in ['on', '1', 'true', 'yes']
    update_power_state()
    save_config()
    return jsonify({
        'prevent_sleep_while_visible': prevent_sleep_while_visible
    })

@app.route('/status')
def api_status():
    return jsonify({
        "text": text, "brightness": brightness, "speed": speed,
        "red": red, "green": green, "blue": blue, "mode": mode,
        "repeat": repeat_count, "duration": duration, "textsize": textsize,
        "position": position, "direction": direction, "priority": priority,
        "transparency": transparency,
        "is_visible": is_visible,
        "is_paused": is_paused,
        "prevent_sleep_while_visible": prevent_sleep_while_visible
    })

# =============================================================================
# Start
# =============================================================================

def start_flask():
    app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False, threaded=True)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    pygame_loop()
    save_config()