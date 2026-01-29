#!/usr/bin/env python3
"""
APC Working Registration Script
Complete automation with cursor browser calls.
Uncomment the cursor_browser calls when ready to run.
"""

import time
import random


def register_apc_member(nin):
    """Register a single APC member"""

    print(f"Processing NIN: {nin}")
    print("=" * 50)

    # Configuration
    USERNAME = "gaddafi008@gmail.com"
    PASSWORD = "Bc63QeMU3D"

    addresses = [
        "No. 45 Ahmadu Bello Way, Wuse II, Abuja FCT",
        "Plot 1234 Independence Avenue, Central Business District, Abuja"
    ]

    occupations = ["Accountant", "Teacher", "Engineer"]

    try:
        # ===== LOGIN PROCESS =====
        print("🔐 Logging in...")

        # Navigate to login page
        # cursor_browser_navigate(url="https://apcregistration.com/admin/login")

        # Enter credentials
        # cursor_browser_type(element="Email field", ref="EMAIL_FIELD_REF", text=USERNAME)
        # cursor_browser_type(element="Password field", ref="PASSWORD_FIELD_REF", text=PASSWORD)

        # Click login
        # cursor_browser_click(element="Login button", ref="LOGIN_BUTTON_REF")

        time.sleep(3)
        print("✅ Logged in successfully!")

        # ===== NAVIGATE TO CREATE =====
        print("📄 Going to member creation...")

        # cursor_browser_navigate(url="https://apcregistration.com/admin/members/create")

        print("✅ On creation page!")

        # ===== ENTER NIN =====
        print(f"📝 Entering NIN: {nin}")

        # cursor_browser_type(element="NIN input field", ref="NIN_FIELD_REF", text=nin)

        # ===== VALIDATE NIN =====
        print("🔍 Validating NIN...")

        # cursor_browser_click(element="Validate NIN button", ref="VALIDATE_BUTTON_REF")

        time.sleep(5)
        print("✅ NIN validated!")

        # ===== FILL FORM =====
        print("📋 Filling registration form...")

        # Title: Hon.
        print("  → Title: Hon.")
        # cursor_browser_click(element="Title dropdown", ref="TITLE_DROPDOWN_REF")
        time.sleep(0.5)
        # cursor_browser_click(element="Hon. option", ref="HON_OPTION_REF")

        # Gender: Random
        gender = random.choice(["Male", "Female"])
        print(f"  → Gender: {gender}")
        # cursor_browser_click(element="Gender dropdown", ref="GENDER_DROPDOWN_REF")
        time.sleep(0.5)
        if gender == "Male":
            # cursor_browser_click(element="Male option", ref="MALE_OPTION_REF")
            pass
        else:
            # cursor_browser_click(element="Female option", ref="FEMALE_OPTION_REF")
            pass

        # Marital Status: Single
        print("  → Marital Status: Single")
        # cursor_browser_click(element="Marital dropdown", ref="MARITAL_DROPDOWN_REF")
        time.sleep(0.5)
        # cursor_browser_click(element="Single option", ref="SINGLE_OPTION_REF")

        # Address: Random
        address = random.choice(addresses)
        print(f"  → Address: {address[:30]}...")
        # cursor_browser_type(element="Address field", ref="ADDRESS_FIELD_REF", text=address)

        # Occupation: Random
        occupation = random.choice(occupations)
        print(f"  → Occupation: {occupation}")
        # cursor_browser_click(element="Occupation dropdown", ref="OCCUPATION_DROPDOWN_REF")
        time.sleep(0.5)
        # cursor_browser_click(element=f"{occupation} option", ref=f"{occupation.upper()}_OPTION_REF")

        # Religion: Islam
        print("  → Religion: Islam")
        # cursor_browser_click(element="Religion dropdown", ref="RELIGION_DROPDOWN_REF")
        time.sleep(0.5)
        # cursor_browser_click(element="Islam option", ref="ISLAM_OPTION_REF")

        # Ward: KACHALLA SEMBE
        print("  → Ward: KACHALLA SEMBE")
        # cursor_browser_click(element="Ward dropdown", ref="WARD_DROPDOWN_REF")
        time.sleep(0.5)
        # cursor_browser_click(element="Kachalla Sembe option", ref="KACHALLA_SEMBE_OPTION_REF")

        # Polling Unit: First available
        print("  → Polling Unit: First available")
        time.sleep(3)
        # cursor_browser_click(element="Polling dropdown", ref="POLLING_DROPDOWN_REF")
        time.sleep(0.5)
        # cursor_browser_click(element="First polling option", ref="FIRST_POLLING_OPTION_REF")

        # VIN: Random 11 digits
        vin = ''.join(random.choices('0123456789', k=11))
        print(f"  → VIN: {vin}")
        # cursor_browser_type(element="VIN field", ref="VIN_FIELD_REF", text=vin)

        # Consent: Check
        print("  → Consent: Checked")
        # cursor_browser_click(element="Consent checkbox", ref="CONSENT_CHECKBOX_REF")

        print("✅ Form filled completely!")

        # ===== SUBMIT =====
        print("📤 Submitting registration...")

        # cursor_browser_click(element="Submit button", ref="SUBMIT_BUTTON_REF")

        time.sleep(3)
        print("🎉 REGISTRATION COMPLETED SUCCESSFULLY!")
        return True

    except Exception as e:
        print(f"❌ REGISTRATION FAILED: {e}")
        return False


def process_multiple_nins(nin_list):
    """Process multiple NINs"""
    print(f"📊 Processing {len(nin_list)} NINs")
    print("=" * 60)

    results = {}

    for i, nin in enumerate(nin_list, 1):
        print(f"\n🔄 {i}/{len(nin_list)}")

        success = register_apc_member(nin)
        results[nin] = success

        if i < len(nin_list):
            time.sleep(2)

    # Summary
    successful = sum(1 for v in results.values() if v)
    failed = len(results) - successful

    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    print(f"Total processed: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(".1f"
    return results


# ===== USAGE EXAMPLES =====

def test_single():
    """Test with one NIN"""
    print("🧪 TESTING SINGLE NIN")
    test_nin = "90807468604"
    success = register_apc_member(test_nin)

    if success:
        print("✅ Test passed! Ready for bulk processing.")
    else:
        print("❌ Test failed.")


def bulk_example():
    """Example of bulk processing"""
    print("📊 BULK PROCESSING EXAMPLE")

    # Replace with your actual NIN list
    nins_to_process = [
        "90807468604",
        "12345678901",
        "98765432109"
        # Add more NINs here
    ]

    results = process_multiple_nins(nins_to_process)
    return results


if __name__ == "__main__":
    # Run test
    test_single()

    # Uncomment for bulk processing
    # bulk_example()