"""
compile_complete_report.py
Generates the publication-grade CSI1006 Mini Project Report:
1. MINI_PROJECT_REPORT_CSI1006.md (Markdown master)
2. MINI_PROJECT_REPORT_CSI1006.html (Academic print-ready HTML with A4 formatting)
3. MINI_PROJECT_REPORT_CSI1006.pdf (Compiled publication PDF via headless Chromium)
"""

import os
import sys
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"C:\Users\rarun\.gemini\antigravity\scratch\alt-digital-student-twin")
IMG_DIR = BASE_DIR / "report_images"

def get_image_base64(filepath):
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "rb") as f:
        data = f.read()
    ext = os.path.splitext(filepath)[1].lower().replace(".", "")
    if ext == "svg":
        mime = "image/svg+xml"
    elif ext in ["png", "jpg", "jpeg"]:
        mime = f"image/{ext}"
    else:
        mime = "image/png"
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def build_report_data():
    # Load all images as base64 for embedding directly into HTML and referencing in MD
    images = {
        "fig_3_1": get_image_base64(IMG_DIR / "fig_3_1_usecase_diagram.svg"),
        "fig_3_2": get_image_base64(IMG_DIR / "fig_3_2_data_flow_diagram.svg"),
        "fig_3_3": get_image_base64(IMG_DIR / "fig_3_3_state_transition.svg"),
        "fig_4_1": get_image_base64(IMG_DIR / "fig_4_1_system_architecture.svg"),
        "fig_4_2": get_image_base64(IMG_DIR / "fig_4_2_sequence_diagram.svg"),
        "fig_4_3": get_image_base64(IMG_DIR / "fig_4_3_class_diagram.svg"),
        "fig_7_1": get_image_base64(IMG_DIR / "fig_7_1_login_monolith.png"),
        "fig_7_2": get_image_base64(IMG_DIR / "fig_7_2_cohort_overview.png"),
        "fig_7_3": get_image_base64(IMG_DIR / "fig_7_3_student_twin.png"),
        "fig_7_4": get_image_base64(IMG_DIR / "fig_7_4_what_if_simulator.png"),
        "fig_7_5": get_image_base64(IMG_DIR / "fig_7_5_student_twin_at_risk.png"),
        "fig_7_6": get_image_base64(IMG_DIR / "fig_7_6_daily_checkin.png"),
        "fig_7_7": get_image_base64(IMG_DIR / "fig_7_7_cohort_analytics_scatter.png"),
        "fig_7_8": get_image_base64(IMG_DIR / "fig_7_8_feature_importance.png"),
        "fig_7_9": get_image_base64(IMG_DIR / "fig_7_9_all_students_table.png"),
        "fig_7_10": get_image_base64(IMG_DIR / "fig_7_10_assistant_chat.png"),
        "fig_7_11": get_image_base64(IMG_DIR / "fig_7_11_chat_simulation_card.png"),
        "fig_7_12": get_image_base64(IMG_DIR / "fig_7_12_about_and_model.png"),
        "fig_7_13": get_image_base64(IMG_DIR / "fig_7_13_header_audio_player.png"),
    }
    return images

print("build_report_data loaded successfully.")
