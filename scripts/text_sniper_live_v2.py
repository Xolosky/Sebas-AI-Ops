# =============================
# 🔧 1. INITIAL CONFIGURATION
# =============================
import cv2
import numpy as np
import pytesseract
import keyboard
import os
import time
from datetime import datetime
from PIL import ImageGrab, Image
import subprocess
import ctypes
ctypes.windll.user32.SetProcessDPIAware()


# Emojis
EMOJIS = {
    "start": "🟢",
    "step": "✔️",
    "error": "❌",
    "done": "✅"
}

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Zpython\OCR\Tesseract-OCR\tesseract.exe"

# Output folder
OUTPUT_FOLDER = r"C:\Zpython\OCR\Salidas"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =============================
# 🧱 2. UTILITY FUNCTIONS
# =============================
def print_step(number, message):
    print(f"{EMOJIS['step']} Step {number}: {message}")

def open_txt_in_vscode(path):
    try:
        vscode_path = r"C:\Users\s.arevalo.munoz\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        subprocess.Popen([vscode_path, path])
    except Exception as e:
        print(f"{EMOJIS['error']} Failed to open VSCode: {e}")

def select_screen_area():
    print_step(1, "Select screen area with mouse (drag and release)")

    screen = np.array(ImageGrab.grab())
    clone = screen.copy()
    roi = [0, 0, 0, 0]
    cropping = [False]

    def mouse_crop(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            roi[0], roi[1] = x, y
            cropping[0] = True
        elif event == cv2.EVENT_LBUTTONUP:
            roi[2], roi[3] = x, y
            cropping[0] = False
            cv2.destroyAllWindows()

    cv2.namedWindow("Select Area", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Select Area", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("Select Area", mouse_crop)

    while cropping[0] or roi[2] == 0:
        cv2.imshow("Select Area", clone)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    x0, y0, x1, y1 = roi
    x0, x1 = sorted([x0, x1])
    y0, y1 = sorted([y0, y1])
    return screen[y0:y1, x0:x1]

def capture_and_extract_text():
    image = select_screen_area()
    if image is None or image.size == 0:
        print(f"{EMOJIS['error']} No area selected.")
        return None

    text = pytesseract.image_to_string(Image.fromarray(image)).strip()
    return text

# =============================
# 🚀 3. MAIN EXECUTION
# =============================
def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_FOLDER, f"text_capture_{timestamp}.txt")
    print(f"{EMOJIS['start']} Sebas AI Text Sniper V2 started")
    print_step(0, f"Output file: {output_file}")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("🧠 Sebas AI Text Sniper V2 Log\n")

    open_txt_in_vscode(output_file)
    print("🔁 Press Ctrl + Shift + C to capture | ESC to stop")

    while True:
        if keyboard.is_pressed("esc"):
            print(f"{EMOJIS['done']} Sniper stopped.")
            break
        if keyboard.is_pressed("ctrl+shift+c"):
            time.sleep(0.3)
            text = capture_and_extract_text()
            if text:
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"\n\n🔸 Fragmento ({datetime.now().strftime('%H:%M:%S')}):\n{text}\n")
                print(f"{EMOJIS['done']} Text captured and saved.")
            else:
                print(f"{EMOJIS['error']} No text detected.")

# =============================
# ▶️ 4. EXECUTION ENTRY POINT
# =============================
if __name__ == "__main__":
    main()
