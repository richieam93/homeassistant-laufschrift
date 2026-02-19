import pygame
import time
from flask import Flask, render_template, request, jsonify
import threading
from urllib.parse import unquote
import ctypes
import os
import subprocess
import json
import tkinter as tk
root = tk.Tk()
root.iconify() # Minimiert das Fenster sofort
app = Flask(__name__)

# =============================================================================
# Konfiguration
# =============================================================================

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "text": "Hallo, Welt!",
    "brightness": 230,
    "speed": 5,
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
    "bar_height": 80,
    "port": 5000
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        except:
            return DEFAULT_CONFIG.copy()
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
        "port": port
    }
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

# Lade Config
config = load_config()

# Globale Variablen
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

is_visible = False
is_paused = False
running = True
screen = None
hwnd = None

# Bildschirmgröße
user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)

print(f"Bildschirm: {SCREEN_WIDTH} x {SCREEN_HEIGHT}")

# =============================================================================
# Fenster-Funktionen (Windows API)
# =============================================================================

def get_y_position(pos):
    """Berechnet die Y-Position basierend auf Position-String."""
    if pos == "unten":
        return SCREEN_HEIGHT - bar_height
    elif pos == "mitte":
        return (SCREEN_HEIGHT - bar_height) // 2
    else:  # oben
        return 0

def create_window_at_position(pos):
    """Erstellt das Pygame-Fenster an der gewünschten Position."""
    global screen, hwnd
    
    y = get_y_position(pos)
    
    # Fensterposition VOR der Erstellung setzen
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'0,{y}'
    
    print(f"Erstelle Fenster bei Y={y} (Position: {pos})")
    
    # Pygame neu initialisieren wenn nötig
    if screen is not None:
        pygame.display.quit()
    
    pygame.display.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, bar_height), pygame.NOFRAME)
    pygame.display.set_caption("Laufschrift")
    
    # Handle holen
    time.sleep(0.1)
    hwnd = pygame.display.get_wm_info()['window']
    
    # Fenster in den Vordergrund bringen (TOPMOST)
    HWND_TOPMOST = -1
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    SWP_SHOWWINDOW = 0x0040
    
    ctypes.windll.user32.SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        0, 0, 0, 0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW
    )
    
    # Transparenz setzen
    set_transparency(transparency)
    
    return screen

def set_transparency(percent):
    """Setzt die Fenstertransparenz."""
    global hwnd
    if not hwnd:
        return
    
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x80000
    LWA_ALPHA = 2
    
    # Layered Style aktivieren
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED)
    
    # Alpha berechnen
    alpha = int(255 * (100 - percent) / 100)
    alpha = max(15, min(255, alpha))
    
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA)
    print(f"Transparenz: {percent}% (Alpha: {alpha})")

def minimize():
    """Fenster minimieren."""
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 6)

def show_window():
    """Fenster anzeigen (neu erstellen an richtiger Position)."""
    create_window_at_position(position)

# =============================================================================
# Text-Rendering
# =============================================================================

def get_font():
    sizes = {"klein": 40, "mittel": 60, "gross": 90}
    return pygame.font.Font(None, sizes.get(textsize, 60))

def get_color():
    factor = brightness / 255.0
    return (int(red * factor), int(green * factor), int(blue * factor))

def show_text():
    """Zeigt den Text an."""
    global is_visible, screen
    
    if screen is None:
        return
    
    font = get_font()
    color = get_color()
    text_surface = font.render(text, True, color)
    
    text_w = text_surface.get_width()
    text_h = text_surface.get_height()
    
    # Vertikale Zentrierung im Balken
    y = (bar_height - text_h) // 2
    
    for rep in range(repeat_count):
        if not is_visible:
            break
        
        if mode == "scroll":
            # SCROLL MODUS
            if direction == "rtl":
                x = SCREEN_WIDTH
                while x > -text_w and is_visible:
                    while is_paused and is_visible:
                        time.sleep(0.1)
                    screen.fill((0, 0, 0))
                    screen.blit(text_surface, (x, y))
                    pygame.display.flip()
                    x -= speed
                    time.sleep(0.015)
            else:
                x = -text_w
                while x < SCREEN_WIDTH and is_visible:
                    while is_paused and is_visible:
                        time.sleep(0.1)
                    screen.fill((0, 0, 0))
                    screen.blit(text_surface, (x, y))
                    pygame.display.flip()
                    x += speed
                    time.sleep(0.015)
        else:
            # STATISCH MODUS - Text ZENTRIERT
            x = (SCREEN_WIDTH - text_w) // 2
            y = (bar_height - text_h) // 2
            
            print(f"Statisch: Position ({x}, {y}), Textgröße ({text_w}x{text_h})")
            
            start = time.time()
            while time.time() - start < duration and is_visible:
                while is_paused and is_visible:
                    time.sleep(0.1)
                    start += 0.1
                screen.fill((0, 0, 0))
                screen.blit(text_surface, (x, y))
                pygame.display.flip()
                time.sleep(0.05)
        
        if rep < repeat_count - 1 and is_visible:
            time.sleep(0.3)
    
    is_visible = False

# =============================================================================
# Haupt-Loop
# =============================================================================

