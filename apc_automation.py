#!/usr/bin/env python3
"""
APC Registration Automation Script
Automates the filling of APC member registration forms after NIN validation.
"""

import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class APCRegistrationBot:
    def __init__(self):
        self.driver = None
        self.nigerian_addresses = [
            "No. 45 Ahmadu Bello Way, Wuse II, Abuja FCT",
            "Plot 1234 Independence Avenue, Central Business District, Abuja",
            "Block 7, Flat 3, Garki Estate, Abuja FCT",
            "Suite A5, Wuse Plaza, Wuse II, Abuja",
            "House 12, Area 11, Garki, Abuja FCT",
            "Plot 456, Asokoro District, Abuja FCT",
            "No. 78 Aminu Kano Crescent, Wuse II, Abuja",
            "Flat 2B, Maitama Extension, Abuja FCT",
            "Plot 789, Utako District, Abuja FCT",
            "No. 23, Herbert Macaulay Way, Central Area, Abuja"
        ]

        self.nigerian_occupations = [
            "Accountant", "Teacher", "Engineer", "Doctor", "Lawyer",
            "Businessman", "Farmer", "Trader", "Driver", "Mechanic",
            "Carpenter", "Electrician", "Plumber", "Tailor", "Chef",
            "Nurse", "Pharmacist", "Journalist", "Banker", "Civil Servant"
        ]

    def setup_driver(self):
        """Initialize Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be present and return it"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click_element(self, locator, timeout=10):
        """Click an element with proper waiting"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        time.sleep(0.5)  # Brief pause after clicks

    def select_dropdown_option(self, dropdown_selector, option_text):
        """Select an option from a dropdown by text"""
        try:
            # Click the dropdown to open it
            dropdown = self.wait_for_element(dropdown_selector)
            dropdown.click()
            time.sleep(0.5)

            # Find and click the option
            option_xpath = f"//option[contains(text(), '{option_text}')]"
            option = self.wait_for_element((By.XPATH, option_xpath))
            option.click()
            time.sleep(0.5)
        except Exception as e:
            print(f"Error selecting {option_text}: {e}")

    def fill_nin_form(self, nin_number):
        """Fill out the NIN validation form"""
        try:
            print(f"Entering NIN: {nin_number}")

            # Find and fill NIN field
            nin_field = self.wait_for_element((By.ID, "nin"))
            nin_field.clear()
            nin_field.send_keys(nin_number)

            # Click validate button
            validate_btn = self.wait_for_element((By.ID, "validateNin"))
            validate_btn.click()

            print("NIN validation submitted, waiting for form expansion...")

            # Wait for form to expand (new fields to appear)
            WebDriverWait(self.driver, 15).until(
                lambda driver: len(driver.find_elements(By.ID, "title_id")) > 0
            )

            print("Form expanded successfully!")
            return True

        except Exception as e:
            print(f"Error in NIN validation: {e}")
            return False

    def fill_registration_form(self):
        """Fill out the complete registration form"""
        try:
            print("Starting form filling process...")

            # 1. Select Title: Hon.
            print("Selecting title: Hon.")
            self.select_dropdown_option((By.ID, "title_id"), "Hon.")

            # 2. Gender: Random (Male/Female)
            gender = random.choice(["Male", "Female"])
            print(f"Selecting gender: {gender}")
            self.select_dropdown_option((By.ID, "gender"), gender)

            # 3. Marital Status: Single
            print("Selecting marital status: Single")
            self.select_dropdown_option((By.ID, "marital_status"), "Single")

            # 4. Address: Random Nigerian address
            address = random.choice(self.nigerian_addresses)
            print(f"Entering address: {address}")
            address_field = self.wait_for_element((By.ID, "address"))
            address_field.clear()
            address_field.send_keys(address)

            # 5. Occupation: Random
            occupation = random.choice(self.nigerian_occupations)
            print(f"Selecting occupation: {occupation}")
            self.select_dropdown_option((By.ID, "occupation_id"), occupation)

            # 6. Religion: Random (Islam/Christianity/Other)
            religion = random.choice(["Islam", "Christianity", "Other"])
            print(f"Selecting religion: {religion}")
            self.select_dropdown_option((By.ID, "religion"), religion)

            # 7. Ward: KACHALLA SEMBE
            print("Selecting ward: KACHALLA SEMBE")
            self.select_dropdown_option((By.ID, "ward_id"), "KACHALLA SEMBE")

            # 8. Polling Unit: Wait for options to load, then select first one
            print("Waiting for polling units to load...")
            time.sleep(2)  # Give time for AJAX to load polling units

            # Try to select first available polling unit
            try:
                polling_select = self.wait_for_element((By.ID, "polling_unit_id"))
                options = polling_select.find_elements(By.TAG_NAME, "option")

                # Skip the first "Select a Ward first" option
                if len(options) > 1:
                    polling_unit = options[1].text  # Select second option (first real polling unit)
                    print(f"Selecting polling unit: {polling_unit}")
                    self.select_dropdown_option((By.ID, "polling_unit_id"), polling_unit)
                else:
                    print("No polling units available yet")
            except Exception as e:
                print(f"Error selecting polling unit: {e}")

            # 9. VIN: Random 11-digit number
            vin = ''.join(random.choices('0123456789', k=11))
            print(f"Entering VIN: {vin}")
            vin_field = self.wait_for_element((By.ID, "inec_id"))
            vin_field.clear()
            vin_field.send_keys(vin)

            # 10. Check consent checkbox
            print("Checking consent checkbox")
            consent_checkbox = self.wait_for_element((By.ID, "consent"))
            if not consent_checkbox.is_selected():
                consent_checkbox.click()

            print("Form filling completed successfully!")
            return True

        except Exception as e:
            print(f"Error filling registration form: {e}")
            return False

    def submit_form(self):
        """Submit the completed form"""
        try:
            print("Submitting form...")

            # Find and click submit button
            submit_btn = self.wait_for_element((By.CSS_SELECTOR, ".btnSubmit"))
            submit_btn.click()

            print("Form submitted! Waiting for response...")

            # Wait for either success message or error
            time.sleep(3)

            # Check for success indicators
            try:
                # Look for success message or redirect
                success_indicators = [
                    "success", "successful", "created", "registered",
                    "member created", "registration successful"
                ]

                page_text = self.driver.page_source.lower()
                if any(indicator in page_text for indicator in success_indicators):
                    print("✅ Registration appears successful!")
                    return True
                else:
                    print("⚠️ Registration status unclear - check page manually")
                    return False

            except Exception as e:
                print(f"Error checking submission result: {e}")
                return False

        except Exception as e:
            print(f"Error submitting form: {e}")
            return False

    def run_automation(self, nin_number, url="https://apcregistration.com/admin/members/create"):
        """Run the complete automation process"""
        try:
            print("🚀 Starting APC Registration Automation")
            print("=" * 50)

            # Setup driver
            self.setup_driver()

            # Navigate to the page
            print(f"Navigating to: {url}")
            self.driver.get(url)

            # Step 1: Fill NIN and validate
            if not self.fill_nin_form(nin_number):
                print("❌ NIN validation failed")
                return False

            # Step 2: Fill registration form
            if not self.fill_registration_form():
                print("❌ Form filling failed")
                return False

            # Step 3: Submit form
            if not self.submit_form():
                print("❌ Form submission failed")
                return False

            print("✅ Automation completed successfully!")
            return True

        except Exception as e:
            print(f"❌ Automation failed with error: {e}")
            return False

        finally:
            if self.driver:
                print("Closing browser...")
                time.sleep(2)  # Give time to see results
                self.driver.quit()

def main():
    """Main function to run the automation"""
    # Configuration
    NIN_NUMBER = "90807468604"  # Update this with the NIN you want to use

    # Create and run bot
    bot = APCRegistrationBot()
    success = bot.run_automation(NIN_NUMBER)

    if success:
        print("\n🎉 APC Registration Automation completed successfully!")
    else:
        print("\n❌ APC Registration Automation failed. Check logs above.")

if __name__ == "__main__":
    main()