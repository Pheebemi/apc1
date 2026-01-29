import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class APCAutomator:
    """APC Registration System Automator"""

    def __init__(self):
        """Initialize the APC Automator with WebDriver setup"""
        # Load environment variables from current directory
        load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
        print(f"Loading .env from: {os.path.join(os.getcwd(), '.env')}")

        # Chrome options for stable operation
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-plugins")
        self.chrome_options.add_argument("--disable-images")  # Speed up loading
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--disable-web-security")
        self.chrome_options.add_argument("--allow-running-insecure-content")
        # Disable headless mode to see the browser
        # self.chrome_options.add_argument("--headless")  # Enable headless mode

        # Initialize WebDriver with automatic driver management
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        except Exception as e:
            print(f"Error initializing Chrome driver: {e}")
            print("Falling back to system Chrome driver...")
            self.driver = webdriver.Chrome(options=self.chrome_options)

        # Set up WebDriverWait
        self.wait = WebDriverWait(self.driver, 10)

        # Store CSRF token for later use
        self.csrf_token = None

        print("APC Automator initialized successfully!")

    def login(self):
        """STEP 1: Log into the APC admin portal - WITH EXACT SELECTORS"""
        print("Navigating to login page...")
        try:
            self.driver.get("https://apcregistration.com/admin/login")
            # Wait for page to load
            time.sleep(3)
        except Exception as e:
            print(f"Error loading login page: {e}")
            return False

        # EXACT SELECTORS FROM THE HTML
        USERNAME_SELECTOR = "#email"  # Confirmed: id="email"
        PASSWORD_SELECTOR = "#password"  # Confirmed: id="password"
        LOGIN_BUTTON_SELECTOR = "button.btn-danger"  # Confirmed: class="btn btn-danger"

        try:
            # Get CSRF token (important for Laravel)
            csrf_token = self.driver.find_element(By.NAME, "_token").get_attribute("value")
            print(f"CSRF token acquired: {csrf_token[:15]}...")
            self.csrf_token = csrf_token

            # Wait for and fill email
            email_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, USERNAME_SELECTOR))
            )
            email_field.send_keys("gaddafi008@gmail.com")  # Hardcoded credentials
            print("Email entered.")

            # Fill password
            password_field = self.driver.find_element(By.CSS_SELECTOR, PASSWORD_SELECTOR)
            password_field.send_keys("Bc63QeMU3D")  # Hardcoded credentials
            print("Password entered.")

            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, LOGIN_BUTTON_SELECTOR)
            login_button.click()
            print("Login button clicked. Waiting for dashboard...")

            # Wait for successful login
            # After login, we should be redirected away from the login page
            self.wait.until(EC.url_changes("https://apcregistration.com/admin/login"))
            print("Login successful! Redirected from login page.")

            # Additional: Wait for dashboard elements
            time.sleep(3)  # Allow dashboard to load
            return True

        except TimeoutException:
            print("ERROR: Login failed or timed out.")
            # Check if we're still on login page
            if "login" in self.driver.current_url:
                print("Still on login page. Check credentials or website status.")
                self.driver.save_screenshot("login_failed.png")
            return False

        except Exception as e:
            print(f"ERROR during login: {str(e)}")
            self.driver.save_screenshot("login_error.png")
            return False

    def navigate_to_member_creation(self):
        """Navigate to the member creation page"""
        try:
            print("Navigating to member creation page...")
            self.driver.get("https://apcregistration.com/admin/members/create")

            # Wait for the page to load
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            print("Member creation page loaded successfully!")
            return True

        except Exception as e:
            print(f"ERROR navigating to member creation: {str(e)}")
            return False

    def create_member(self, member_data):
        """
        Create a new member with the provided data

        Args:
            member_data (dict): Dictionary containing member information
                Required keys: nin, first_name, last_name, phone, state_id, lga_id
        """
        print(f"Creating member: {member_data.get('first_name', 'Unknown')} {member_data.get('last_name', 'Unknown')}")

        # TODO: Implement member creation form filling
        # This will be completed once we get the HTML structure of the member creation form

        print("Member creation not yet implemented - need form selectors")
        return False

    def logout(self):
        """Log out from the admin panel"""
        try:
            print("Logging out...")
            # Look for logout link/button
            logout_selectors = [
                "a[href*='logout']",
                "button[type='submit'][value*='logout']",
                ".logout",
                "#logout"
            ]

            for selector in logout_selectors:
                try:
                    logout_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    logout_element.click()
                    print("Logout successful!")
                    return True
                except NoSuchElementException:
                    continue

            print("Logout element not found, closing browser...")
            return False

        except Exception as e:
            print(f"Error during logout: {str(e)}")
            return False

        finally:
            self.close()

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def main():
    """Main function to run the APC Automator"""
    print("Starting APC Registration Automator...")
    print("Using hardcoded credentials for testing...")

    with APCAutomator() as automator:
        # Login to the system
        if automator.login():
            print("✅ Login successful!")

            # Navigate to member creation (for future use)
            if automator.navigate_to_member_creation():
                print("✅ Ready for member creation")
                # TODO: Implement member creation loop here

            else:
                print("❌ Failed to navigate to member creation")
        else:
            print("❌ Login failed!")


if __name__ == "__main__":
    main()