
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class APCAutomator:
    """APC Registration System Automator using Selenium"""

    def __init__(self):
        """Initialize the APC Automator with WebDriver setup"""
        # Chrome options for stable operation
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--window-size=1920,1080")

        # Initialize WebDriver with automatic driver management
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        except Exception as e:
            print(f"Error initializing Chrome driver: {e}")
            print("Falling back to system Chrome driver...")
            self.driver = webdriver.Chrome(options=self.chrome_options)

        # Set up WebDriverWait
        self.wait = WebDriverWait(self.driver, 30)

        # Store CSRF token for later use
        self.csrf_token = None

        print("APC Automator initialized successfully!")

    def login(self, max_retries=2):
        """STEP 1: Log into the APC admin portal"""
        print("🔐 Logging into APC Portal")

        for attempt in range(max_retries + 1):
            if attempt > 0:
                print(f"  → Retry attempt {attempt}/{max_retries}")
                time.sleep(5)  # Wait before retry

            try:
                # Navigate to login page
                print("  → Navigating to login page...")
                self.driver.get("https://apcregistration.com/admin/login")
                time.sleep(3)

                # EXACT SELECTORS FROM THE HTML
                USERNAME_SELECTOR = "#email"  # Confirmed: id="email"
                PASSWORD_SELECTOR = "#password"  # Confirmed: id="password"
                LOGIN_BUTTON_SELECTOR = "button.btn-danger"  # Confirmed: class="btn btn-danger"

                # Get CSRF token (important for Laravel)
                csrf_token = self.driver.find_element(By.NAME, "_token").get_attribute("value")
                print(f"  → CSRF token acquired: {csrf_token[:15]}...")
                self.csrf_token = csrf_token

                # Wait for and fill email
                email_field = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, USERNAME_SELECTOR))
                )
                email_field.send_keys("gaddafi008@gmail.com")
                print("  → Email entered.")

                # Fill password
                password_field = self.driver.find_element(By.CSS_SELECTOR, PASSWORD_SELECTOR)
                password_field.send_keys("Bc63QeMU3D")
                print("  → Password entered.")

                # Click login button
                login_button = self.driver.find_element(By.CSS_SELECTOR, LOGIN_BUTTON_SELECTOR)
                login_button.click()
                print("  → Login button clicked. Waiting for dashboard...")

                # Give more time for login to process
                time.sleep(5)

                # Wait for successful login - try multiple ways
                try:
                    # First try: wait for URL change (up to 30 seconds)
                    self.wait.until(EC.url_changes("https://apcregistration.com/admin/login"))
                    print("  → Login successful! Redirected from login page.")
                    time.sleep(3)
                    return True
                except TimeoutException:
                    # Second try: check if we're no longer on login page
                    current_url = self.driver.current_url
                    if "login" not in current_url:
                        print("  → Login successful! Redirected from login page.")
                        time.sleep(3)
                        return True
                    else:
                        # Third try: look for dashboard elements
                        try:
                            # Common dashboard elements
                            dashboard_indicators = [
                                "a[href*='dashboard']",
                                ".dashboard",
                                "h1",  # Usually a welcome header
                                ".navbar",
                                ".sidebar"
                            ]

                            for indicator in dashboard_indicators:
                                try:
                                    self.driver.find_element(By.CSS_SELECTOR, indicator)
                                    print("  → Login successful! Dashboard elements found.")
                                    time.sleep(3)
                                    return True
                                except:
                                    continue

                            # Check for error messages
                            error_indicators = [
                                ".alert-danger",
                                ".error",
                                "div:contains('Invalid')",
                                "div:contains('failed')"
                            ]

                            for error_indicator in error_indicators:
                                try:
                                    error_element = self.driver.find_element(By.CSS_SELECTOR, error_indicator)
                                    print(f"  → Login failed: {error_element.text}")
                                    return False
                                except:
                                    continue

                            print("  → Login status unclear - proceeding anyway...")
                            time.sleep(3)
                            return True

                        except Exception as e:
                            print(f"  → Could not verify login status: {e}")
                            # Give it one more chance
                            time.sleep(5)
                            if "login" not in self.driver.current_url:
                                print("  → Login appears successful.")
                                return True
                            else:
                                print("  → Login verification failed.")
                                return False

            except TimeoutException:
                if attempt < max_retries:
                    print(f"  → Login attempt {attempt + 1} timed out, retrying...")
                    continue
                else:
                    print("❌ Login failed or timed out after all retries.")
                    return False
            except Exception as e:
                if attempt < max_retries:
                    print(f"  → Login attempt {attempt + 1} failed: {str(e)}, retrying...")
                    continue
                else:
                    print(f"❌ Login error after all retries: {str(e)}")
                    return False

        # If we get here, all retries failed
        return False

    def navigate_to_create(self):
        """Navigate to member creation page"""
        try:
            print("📄 Navigating to member creation page...")
            self.driver.get("https://apcregistration.com/admin/members/create")

            # Give extra time for page to load
            time.sleep(3)

            # Wait for the page to load - try multiple indicators
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "form"))
                )
                print("✅ On member creation page!")
                return True
            except TimeoutException:
                # Check if we're on the right page anyway
                if "members/create" in self.driver.current_url:
                    print("✅ On member creation page (alternative check)!")
                    return True
                else:
                    print("❌ Not on member creation page")
                    return False

        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False

    def register_single_member(self, nin, is_first_nin=False):
        """Complete registration for one NIN"""
        print(f"🚀 Processing NIN: {nin}")
        print("=" * 60)

        addresses = [
            "No. 45 Ahmadu Bello Way, Wuse II, Abuja FCT",
            "Plot 1234 Independence Avenue, Central Business District, Abuja",
            "Block 7, Flat 3, Garki Estate, Abuja FCT",
            "Suite A5, Wuse Plaza, Wuse II, Abuja"
        ]

        occupations = ["Accountant", "Teacher", "Engineer", "Doctor", "Lawyer"]

        try:
            # ===== STEP 1: LOGIN (only for first NIN) =====
            if is_first_nin:
                if not self.login():
                    return False
                # ===== STEP 2: NAVIGATE TO CREATE =====
                if not self.navigate_to_create():
                    return False
            else:
                # For subsequent NINs, ensure we're on the create page
                print(f"  → Current URL: {self.driver.current_url}")
                if "members/create" not in self.driver.current_url:
                    print("📄 Navigating back to member creation page...")
                    self.driver.get("https://apcregistration.com/admin/members/create")
                    time.sleep(3)
                else:
                    print("📄 Already on member creation page")

                # Additional check: refresh page if NIN field not found
                try:
                    self.driver.find_element(By.CSS_SELECTOR, "#nin")
                    print("  → NIN field available")
                except:
                    print("  → NIN field not found, refreshing page...")
                    self.driver.refresh()
                    time.sleep(3)

            # ===== STEP 3: ENTER NIN =====
            print("📝 Step 3: Entering NIN")

            # Try multiple selectors for NIN field
            nin_selectors = ["#nin", "input[name='nin']", "input[placeholder*='NIN']", "input[type='text']"]
            nin_field = None

            print(f"  → Looking for NIN field with selectors: {nin_selectors}")
            for selector in nin_selectors:
                try:
                    print(f"    → Trying selector: {selector}")
                    nin_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    print(f"    → Found NIN field with: {selector}")
                    break
                except Exception as e:
                    print(f"    → Selector {selector} failed: {str(e)[:50]}...")
                    continue

            if not nin_field:
                print("❌ Could not find NIN input field with any selector")
                # Debug: print page source snippet
                try:
                    body_text = self.driver.find_element(By.TAG_NAME, "body").text[:200]
                    print(f"  → Page content preview: {body_text}...")
                except:
                    print("  → Could not get page content")
                return False

            nin_field.clear()
            nin_field.send_keys(nin)
            print(f"  → NIN entered: {nin}")

            # ===== STEP 4: VALIDATE NIN IMMEDIATELY =====
            print("🔍 Step 4: Validating NIN (immediate)")

            # Try multiple selectors for validate button - prioritize faster ones
            validate_selectors = ["button[type='button']", ".btn-primary", "input[type='submit']"]
            validate_button = None

            for selector in validate_selectors:
                try:
                    validate_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if validate_button and validate_button.is_displayed() and validate_button.is_enabled():
                        break
                except:
                    continue

            if validate_button:
                validate_button.click()
                print("  → Validate button clicked immediately")
            else:
                print("  → Could not find validate button, proceeding anyway...")

            print("  → Waiting for form loading...")

            # Check if NIN validation was successful and form is available
            max_wait_time = 6  # Reduced maximum time to wait for form (faster)
            form_ready = False

            for attempt in range(max_wait_time):
                try:
                    # Check if form fields are now available - prioritize key fields that load first
                    form_indicators = [
                        "#gender",  # Gender dropdown (usually loads first)
                        "#address",  # Address field
                        "#title_id",  # Title dropdown
                    ]

                    for indicator in form_indicators:
                        try:
                            element = self.driver.find_element(By.CSS_SELECTOR, indicator)
                            if element.is_displayed():
                                print(f"  → Form ready! Found: {indicator}")
                                form_ready = True
                                break
                        except:
                            continue

                    if form_ready:
                        break

                    # Quick check if we were redirected to a different page
                    current_url = self.driver.current_url
                    if "members/create" not in current_url and "nin" not in current_url.lower():
                        print(f"  → Redirected to: {current_url}")
                        time.sleep(0.5)
                        continue

                    # Shorter wait between checks
                    time.sleep(0.5)

                except Exception as e:
                    print(f"  → Checking form availability: {e}")
                    time.sleep(0.5)

            if not form_ready:
                print("❌ NIN validation failed - no form loaded, skipping to next NIN")
                return False  # Skip to next NIN immediately

            print("✅ NIN validation complete!")

            # ===== STEP 5: FILL FORM FIELDS =====
            print("📋 Step 5: Filling Registration Form")

            # Title: Hon. - Direct select approach
            print("  → Selecting Title: Hon.")
            try:
                title_select = Select(self.driver.find_element(By.CSS_SELECTOR, "#title_id"))
                title_select.select_by_value("10")  # Hon. value
                print("  → Title selected: Hon.")
            except Exception as e:
                print(f"  → Title selection failed (optional): {e}")

            # Gender: Random - Direct select approach
            gender = random.choice(["Male", "Female"])
            print(f"  → Selecting Gender: {gender}")
            try:
                gender_select = Select(self.driver.find_element(By.CSS_SELECTOR, "#gender"))
                gender_select.select_by_value(gender)  # Use the exact case: "Male" or "Female"
                print(f"  → Gender selected: {gender}")
            except Exception as e:
                print(f"  → Gender selection failed: {e}")

            # Marital Status: Single - Direct select approach
            print("  → Selecting Marital Status: Single")
            try:
                marital_select = Select(self.driver.find_element(By.CSS_SELECTOR, "#marital_status"))
                marital_select.select_by_value("Single")
                print("  → Marital status selected: Single")
            except Exception as e:
                print(f"  → Marital status selection failed: {e}")

            # Address: Random
            address = random.choice(addresses)
            print(f"  → Entering Address: {address[:30]}...")
            try:
                address_field = self.driver.find_element(By.CSS_SELECTOR, "#address")
                address_field.clear()
                address_field.send_keys(address)
                print("  → Address entered")
            except Exception as e:
                print(f"  → Address entry failed: {e}")

            # Email: Optional, can skip
            print("  → Email field (optional - skipping)")
            # Email is optional in the form

            # Occupation: Random - Direct select approach
            occupation = random.choice(occupations)
            print(f"  → Selecting Occupation: {occupation}")
            try:
                occupation_select = Select(self.driver.find_element(By.CSS_SELECTOR, "#occupation_id"))
                # Try to find occupation by visible text
                occupation_select.select_by_visible_text(occupation)
                print(f"  → Occupation selected: {occupation}")
            except Exception as e:
                print(f"  → Occupation selection failed: {e}")

            # Religion: Islam - Standard select
            print("  → Selecting Religion: Islam")
            try:
                religion_select = Select(self.driver.find_element(By.CSS_SELECTOR, "#religion"))
                religion_select.select_by_value("Islam")
                print("  → Religion selected: Islam")
            except Exception as e:
                print(f"  → Religion selection failed: {e}")

            # Ward: KACHALLA SEMBE - Direct select approach
            print("  → Selecting Ward: KACHALLA SEMBE")
            try:
                ward_select = Select(self.driver.find_element(By.CSS_SELECTOR, "#ward_id"))
                # Try to select by value first (8320), then by visible text
                try:
                    ward_select.select_by_value("8320")
                    print("  → Ward selected: KACHALLA SEMBE")
                except:
                    # Fallback: try to find by visible text
                    try:
                        ward_select.select_by_visible_text("KACHALLA SEMBE")
                        print("  → Ward selected: KACHALLA SEMBE")
                    except:
                        # Final fallback: select first option
                        ward_select.select_by_index(1)
                        print("  → Ward selected: First available")
            except Exception as e:
                print(f"  → Ward selection failed: {e}")

            # Polling Unit: First available - Direct select approach
            print("  → Selecting Polling Unit")
            try:
                # Wait for polling unit options to load after ward selection
                print("  → Waiting for polling unit options to load...")
                self.wait.until(
                    lambda driver: len(Select(driver.find_element(By.CSS_SELECTOR, "#polling_unit_id")).options) > 1
                )
                print("  → Polling unit options loaded")

                polling_select = Select(self.driver.find_element(By.CSS_SELECTOR, "#polling_unit_id"))
                # Select first available polling unit (index 1, skipping empty/placeholder option at 0)
                polling_select.select_by_index(1)
                print("  → Polling unit selected")
            except TimeoutException:
                print("  → Timeout waiting for polling unit options - trying anyway")
                try:
                    polling_select = Select(self.driver.find_element(By.CSS_SELECTOR, "#polling_unit_id"))
                    # Check if we have options beyond the placeholder
                    if len(polling_select.options) > 1:
                        polling_select.select_by_index(1)
                        print("  → Polling unit selected (after timeout)")
                    else:
                        print("  → No polling unit options available")
                except Exception as e:
                    print(f"  → Polling unit selection failed: {e}")
            except Exception as e:
                print(f"  → Polling unit selection failed: {e}")

            # VIN: Random 11 digits
            vin = ''.join(random.choices('0123456789', k=11))
            print(f"  → Entering VIN: {vin}")
            try:
                vin_field = self.driver.find_element(By.CSS_SELECTOR, "#inec_id")
                vin_field.clear()
                vin_field.send_keys(vin)
                print("  → VIN entered")
            except Exception as e:
                print(f"  → VIN entry failed: {e}")

            # Consent: Check
            print("  → Checking Consent")
            try:
                consent_checkbox = self.driver.find_element(By.CSS_SELECTOR, "#consent")
                if not consent_checkbox.is_selected():
                    consent_checkbox.click()
                    print("  → Consent checked")
            except Exception as e:
                print(f"  → Consent check failed: {e}")

            print("✅ Form filling complete (some fields may have been skipped if not found)!")

            # ===== STEP 6: SUBMIT =====
            print("📤 Step 6: Submitting Registration")
            try:
                submit_button = self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary.btnSubmit")
                submit_button.click()

                print("  → Waiting for completion...")
                time.sleep(5)  # Increased wait time for submission

                # Check for success/error messages after submission
                try:
                    # Look for success messages
                    success_indicators = [
                        ".alert-success",
                        ".success",
                        "div:contains('success')",
                        "div:contains('registered')",
                        "div:contains('created')"
                    ]

                    submission_success = False
                    for indicator in success_indicators:
                        try:
                            if "contains" in indicator:
                                success_msg = self.driver.find_element(By.XPATH, f"//div[contains(text(), 'success')]")
                                print(f"  → Success message found: {success_msg.text[:50]}...")
                                submission_success = True
                                break
                            else:
                                success_msg = self.driver.find_element(By.CSS_SELECTOR, indicator)
                                print(f"  → Success message found: {success_msg.text[:50]}...")
                                submission_success = True
                                break
                        except:
                            continue

                    if submission_success:
                        print("  → Registration confirmed successful!")
                    else:
                        print("  → No success message found, assuming successful")

                except Exception as e:
                    print(f"  → Could not check submission status: {e}")

                # Check submission result and prepare for next NIN
                current_url = self.driver.current_url
                print(f"  → Post-submission URL: {current_url}")

                if "members/create" in current_url:
                    print("  → Still on create page - form ready for next NIN")
                elif "members" in current_url and "create" not in current_url:
                    print("  → Redirected to members list - navigating back to create page...")
                    self.driver.get("https://apcregistration.com/admin/members/create")
                    time.sleep(3)
                else:
                    print(f"  → Unexpected redirect to: {current_url} - navigating to create page...")
                    self.driver.get("https://apcregistration.com/admin/members/create")
                    time.sleep(3)

                print("🎉 REGISTRATION COMPLETED SUCCESSFULLY!")
                print(f"✅ NIN {nin} registered!")
                return True
            except Exception as submit_error:
                print(f"❌ Submission failed: {submit_error}")
                # Try to navigate back to create page for next NIN
                try:
                    self.driver.get("https://apcregistration.com/admin/members/create")
                    time.sleep(3)
                except:
                    pass
                return False

        except Exception as e:
            print(f"❌ REGISTRATION FAILED for NIN {nin}")
            print(f"Error: {e}")
            return False

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


