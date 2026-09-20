"""
Automated Screen Recording of EcoDispatch AI Web Dashboard using Playwright
Records live user interaction with the production dashboard on Vercel.
"""
import os
import time
from playwright.sync_api import sync_playwright

REC_DIR = os.path.abspath("demo/recordings")
os.makedirs(REC_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=REC_DIR,
        record_video_size={"width": 1920, "height": 1080}
    )
    page = context.new_page()

    print("Navigating to live production dashboard...")
    page.goto("https://ecodispatch-ai.vercel.app", wait_until="networkidle")
    time.sleep(3.0)

    # 1. Switch region to ERCOT (Texas)
    print("Switching grid region to Texas (ERCOT)...")
    page.click("button[data-region='ERCOT']")
    time.sleep(4.5)

    # 2. Switch region to Great Britain (UK)
    print("Switching grid region to UK...")
    page.click("button[data-region='UK']")
    time.sleep(4.0)

    # 3. Switch back to California (CAISO)
    print("Switching grid region back to California (CAISO)...")
    page.click("button[data-region='CAISO']")
    time.sleep(4.0)

    # 4. Trigger Autonomous Carbon Dispatch
    print("Running Autonomous Carbon Dispatch...")
    page.click("button:has-text('Run Autonomous Carbon Dispatch')")
    time.sleep(5.5)

    # 5. Hover and inspect the ESG Certificate Card
    print("Inspecting cryptographic ESG certificate...")
    page.hover("#certId")
    time.sleep(6.0)

    context.close()
    browser.close()
    print("Live screen recording complete.")
