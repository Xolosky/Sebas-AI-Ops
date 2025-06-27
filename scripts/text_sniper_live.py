# =============================
# 🔧 1. INITIAL CONFIGURATION
# =============================
import pytesseract
import pyautogui
import keyboard
import os
import time
from datetime import datetime
from PIL import ImageGrab
import subprocess

# Emojis
EMOJIS = {
    "start": "🟢",
    "step": "✔️",
    "error": "❌",
    "done": "✅"
}

# Tesseract path (actualizado)
pytesseract.pytesseract.tesseract_cmd = r"C:\Zpython\OCR\Tesseract-OCR\tesseract.exe"

# Output folder
OUTPUT_FOLDER = r"C:\Zpython\OCR\Salidas"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Timestamped output file
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, f"text_capture_{TIMESTAMP}.txt")

# =============================
# 🧱 2. UTILITY FUNCTIONS
# =============================
def print_step(number, message):
    print(f"{EMOJIS['step']} Step {number}: {message}")

def open_txt_in_vscode(path):
    try:
        print_step(1, f"Opening VSCode for: {path}")
        vscode_path = r"C:\Users\s.arevalo.munoz\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        subprocess.Popen([vscode_path, path])
    except Exception as e:
        print(f"{EMOJIS['error']} Failed to open VSCode: {e}")

def capture_text_and_append(path):
    print_step(2, "Waiting for selection and hotkey (Ctrl+Shift+C)...")
    keyboard.wait("ctrl+shift+c")
    time.sleep(0.3)

    image = ImageGrab.grabclipboard() or pyautogui.screenshot()

    print_step(3, "Extracting text using OCR...")
    text = pytesseract.image_to_string(image).strip()

    if text:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n\n🔸 Nuevo fragmento ({datetime.now().strftime('%H:%M:%S')}):\n")
            f.write(text)
        print(f"{EMOJIS['done']} Text added to file:")
        print(text)
    else:
        print(f"{EMOJIS['error']} No text recognized.")

# =============================
# 🚀 3. MAIN EXECUTION
# =============================
def main():
    print(f"{EMOJIS['start']} Sebas AI Live Text Sniper started")
    print_step(0, f"Output file: {OUTPUT_FILE}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("🧠 Sebas AI Text Sniper Log\n")

    open_txt_in_vscode(OUTPUT_FILE)

print("🔴 Press ESC to stop the sniper...")

while True:
    if keyboard.is_pressed("esc"):
        print(f"{EMOJIS['done']} Sebas AI Text Sniper stopped.")
        break
    capture_text_and_append(OUTPUT_FILE)


# =============================
# ▶️ 4. EXECUTION ENTRY POINT
# =============================
if __name__ == "__main__":
    main()