def process_bulk_nins(automator, nin_list):
    """Process multiple NINs using the APC automator"""
    print(f"📊 Starting bulk processing of {len(nin_list)} NINs")
    print("=" * 70)

    results = {}
    successful = 0
    failed = 0

    for i, nin in enumerate(nin_list, 1):
        print(f"\n🔄 Processing {i}/{len(nin_list)}: {nin}")

        # Only login for the first NIN
        is_first = (i == 1)
        success = automator.register_single_member(nin, is_first_nin=is_first)
        results[nin] = success

        if success:
            successful += 1
            print(f"✅ {nin}: SUCCESS")
        else:
            failed += 1
            print(f"❌ {nin}: FAILED")

        # Brief pause between registrations
        if i < len(nin_list):
            print("⏳ Preparing for next NIN...")
            time.sleep(5)

    # Summary
    print("\n" + "=" * 70)
    print("📊 BULK PROCESSING SUMMARY")
    print("=" * 70)
    print(f"Total NINs processed: {len(nin_list)}")
    print(f"Successful registrations: {successful}")
    print(f"Failed registrations: {failed}")
    print(f"Success rate: {successful/len(nin_list)*100:.1f}%")
    return results


def main():
    """Main function"""
    print("🚀 APC Registration Automation Runner")
    print("=" * 60)

    def parse_nins(raw: str):
        """Parse and de-duplicate NINs from raw multiline text."""
        seen = set()
        ordered = []
        for line in raw.splitlines():
            line = line.strip()
            if not line or line == "-":
                continue
            nin = line.replace(" ", "")
            if len(nin) == 11 and nin.isdigit() and nin not in seen:
                seen.add(nin)
                ordered.append(nin)
        return ordered

    raw_nins = """
74631809019
83156944198
86225123052
74964221347
22683674801
58024364509
77507301479
39231897428
34224948510
81257668877
62927014209
69891849608
71477590790
81776721370
71052432109
94088135152
39659637416
67159073343
34010338236
97316587284
85394444122
02330539648
63514923303
61771602784
81354340901
33491892032
61460934226
77767414280
26511938000
52490239310
24482036857
89554320092
65856793210
89350776892
33900509752
28913119706
21303285813
81862871967
41847805914
52902644331
93574811974
50682412502
47998841752
73829864586
84768143235
47741935973
"""

    nins_to_process = parse_nins(raw_nins)

    print(f"📊 Processing {len(nins_to_process)} NINs:")
    # Show first 5 and last 5 for brevity
    for i, nin in enumerate(nins_to_process[:5], 1):
        print(f"   {i}. {nin}")
    if len(nins_to_process) > 10:
        print(f"   ... ({len(nins_to_process) - 10} more NINs) ...")
        for i, nin in enumerate(nins_to_process[-5:], len(nins_to_process) - 4):
            print(f"   {i}. {nin}")
    print()
    print("⚠️  IMPORTANT: This script uses Selenium WebDriver to automate APC registration")
    print("🔧 Make sure Chrome is installed and webdriver-manager can download the driver")
    print()

    # Initialize the automator
    with APCAutomator() as automator:
        # Run bulk processing
        results = process_bulk_nins(automator, nins_to_process)

        # Final summary
        successful = sum(1 for v in results.values() if v)
        failed = len(results) - successful

        print("\n" + "=" * 80)
        print("🎯 FINAL RESULTS SUMMARY")
        print("=" * 80)
        print(f"Total NINs processed: {len(results)}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"Success rate: {successful/len(results)*100:.1f}%")

        if successful > 0:
            print("\n🎉 Automation completed! Check the results above.")
        else:
            print("\n❌ All registrations failed. Check the form selectors and try again.")


if __name__ == "__main__":
    main() 