from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load credentials from .env
load_dotenv()
USERNAME = os.getenv("SB_USERNAME")
PASSWORD = os.getenv("SB_PASSWORD")

# Set your fixed availability time
Y_TIME = "11:00 AM"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        page = context.new_page()

        print(" Logging in...")

        page.goto("https://portal.spacebasic.com/login")
        page.wait_for_load_state("networkidle")

        page.fill('#email', USERNAME)
        page.fill('#password', PASSWORD)

        page.wait_for_selector("button.login-btn:not([disabled])")
        page.click("button.login-btn")
        page.wait_for_load_state("networkidle")

        try:
            page.wait_for_selector('text="Complaints"', timeout=5000)
            print(" Logged in successfully.")
        except:
            print(" Login failed. Still on login page.")
           

        print(" Proceeding to submit new cleaning ticket...")

        # Go to complaints module
        page.goto("https://portal.spacebasic.com/module/complaints")
        page.wait_for_load_state("networkidle")

        # Open new ticket form
        page.click('button:has-text("Add Ticket")')
        #page.wait_for_selector('#category')
        #TO BE DELETED C

        tomorrow = datetime.now() + timedelta(days=1)
        date_string = tomorrow.strftime("%Y-%m-%d")
        page.fill('input[name="dateForTimeSlab"]', date_string)

        # Fill the form
           # Open the category dropdown
        page.click('ng-select[name="category"] .ng-arrow-wrapper')

        # Wait for options to appear
        page.wait_for_selector('.ng-dropdown-panel .ng-option')

        # Click on the Housekeeping option
        page.click('.ng-option:has-text("Housekeeping")')

        #Sub Category options
        page.click('ng-select[name="subCategory"] .ng-arrow-wrapper')

         
        page.wait_for_selector('.ng-dropdown-panel .ng-option')
        page.click('.ng-option:has-text("Room and Bathroom Cleaning")')

        #Priority Options

        page.click('ng-select[name="assign"] .ng-arrow-wrapper')

         
        page.wait_for_selector('.ng-dropdown-panel .ng-option')
        page.click('.ng-option:has-text("Critical")')
 
       
        #page.select_option("#priority", "Medium")
        page.fill('textarea[name="description"]', "Room cleaning requested")


        # Always select tomorrow
        # tomorrow = datetime.now() + timedelta(days=1)
        # date_string = tomorrow.strftime("%Y-%m-%d")
        # page.fill('input[name="dateForTimeSlab"]', date_string)

        #Selecting Time
        page.click('ng-select[name="timeslab"] .ng-arrow-wrapper')

         
        page.wait_for_selector('.ng-dropdown-panel .ng-option')
        page.click('.ng-option:has-text("03:01 PM - 04:00 PM")')

        print("Idhar tak toh chala hai")

        # Submit
        page.wait_for_selector('button:has-text("Submit"):not([disabled])')
        page.click('button:has-text("Submit")')
        print(" Cleaning ticket submitted successfully!")

        browser.close()

if __name__ == "__main__":
    main()