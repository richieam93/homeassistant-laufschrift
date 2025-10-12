import pygame
import time
from flask import Flask, render_template, request
import threading
from urllib.parse import unquote
import ctypes  # Für Fenster-Manipulation unter Windows
import os      # Für Umgebungsvariablen
import subprocess # Für das Herunterfahren

app = Flask(__name__)

# Fensterposition festlegen (vor der Pygame-Initialisierung!)
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'  # Obere linke Ecke

# Pygame-Initialisierung
pygame.init()
width, height = 1600, 65
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Laufschrift")
black = (0, 0, 0)
white = (255, 255, 255)
font = pygame.font.Font(None, 36)

# Globale Variablen
text = "Hallo, Welt!"
brightness = 230
speed = 3
red = 255
green = 255
blue = 255
is_visible = False
is_minimized = True  # Zustand des Fensters: minimiert oder nicht
hwnd = pygame.display.get_wm_info()['window'] # Handle für das Fenster

# Funktionen für Fenster-Manipulation (Windows-spezifisch)
def minimize_window():
    global hwnd
    ctypes.windll.user32.ShowWindow(hwnd, 6)  # SW_MINIMIZE = 6

def restore_window():
    global hwnd
    ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE = 9

def display_text():
    global text, brightness, speed, red, green, blue, is_visible, is_minimized
    text_color = (red, green, blue)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.x = width
    text_rect.y = height // 2 - text_rect.height // 2

    while text_rect.x > -text_rect.width:
        if not is_visible:
            break
        screen.fill(black)
        screen.blit(text_surface, text_rect)
        text_rect.x -= speed
        pygame.display.flip()
        time.sleep(0.02)
    
    is_visible = False

def pygame_loop():
    global running, is_visible, is_minimized
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global flask_thread
                flask_thread.join()
                running = False
                break

        if is_visible:
            if is_minimized:
                restore_window() # Fenster wiederherstellen, wenn es minimiert ist
                is_minimized = False
            display_text()
        else:
            screen.fill(black)
            pygame.display.flip()
            if not is_minimized:
                minimize_window() # Fenster minimieren, wenn es nicht sichtbar ist
                is_minimized = True
            time.sleep(0.1)

    pygame.quit()

@app.route('/text/<string:new_text>')
def update_text(new_text):
    global text, is_visible
    text = unquote(new_text)
    is_visible = True
    return f"Text aktualisiert auf: {text}"

@app.route('/brightness/<int:new_brightness>')
def update_brightness(new_brightness):
    global brightness
    brightness = new_brightness
    return f"Helligkeit aktualisiert auf: {brightness}"

@app.route('/speed/<int:new_speed>')
def update_speed(new_speed):
    global speed
    speed = new_speed
    return f"Geschwindigkeit aktualisiert auf: {speed}"

@app.route('/red/<int:new_red>')
def update_red(new_red):
    global red
    red = new_red
    return f"Rot aktualisiert auf: {red}"

@app.route('/green/<int:new_green>')
def update_green(new_green):
    global green
    green = new_green
    return f"Grün aktualisiert auf: {green}"

@app.route('/blue/<int:new_blue>')
def update_blue(new_blue):
    global blue
    blue = new_blue
    return f"Blau aktualisiert auf: {blue}"

@app.route('/', methods=['GET', 'POST'])
def index():
    global text, brightness, speed, red, green, blue, is_visible
    if request.method == 'POST':
        text = request.form['text']
        brightness = int(request.form['brightness'])
        speed = int(request.form['speed'])
        red = int(request.form['red'])
        green = int(request.form['green'])
        blue = int(request.form['blue'])
        is_visible = True # Zeige die Anzeige, wenn ein neuer Text eintrifft
        return "Laufschrift aktualisiert!"
    return render_template('index.html', text=text, brightness=brightness, speed=speed, red=red, green=green, blue=blue)

@app.route('/shutdown')
def shutdown():
    """Route zum Herunterfahren des Computers."""
    def shutdown_pc():
        # Je nach Betriebssystem unterschiedliche Befehle verwenden
        if os.name == 'nt':  # Windows
            subprocess.call(['shutdown', '/s', '/t', '1'])
        else:  # Linux oder macOS
            subprocess.call(['shutdown', '-h', 'now'])
    
    # Starte das Herunterfahren in einem separaten Thread, um die Antwort zurückzugeben
    shutdown_thread = threading.Thread(target=shutdown_pc)
    shutdown_thread.daemon = True
    shutdown_thread.start()
    
    return "Herunterfahren wird initiiert..."

def start_flask():
    app.run(debug=False, host='0.0.0.0', use_reloader=False)

if __name__ == '__main__':
    # Starte Pygame in einem separaten Thread
    pygame_thread = threading.Thread(target=pygame_loop)
    pygame_thread.daemon = True

    # Starte Flask in einem separaten Thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Fenster minimieren bevor Pygame Loop startet
    time.sleep(1)
    minimize_window()

    # Starte Pygame-Thread
    pygame_thread.start()

    # Verhindere, dass sich das Hauptprogramm beendet, solange Pygame läuft, aber blockiere die Pygame-Ausgabe nicht
    while pygame_thread.is_alive():
        pygame.event.pump() # Erlaube Pygame, Ereignisse zu verarbeiten
        time.sleep(0.1)