# =============================
# 🔧 1. INITIAL CONFIGURATION
# =============================
import os
import json
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options

# Emojis for console logs
EMOJIS = {
    "start": "🟢",
    "step": "✔️",
    "done": "✅",
    "error": "❌",
    "pause": "⏸️"
}

# Constants
EDGE_DEBUG_PORT = 9222
EDGE_USER_DIR = r"C:\\ZedgeTemp"
EDGE_DRIVER_PATH = r"C:\\Zpython\\edgedriver_win64\\msedgedriver.exe"
START_URL = "https://jira.tools.digital.engie.com/browse/GET5-1132"
OUTPUT_FOLDER = r"C:\\Zpython\\OCR\\Salidas"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M")
OUTPUT_JSON = os.path.join(OUTPUT_FOLDER, f"jira_fields_{TIMESTAMP}.json")
OUTPUT_EXCEL = os.path.join(OUTPUT_FOLDER, f"jira_fields_{TIMESTAMP}.xlsx")

# =============================
# 🧱 2. UTILITY FUNCTIONS
# =============================
def print_step(number, message):
    print(f"{EMOJIS['step']} Step {number}: {message}")

def launch_edge_with_debug():
    print_step(1, "Launching Edge with remote debugging...")
    os.system(f"start msedge --remote-debugging-port={EDGE_DEBUG_PORT} --user-data-dir={EDGE_USER_DIR} {START_URL}")

def connect_to_edge():
    print_step(2, "Connecting to Edge instance")
    options = Options()
    options.debugger_address = f"localhost:{EDGE_DEBUG_PORT}"
    service = EdgeService(executable_path=EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)
    return driver

def extract_select_fields(driver):
    print_step(3, "Extracting standard <select> fields")
    selects = driver.find_elements(By.TAG_NAME, "select")
    data = []

    for sel in selects:
        try:
            field_id = sel.get_attribute("id")
            field_name = sel.get_attribute("name")
            field_label = sel.get_attribute("aria-label")
            selected = sel.get_attribute("value")
            options = [opt.text for opt in sel.find_elements(By.TAG_NAME, "option")]
            current_text = next((opt.text for opt in sel.find_elements(By.TAG_NAME, "option") if opt.get_attribute("value") == selected), selected)

            data.append({
                "Type": "Select",
                "Field ID": field_id,
                "Field Name": field_name,
                "Label": field_label,
                "Selected Option": current_text,
                "All Options": options
            })
        except Exception as e:
            print(f"{EMOJIS['error']} Error reading select: {e}")

    return data

def extract_multitag_fields(driver):
    print_step(4, "Extracting multi-tag fields")
    data = []
    multitag_containers = driver.find_elements(By.XPATH, "//div[contains(@aria-label, 'Component') or @role='listbox']")

    for container in multitag_containers:
        try:
            label = container.get_attribute("aria-label") or container.get_attribute("data-fieldname")
            selected_tags = container.find_elements(By.XPATH, ".//span[contains(@class,'lozenge') or contains(@class,'value')]")
            values = [tag.text.strip() for tag in selected_tags if tag.text.strip()]

            data.append({
                "Type": "MultiTag",
                "Label": label,
                "Selected Tags": values,
                "All Options": "(dynamic, not captured)"
            })
        except Exception as e:
            print(f"{EMOJIS['error']} Error reading multitag: {e}")

    return data

def save_outputs(data):
    print_step(5, f"Saving to JSON: {OUTPUT_JSON}")
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print_step(6, f"Saving to Excel: {OUTPUT_EXCEL}")
    df = pd.DataFrame(data)
    df.to_excel(OUTPUT_EXCEL, index=False)

    print(f"{EMOJIS['done']} Outputs saved successfully!")

# =============================
# ▶️ 4. EXECUTION ENTRY POINT
# =============================
def main():
    print(f"{EMOJIS['start']} Starting Sebas AI Field Sniffer for Edge (v2.0 with MultiTag)")
    launch_edge_with_debug()
    input(f"{EMOJIS['pause']} Press ENTER once you have logged in and opened the JIRA page...")

    try:
        driver = connect_to_edge()
        data = extract_select_fields(driver)
        data += extract_multitag_fields(driver)
        save_outputs(data)
        driver.quit()
    except Exception as e:
        print(f"{EMOJIS['error']} Unexpected error: {e}")

if __name__ == "__main__":
    main()
