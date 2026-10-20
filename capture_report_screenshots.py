import os
import time
from playwright.sync_api import sync_playwright

output_dir = os.path.join(os.path.dirname(__file__), "report_images")
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1.5)
    page = context.new_page()

    print("1. Capturing Login Monolith Screen...")
    page.goto("http://127.0.0.1:8000")
    page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(output_dir, "fig_7_1_login_monolith.png"))

    print("2. Logging in as Admin...")
    page.click('button[data-u="admin"]')
    page.click('#loginSubmit')
    page.wait_for_selector("#appShell.active", timeout=10000)
    page.wait_for_timeout(2500) # wait for chart animations and data fetch

    print("3. Capturing Cohort Overview Page...")
    page.screenshot(path=os.path.join(output_dir, "fig_7_2_cohort_overview.png"))

    print("4. Navigating to Student Twin (S1000)...")
    page.click('button[data-page="student"]')
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(output_dir, "fig_7_3_student_twin.png"))

    print("5. Interacting with What-If Simulator...")
    # Scroll down to what-if simulator
    page.evaluate("window.scrollTo(0, 1000)")
    page.wait_for_timeout(1000)
    # Adjust study hours slider
    study_slider = page.query_selector('#whatIfSliders input[type="range"]')
    if study_slider:
        page.evaluate('(el) => { el.value = 4.5; el.dispatchEvent(new Event("input")); }', study_slider)
        page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(output_dir, "fig_7_4_what_if_simulator.png"))

    print("6. Viewing At-Risk Student (S1093)...")
    page.select_option("#studentSelect", "S1093")
    page.wait_for_timeout(2500)
    page.evaluate("window.scrollTo(0, 0)")
    page.screenshot(path=os.path.join(output_dir, "fig_7_5_student_twin_at_risk.png"))

    print("7. Navigating to Cohort Analytics...")
    page.click('button[data-page="cohort"]')
    page.wait_for_timeout(2500)
    page.screenshot(path=os.path.join(output_dir, "fig_7_7_cohort_analytics_scatter.png"))

    # Scroll down to Feature Importance and Student Table
    page.evaluate("window.scrollTo(0, 450)")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(output_dir, "fig_7_8_feature_importance.png"))

    page.evaluate("window.scrollTo(0, 950)")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(output_dir, "fig_7_9_all_students_table.png"))

    print("8. Navigating to Assistant Chat...")
    page.click('button[data-page="assistant"]')
    page.wait_for_timeout(1500)
    page.evaluate("window.scrollTo(0, 0)")
    
    # Send a prompt to show the chat
    page.fill("#chatInputAssistant", "What is the single highest-impact change for this student?")
    page.click("#chatSendAssistant")
    page.wait_for_timeout(3000)
    page.screenshot(path=os.path.join(output_dir, "fig_7_10_assistant_chat.png"))

    # Send a what-if simulation prompt in chat
    page.fill("#chatInputAssistant", "what if they sleep 8 hours and study 3 hours?")
    page.click("#chatSendAssistant")
    page.wait_for_timeout(3500)
    page.screenshot(path=os.path.join(output_dir, "fig_7_11_chat_simulation_card.png"))

    print("9. Navigating to About & Model Page...")
    page.click('button[data-page="about"]')
    page.wait_for_timeout(2000)
    page.evaluate("window.scrollTo(0, 0)")
    page.screenshot(path=os.path.join(output_dir, "fig_7_12_about_and_model.png"))

    print("10. Testing Sound Engine...")
    page.click("#toggleSoundBtn")
    page.wait_for_timeout(1000)
    header_el = page.query_selector(".Header")
    if header_el:
        header_el.screenshot(path=os.path.join(output_dir, "fig_7_13_header_audio_player.png"))

    print("11. Logging in as Student (S1093) to capture Daily Check-in...")
    page.click("#logoutBtn")
    page.wait_for_selector("#loginScreen:not(.hidden)", timeout=5000)
    page.click('button[data-u="s1093"]')
    page.click("#loginSubmit")
    page.wait_for_selector("#appShell.active", timeout=10000)
    page.wait_for_timeout(2000)
    page.evaluate("window.scrollTo(0, 500)")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(output_dir, "fig_7_6_daily_checkin.png"))

    browser.close()
    print("All screenshots successfully captured!")
