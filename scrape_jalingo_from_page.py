
import time
import csv
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

LOGIN_EMAIL = "ajjenventuresltd@gmail.com"
LOGIN_PASSWORD = "E7CE4VMGaF"
FIELDS = ["#", "Member ID", "First Name", "Middle Name", "Last Name", "Phone", "State", "LGA", "Ward"]


class JalingoPageScraper:

    def __init__(self, start_page, end_page=None):
        self.start_page = start_page
        self.end_page = end_page  # None means scrape until last page
        self.output_file = f"yorro_members_p{start_page}.csv"

        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception:
            self.driver = webdriver.Chrome(options=chrome_options)

        self.driver.set_page_load_timeout(60)
        self.wait = WebDriverWait(self.driver, 30)
        print(f"[p{start_page}] Browser initialized. Output: {self.output_file}")

    def login(self, retries=5):
        for attempt in range(1, retries + 1):
            try:
                print(f"[p{self.start_page}] Logging in (attempt {attempt})...")
                self.driver.get("https://apcregistration.com/admin/login")
                time.sleep(3)
                self.wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(LOGIN_EMAIL)
                self.driver.find_element(By.ID, "password").send_keys(LOGIN_PASSWORD)
                self.driver.find_element(By.CSS_SELECTOR, "button.btn-danger").click()
                try:
                    self.wait.until(EC.url_changes("https://apcregistration.com/admin/login"))
                except TimeoutException:
                    pass
                if "login" not in self.driver.current_url:
                    print(f"[p{self.start_page}] Login successful.")
                    time.sleep(2)
                    return True
                print(f"[p{self.start_page}] Login failed (wrong credentials or redirect).")
                return False
            except Exception as e:
                print(f"[p{self.start_page}] Login error: {e}")
                if attempt < retries:
                    wait = attempt * 15
                    print(f"[p{self.start_page}] Site slow, retrying in {wait}s...")
                    time.sleep(wait)
        print(f"[p{self.start_page}] Login failed after {retries} attempts.")
        return False

    def navigate_and_filter(self):
        print(f"[p{self.start_page}] Navigating to All Members...")
        self.driver.get("https://apcregistration.com/admin/members")
        time.sleep(3)

        # State filter
        try:
            state_select = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//select[contains(@name,'state') or @id='state']"))
            )
            Select(state_select).select_by_visible_text("TARABA")
            print(f"[p{self.start_page}]   State = TARABA")
            time.sleep(2)
        except Exception as e:
            print(f"[p{self.start_page}]   State filter failed: {e}")

        # LGA filter
        try:
            lga_select = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//select[contains(@name,'lga') or @id='lga']"))
            )
            Select(lga_select).select_by_visible_text("YORRO")
            print(f"[p{self.start_page}]   LGA = YORRO")
            time.sleep(2)
        except Exception as e:
            print(f"[p{self.start_page}]   LGA filter failed: {e}")

        # Set 100 entries per page
        try:
            entries_select = self.driver.find_element(By.CSS_SELECTOR, "select[name$='_length']")
            options = [o.get_attribute("value") for o in Select(entries_select).options]
            best = max((int(v) for v in options if v.isdigit()), default=25)
            Select(entries_select).select_by_value(str(best))
            print(f"[p{self.start_page}]   Entries per page = {best}")
            time.sleep(2)
        except Exception:
            print(f"[p{self.start_page}]   Could not set entries per page.")

    def jump_to_start_page(self):
        if self.start_page <= 1:
            return
        target = self.start_page - 1  # DataTables uses 0-based page index
        print(f"[p{self.start_page}] Jumping to page {self.start_page} via JavaScript...")
        try:
            # Try DataTables JS API first (works on all DataTables setups)
            self.driver.execute_script(
                "var t = $.fn.dataTable.tables({api:true}); t.page(arguments[0]).draw('page');",
                target
            )
            time.sleep(2)
            # Verify we landed on the right page
            actual = self._current_page_number()
            if actual and actual == self.start_page:
                print(f"[p{self.start_page}] JS jump successful, on page {actual}.")
                return
            else:
                print(f"[p{self.start_page}] JS jump landed on page {actual}, will try input method...")
        except Exception as e:
            print(f"[p{self.start_page}] JS jump failed: {e}")

        # Fallback: use the pagination input box if available
        try:
            page_input = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label*='page'], input.paginate_input")
            page_input.clear()
            page_input.send_keys(str(self.start_page))
            from selenium.webdriver.common.keys import Keys
            page_input.send_keys(Keys.RETURN)
            time.sleep(2)
            actual = self._current_page_number()
            print(f"[p{self.start_page}] Input jump landed on page {actual}.")
            return
        except Exception:
            pass

        # Last resort: click Next but verify page number each step
        print(f"[p{self.start_page}] Falling back to Next clicks with verification...")
        current = self._current_page_number() or 1
        while current < self.start_page:
            try:
                next_btn = self.driver.find_element(
                    By.CSS_SELECTOR, "a.paginate_button.next, li.next a, [id$='_next']"
                )
                next_btn.click()
                time.sleep(1)
                new_page = self._current_page_number()
                if new_page:
                    if new_page < current:  # reset detected during jump
                        print(f"[p{self.start_page}] Reset detected during jump at page {current}, retrying JS...")
                        self.driver.execute_script(
                            "var t = $.fn.dataTable.tables({api:true}); t.page(arguments[0]).draw('page');",
                            target
                        )
                        time.sleep(2)
                        break
                    current = new_page
                if current % 20 == 0:
                    print(f"[p{self.start_page}]   At page {current}...")
            except Exception as e:
                print(f"[p{self.start_page}]   Click failed: {e}")
                break
        print(f"[p{self.start_page}] Jump complete, on page {self._current_page_number()}.")

    def _current_page_number(self):
        """Read the current page number from DataTables info text."""
        try:
            info = self.driver.find_element(
                By.CSS_SELECTOR, "div[id$='_info'], .dataTables_info"
            ).text.replace(",", "")
            # "Showing 16001 to 16100 of 23495 entries" -> page = 16001 // 100 + 1
            parts = info.split()
            if "Showing" in parts:
                first_row = int(parts[1])
                # Get entries per page from length select
                try:
                    sel = self.driver.find_element(By.CSS_SELECTOR, "select[name$='_length']")
                    per_page = int(Select(sel).first_selected_option.get_attribute("value"))
                except Exception:
                    per_page = 100
                return (first_row - 1) // per_page + 1
        except Exception:
            pass
        return None

    def get_table_rows(self):
        rows = []
        try:
            tbody = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody")))
            for tr in tbody.find_elements(By.TAG_NAME, "tr"):
                cells = tr.find_elements(By.TAG_NAME, "td")
                if cells:
                    rows.append([c.text.strip() for c in cells[:9]])
        except Exception as e:
            print(f"[p{self.start_page}]   Row extraction error: {e}")
        return rows

    def has_next_page(self):
        try:
            next_btn = self.driver.find_element(
                By.CSS_SELECTOR, "a.paginate_button.next, li.next a, [id$='_next']"
            )
            classes = next_btn.find_element(By.XPATH, "./..").get_attribute("class") or ""
            return "disabled" not in classes
        except Exception:
            return False

    def click_next_page(self):
        try:
            self.driver.find_element(
                By.CSS_SELECTOR, "a.paginate_button.next, li.next a, [id$='_next']"
            ).click()
            time.sleep(2)
            return True
        except Exception:
            return False

    def scrape(self):
        # Write header
        with open(self.output_file, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDS)

        page = self.start_page
        buffer = []

        while True:
            if self.end_page and page > self.end_page:
                print(f"[p{self.start_page}] Reached end page {self.end_page}, stopping.")
                break

            # Verify we are on the expected page — detect resets
            actual = self._current_page_number()
            if actual and actual != page:
                print(f"[p{self.start_page}] Reset detected! Expected page {page}, on page {actual}. Re-jumping...")
                target = page - 1
                self.driver.execute_script(
                    "var t = $.fn.dataTable.tables({api:true}); t.page(arguments[0]).draw('page');",
                    target
                )
                time.sleep(2)
                actual = self._current_page_number()
                print(f"[p{self.start_page}] After re-jump: on page {actual}.")

            print(f"[p{self.start_page}] Scraping page {page}...", end=" ", flush=True)
            rows = self.get_table_rows()
            print(f"{len(rows)} rows")
            buffer.extend(rows)

            # Flush every 10 pages
            if (page - self.start_page + 1) % 10 == 0:
                with open(self.output_file, "a", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerows(buffer)
                buffer = []
                print(f"[p{self.start_page}] Checkpoint saved at page {page}.")

            if not self.has_next_page():
                print(f"[p{self.start_page}] Last page reached.")
                break

            if not self.click_next_page():
                break

            page += 1

        # Flush remainder
        if buffer:
            with open(self.output_file, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(buffer)

        with open(self.output_file, "r", encoding="utf-8") as f:
            total = sum(1 for _ in f) - 1
        print(f"[p{self.start_page}] Done! {total:,} records saved to {self.output_file}")
        return total

    def run(self):
        if not self.login():
            return
        self.navigate_and_filter()
        self.jump_to_start_page()
        self.scrape()

    def close(self):
        self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def main():
    # Usage: python scrape_jalingo_from_page.py <start_page> [end_page]
    # Examples:
    #   python scrape_jalingo_from_page.py 1 100     -> pages 1-100
    #   python scrape_jalingo_from_page.py 101 200   -> pages 101-200
    #   python scrape_jalingo_from_page.py 201        -> pages 201 to end

    args = sys.argv[1:]
    if not args:
        print("Usage: python scrape_jalingo_from_page.py <start_page> [end_page]")
        print("  Example (pages 1-100):   python scrape_jalingo_from_page.py 1 100")
        print("  Example (pages 101-200): python scrape_jalingo_from_page.py 101 200")
        print("  Example (page 201+):     python scrape_jalingo_from_page.py 201")
        sys.exit(1)

    start_page = int(args[0])
    end_page = int(args[1]) if len(args) > 1 else None

    print("=" * 60)
    print(f"Scraping pages {start_page} to {end_page or 'end'}")
    print("=" * 60)

    with JalingoPageScraper(start_page, end_page) as scraper:
        scraper.run()


if __name__ == "__main__":
    main()