def main_loop():
    global running, is_visible, screen
    
    # Pygame initialisieren
    pygame.init()
    pygame.font.init()
    
    # Erstes Fenster erstellen (minimiert starten)
    create_window_at_position(position)
    time.sleep(0.3)
    minimize()
    
    minimized = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if is_visible:
            if minimized:
                # Fenster NEU erstellen an der richtigen Position
                show_window()
                minimized = False
            show_text()
        else:
            if screen:
                screen.fill((0, 0, 0))
                pygame.display.flip()
            if not minimized:
                minimize()
                minimized = True
            time.sleep(0.1)
    
    pygame.quit()

# =============================================================================
# Flask Routes
# =============================================================================

@app.route('/', methods=['GET', 'POST'])
def index():
    global text, brightness, speed, red, green, blue
    global mode, repeat_count, duration, textsize, position
    global direction, priority, transparency, is_visible
    
    message = None
    
    if request.method == 'POST':
        try:
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
            
            print(f"Neue Position: {position}")
            
            is_visible = True
            save_config()
            message = "✅ Text wird angezeigt!"
        except Exception as e:
            message = f"❌ Fehler: {str(e)}"
    
    return render_template('index.html',
        text=text, brightness=brightness, speed=speed,
        red=red, green=green, blue=blue, mode=mode,
        repeat=repeat_count, duration=duration, textsize=textsize,
        position=position, direction=direction, priority=priority,
        transparency=transparency, message=message
    )

@app.route('/text/<path:new_text>')
def api_text(new_text):
    global text, is_visible
    text = unquote(new_text)
    is_visible = True
    save_config()
    return f"OK: {text}"

@app.route('/brightness/<int:val>')
def api_brightness(val):
    global brightness
    brightness = max(0, min(255, val))
    save_config()
    return f"OK: {brightness}"

@app.route('/speed/<int:val>')
def api_speed(val):
    global speed
    speed = max(1, min(20, val))
    save_config()
    return f"OK: {speed}"

@app.route('/red/<int:val>')
def api_red(val):
    global red
    red = max(0, min(255, val))
    save_config()
    return f"OK: {red}"

@app.route('/green/<int:val>')
def api_green(val):
    global green
    green = max(0, min(255, val))
    save_config()
    return f"OK: {green}"

@app.route('/blue/<int:val>')
def api_blue(val):
    global blue
    blue = max(0, min(255, val))
    save_config()
    return f"OK: {blue}"

@app.route('/mode/<string:val>')
def api_mode(val):
    global mode
    val = val.lower()
    if val in ["scroll", "static"]:
        mode = val
        save_config()
        return f"OK: {mode}"
    return "Fehler", 400

@app.route('/repeat/<int:val>')
def api_repeat(val):
    global repeat_count
    repeat_count = max(1, min(10, val))
    save_config()
    return f"OK: {repeat_count}"

@app.route('/duration/<int:val>')
def api_duration(val):
    global duration
    duration = max(1, min(300, val))
    save_config()
    return f"OK: {duration}s"

@app.route('/textsize/<string:val>')
def api_textsize(val):
    global textsize
    val = val.lower()
    if val in ["klein", "mittel", "gross"]:
        textsize = val
        save_config()
        return f"OK: {textsize}"
    return "Fehler", 400

@app.route('/position/<string:val>')
def api_position(val):
    global position
    val = val.lower()
    if val in ["oben", "mitte", "unten"]:
        position = val
        save_config()
        print(f"Position geändert zu: {position}")
        return f"OK: {position}"
    return "Fehler", 400

@app.route('/direction/<string:val>')
def api_direction(val):
    global direction
    val = val.lower()
    if val in ["ltr", "rtl"]:
        direction = val
        save_config()
        return f"OK: {direction}"
    return "Fehler", 400

@app.route('/priority/<string:val>')
def api_priority(val):
    global priority
    val = val.lower()
    if val in ["normal", "hoch", "kritisch"]:
        priority = val
        save_config()
        return f"OK: {priority}"
    return "Fehler", 400

@app.route('/transparency/<int:val>')
def api_transparency(val):
    global transparency
    transparency = max(0, min(95, val))
    save_config()
    return f"OK: {transparency}%"

@app.route('/pause')
def api_pause():
    global is_paused
    is_paused = True
    return "Pausiert"

@app.route('/resume')
def api_resume():
    global is_paused
    is_paused = False
    return "Fortgesetzt"

@app.route('/shutdown')
def api_shutdown():
    def do_shutdown():
        time.sleep(3)
        subprocess.call(['shutdown', '/s', '/t', '1'])
    threading.Thread(target=do_shutdown, daemon=True).start()
    return "Shutdown in 3s..."

@app.route('/status')
def api_status():
    return jsonify({
        "text": text, "brightness": brightness, "speed": speed,
        "red": red, "green": green, "blue": blue, "mode": mode,
        "repeat": repeat_count, "duration": duration, "textsize": textsize,
        "position": position, "direction": direction, "priority": priority,
        "transparency": transparency, "is_visible": is_visible
    })

# =============================================================================
# Start
# =============================================================================

def run_flask():
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)

if __name__ == '__main__':
    print("=" * 60)
    print("  🖥️  LAUFSCHRIFT v2.2")
    print("=" * 60)
    print(f"  📺 Bildschirm:   {SCREEN_WIDTH} x {SCREEN_HEIGHT}")
    print(f"  📏 Balkenhöhe:   {bar_height}px")
    print(f"  🌐 Webinterface: http://localhost:{port}")
    print(f"  📍 Position:     {position}")
    print("=" * 60)
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    main_loop()
    
    save_config()
    print("Beendet.")