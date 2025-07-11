from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

# Load credentials
load_dotenv()
USERNAME = os.getenv("SLCM_USERNAME")
PASSWORD = os.getenv("SLCM_PASSWORD")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # set False if you want to debug locally
        context = browser.new_context()
        page = context.new_page()

        print("🔐 Logging into SLCM...")

        # Step 1: Go to login page
        page.goto("https://mujslcm.jaipur.manipal.edu/")  # replace with exact URL if different
        page.wait_for_load_state("networkidle")

        # Step 2: Fill in login
        page.fill('input[name="UserName"]', USERNAME)
        page.fill('input[name="Password"]', PASSWORD)
        page.click('#login_submitStudent') # Adjust selector if different
        page.wait_for_load_state("networkidle")

        # Step 3: Click Reports menu
        print("📊 Navigating to attendance summary...")
        page.click('text="Reports"')  # Might need to adjust this
        page.wait_for_selector('text="Attendance Summary"')
        page.click('text="Attendance Summary"')
        page.wait_for_load_state("networkidle")

        # Step 4: Screenshot
        print("📸 Taking screenshot...")
        page.screenshot(path="attendance.png", full_page=True)
        print("✅ Screenshot saved as attendance.png")

        browser.close()

if __name__ == "__main__":
    main()
