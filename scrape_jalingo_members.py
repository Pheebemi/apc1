
import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import sys

LOGIN_EMAIL = "ajjenventuresltd@gmail.com"
LOGIN_PASSWORD = "E7CE4VMGaF"
FIELDS = ["#", "Member ID", "First Name", "Middle Name", "Last Name", "Phone", "State", "LGA", "Ward"]

# LGA passed as argument, default to JALINGO
TARGET_LGA = sys.argv[1].upper() if len(sys.argv) > 1 else "JALINGO"
OUTPUT_FILE = f"{TARGET_LGA.lower()}_members.csv"


class JalingoScraper:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception:
            self.driver = webdriver.Chrome(options=chrome_options)

        self.wait = WebDriverWait(self.driver, 30)
        print("Browser initialized.")

    def login(self):
        print("Logging in...")
        self.driver.get("https://apcregistration.com/admin/login")
        time.sleep(3)

        self.wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(LOGIN_EMAIL)
        self.driver.find_element(By.ID, "password").send_keys(LOGIN_PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, "button.btn-danger").click()

        try:
            self.wait.until(EC.url_changes("https://apcregistration.com/admin/login"))
            print("Login successful.")
            time.sleep(2)
            return True
        except TimeoutException:
            if "login" not in self.driver.current_url:
                print("Login successful (URL check).")
                time.sleep(2)
                return True
            print("Login failed.")
            return False

    def navigate_to_all_members(self):
        print("Navigating to All Members...")
        # Click the Members sidebar item to expand dropdown
        try:
            members_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'#') and contains(., 'Members')]"))
            )
            members_link.click()
            time.sleep(1)
        except Exception as e:
            print(f"  Could not click Members sidebar item: {e}")
            # Try alternative: look for nav item with Members text
            try:
                members_link = self.driver.find_element(
                    By.XPATH, "//li[contains(@class,'nav-item')]//a[contains(text(),'Members')]"
                )
                members_link.click()
                time.sleep(1)
            except Exception as e2:
                print(f"  Alternative selector also failed: {e2}")

        # Click "All Members" from the dropdown
        try:
            all_members = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@href,'members') and not(contains(@href,'create')) and contains(., 'All Members')]")
                )
            )
            all_members.click()
            time.sleep(3)
            print(f"  Navigated to: {self.driver.current_url}")
            return True
        except Exception as e:
            print(f"  Could not click All Members: {e}")
            # Fallback: navigate directly
            self.driver.get("https://apcregistration.com/admin/members")
            time.sleep(3)
            return True

    def apply_filters(self):
        print("Applying filters: State=TARABA, LGA=JALINGO...")
        try:
            # Select State: TARABA
            state_select = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//select[contains(@name,'state') or @id='state']"))
            )
            Select(state_select).select_by_visible_text("TARABA")
            print("  State set to TARABA.")
            time.sleep(2)  # Wait for LGA to load

            # Select LGA: JALINGO
            lga_select = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//select[contains(@name,'lga') or @id='lga']"))
            )
            Select(lga_select).select_by_visible_text(TARGET_LGA)
            print(f"  LGA set to {TARGET_LGA}.")
            time.sleep(1)

            # Click Search/Filter button if present
            try:
                search_btn = self.driver.find_element(
                    By.XPATH, "//button[@type='submit' or contains(@class,'btn-primary') or contains(text(),'Search') or contains(text(),'Filter')]"
                )
                search_btn.click()
                print("  Search button clicked.")
                time.sleep(3)
            except Exception:
                print("  No search button found, filter may auto-apply.")
                time.sleep(3)

            return True
        except Exception as e:
            print(f"  Filter error: {e}")
            return False

    def set_entries_per_page(self, count=100):
        """Try to show max entries per page to reduce pagination."""
        try:
            entries_select = self.driver.find_element(
                By.XPATH, "//select[@name='members_table_length' or contains(@name,'_length')]"
            )
            Select(entries_select).select_by_value(str(count))
            print(f"  Entries per page set to {count}.")
            time.sleep(2)
        except Exception:
            try:
                # DataTables length select
                entries_select = self.driver.find_element(By.CSS_SELECTOR, "select[name$='_length']")
                options = [o.get_attribute("value") for o in Select(entries_select).options]
                # Pick largest available option
                best = max((int(v) for v in options if v.isdigit()), default=25)
                Select(entries_select).select_by_value(str(best))
                print(f"  Entries per page set to {best}.")
                time.sleep(2)
            except Exception:
                print("  Could not change entries per page, using default.")

    def get_table_rows(self):
        """Extract all rows from the current table page."""
        rows = []
        try:
            tbody = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody"))
            )
            tr_elements = tbody.find_elements(By.TAG_NAME, "tr")
            for tr in tr_elements:
                cells = tr.find_elements(By.TAG_NAME, "td")
                if not cells:
                    continue
                row = [c.text.strip() for c in cells]
                # Keep only first 9 columns (matching FIELDS)
                rows.append(row[:9])
        except Exception as e:
            print(f"  Error extracting rows: {e}")
        return rows

    def get_total_records(self):
        """Try to read total record count from DataTables info text."""
        try:
            info = self.driver.find_element(
                By.CSS_SELECTOR, "div[id$='_info'], .dataTables_info"
            ).text
            # e.g. "Showing 1 to 100 of 20,453 entries"
            parts = info.replace(",", "").split()
            if "of" in parts:
                idx = parts.index("of")
                return int(parts[idx + 1])
        except Exception:
            pass
        return None

    def has_next_page(self):
        """Check if the Next pagination button is active."""
        try:
            next_btn = self.driver.find_element(
                By.CSS_SELECTOR, "a.paginate_button.next, li.next a, [id$='_next']"
            )
            parent = next_btn.find_element(By.XPATH, "./..")
            classes = parent.get_attribute("class") or ""
            if "disabled" in classes:
                return False
            return True
        except Exception:
            return False

    def click_next_page(self):
        try:
            next_btn = self.driver.find_element(
                By.CSS_SELECTOR, "a.paginate_button.next, li.next a, [id$='_next']"
            )
            next_btn.click()
            time.sleep(2)
            return True
        except Exception as e:
            print(f"  Could not click next: {e}")
            return False

    def scrape_all(self):
        all_rows = []
        page = 1

        # Write CSV header upfront so the file exists from the start
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDS)

        total = self.get_total_records()
        if total:
            print(f"Total records found: {total:,}")

        while True:
            print(f"  Scraping page {page}...", end=" ", flush=True)
            rows = self.get_table_rows()
            print(f"{len(rows)} rows")
            all_rows.extend(rows)

            # Flush to CSV every 10 pages so progress is never lost
            if page % 10 == 0:
                self._append_to_csv(all_rows)
                all_rows = []
                print(f"  Checkpoint saved. Total so far: {(page * 100):,} approx.")

            if not self.has_next_page():
                print("  Reached last page.")
                break

            if not self.click_next_page():
                break

            page += 1

        # Flush any remaining rows
        if all_rows:
            self._append_to_csv(all_rows)

        # Count total saved
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            total_saved = sum(1 for _ in f) - 1  # subtract header
        return total_saved

    def _append_to_csv(self, rows):
        with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(rows)

    def save_to_csv(self, rows):
        # Kept for compatibility but scrape_all now writes incrementally
        pass

    def close(self):
        self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def main():
    print("=" * 60)
    print("APC Members Scraper")
    print("=" * 60)

    with JalingoScraper() as scraper:
        if not scraper.login():
            print("Aborting: login failed.")
            return

        if not scraper.navigate_to_all_members():
            print("Aborting: navigation failed.")
            return

        if not scraper.apply_filters():
            print("Warning: filter may not have applied correctly, proceeding...")

        scraper.set_entries_per_page(100)

        print("\nStarting data extraction...")
        total_saved = scraper.scrape_all()
        if total_saved:
            print(f"\nDone! {total_saved:,} Jalingo/Taraba members saved to: {os.path.abspath(OUTPUT_FILE)}")
        else:
            print("No data collected. Check filters and table selectors.")


if __name__ == "__main__":
    main()
