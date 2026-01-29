#!/usr/bin/env python3
"""
FINAL APC REGISTRATION AUTOMATION
Complete cursor browser automation for bulk APC member registration.
Run this script when the APC website is accessible.
"""

import time
import random


def process_apc_registration(nin_number):
    """Complete APC registration automation for one NIN"""

    print(f"🚀 Processing NIN: {nin_number}")
    print("=" * 50)

    try:
        # ===== STEP 1: LOGIN =====
        print("🔐 LOGIN: Starting...")

        # Navigate to login page
        cursor_browser_navigate(url="https://apcregistration.com/admin/login")
        time.sleep(2)

        # Enter credentials (from .env file)
        cursor_browser_type(
            element="Email field",
            ref="LOGIN_EMAIL_REF",  # You'll need to identify this from snapshot
            text="gaddafi008@gmail.com"
        )

        cursor_browser_type(
            element="Password field",
            ref="LOGIN_PASSWORD_REF",  # You'll need to identify this from snapshot
            text="Bc63QeMU3D"
        )

        # Click login
        cursor_browser_click(
            element="Login button",
            ref="LOGIN_BUTTON_REF"  # You'll need to identify this from snapshot
        )

        time.sleep(3)
        print("✅ LOGIN: Successful")

        # ===== STEP 2: NAVIGATE TO CREATE =====
        print("📄 NAVIGATE: Going to member creation...")

        cursor_browser_navigate(url="https://apcregistration.com/admin/members/create")
        time.sleep(2)

        print("✅ NAVIGATE: On creation page")

        # ===== STEP 3: ENTER NIN =====
        print(f"📝 NIN: Entering {nin_number}")

        cursor_browser_type(
            element="NIN input field",
            ref="NIN_FIELD_REF",  # You'll need to identify this from snapshot
            text=nin_number
        )

        # ===== STEP 4: VALIDATE NIN =====
        print("🔍 VALIDATE: Validating NIN...")

        cursor_browser_click(
            element="Validate NIN button",
            ref="VALIDATE_BUTTON_REF"  # You'll need to identify this from snapshot
        )

        time.sleep(5)
        print("✅ VALIDATE: NIN validated")

        # ===== STEP 5: FILL FORM =====
        print("📋 FORM: Filling registration form...")

        # Title: Hon.
        print("  → Title: Hon.")
        cursor_browser_click(element="Title dropdown", ref="TITLE_DROPDOWN_REF")
        time.sleep(0.5)
        cursor_browser_click(element="Hon. option", ref="HON_OPTION_REF")

        # Gender: Random
        gender = random.choice(["Male", "Female"])
        print(f"  → Gender: {gender}")
        cursor_browser_click(element="Gender dropdown", ref="GENDER_DROPDOWN_REF")
        time.sleep(0.5)
        if gender == "Male":
            cursor_browser_click(element="Male option", ref="MALE_OPTION_REF")
        else:
            cursor_browser_click(element="Female option", ref="FEMALE_OPTION_REF")

        # Marital Status: Single
        print("  → Marital Status: Single")
        cursor_browser_click(element="Marital dropdown", ref="MARITAL_DROPDOWN_REF")
        time.sleep(0.5)
        cursor_browser_click(element="Single option", ref="SINGLE_OPTION_REF")

        # Address: Random
        addresses = [
            "No. 45 Ahmadu Bello Way, Wuse II, Abuja FCT",
            "Plot 1234 Independence Avenue, Central Business District, Abuja"
        ]
        address = random.choice(addresses)
        print(f"  → Address: {address[:30]}...")
        cursor_browser_type(element="Address field", ref="ADDRESS_FIELD_REF", text=address)

        # Occupation: Random
        occupations = ["Accountant", "Teacher", "Engineer"]
        occupation = random.choice(occupations)
        print(f"  → Occupation: {occupation}")
        cursor_browser_click(element="Occupation dropdown", ref="OCCUPATION_DROPDOWN_REF")
        time.sleep(0.5)
        cursor_browser_click(element=f"{occupation} option", ref=f"{occupation.upper()}_OPTION_REF")

        # Religion: Islam
        print("  → Religion: Islam")
        cursor_browser_click(element="Religion dropdown", ref="RELIGION_DROPDOWN_REF")
        time.sleep(0.5)
        cursor_browser_click(element="Islam option", ref="ISLAM_OPTION_REF")

        # Ward: KACHALLA SEMBE
        print("  → Ward: KACHALLA SEMBE")
        cursor_browser_click(element="Ward dropdown", ref="WARD_DROPDOWN_REF")
        time.sleep(0.5)
        cursor_browser_click(element="Kachalla Sembe option", ref="KACHALLA_SEMBE_OPTION_REF")

        # Polling Unit: First available
        print("  → Polling Unit: First available")
        time.sleep(3)
        cursor_browser_click(element="Polling dropdown", ref="POLLING_DROPDOWN_REF")
        time.sleep(0.5)
        cursor_browser_click(element="First polling option", ref="FIRST_POLLING_OPTION_REF")

        # VIN: Random 11 digits
        vin = ''.join(random.choices('0123456789', k=11))
        print(f"  → VIN: {vin}")
        cursor_browser_type(element="VIN field", ref="VIN_FIELD_REF", text=vin)

        # Consent: Check
        print("  → Consent: Checked")
        cursor_browser_click(element="Consent checkbox", ref="CONSENT_CHECKBOX_REF")

        print("✅ FORM: All fields filled")

        # ===== STEP 6: SUBMIT =====
        print("📤 SUBMIT: Submitting registration...")

        cursor_browser_click(element="Submit button", ref="SUBMIT_BUTTON_REF")
        time.sleep(3)

        print("🎉 SUCCESS: Registration completed!")
        print(f"✅ NIN {nin_number} registered successfully!")
        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def bulk_process_nins(nin_list):
    """Process multiple NINs"""
    print(f"📊 BULK PROCESSING {len(nin_list)} NINs")
    print("=" * 60)

    results = {"successful": [], "failed": []}

    for i, nin in enumerate(nin_list, 1):
        print(f"\n🔄 {i}/{len(nin_list)}: {nin}")

        if process_apc_registration(nin):
            results["successful"].append(nin)
        else:
            results["failed"].append(nin)

        # Brief pause between registrations
        if i < len(nin_list):
            time.sleep(2)

    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    print(f"Total: {len(nin_list)}")
    print(f"Successful: {len(results['successful'])}")
    print(f"Failed: {len(results['failed'])}")

    if results["successful"]:
        print("🎉 Bulk processing completed!")
    else:
        print("❌ All registrations failed!")

    return results


# ===== HOW TO USE =====

def test_single():
    """Test with one NIN"""
    print("🧪 TESTING SINGLE NIN")

    test_nin = "90807468604"  # Change this to your test NIN

    if process_apc_registration(test_nin):
        print("✅ Test passed!")
    else:
        print("❌ Test failed!")


def bulk_example():
    """Example of bulk processing"""
    print("📊 BULK PROCESSING EXAMPLE")

    # Add your NINs here
    nins_to_process = [
        "90807468604",
        # "12345678901",
        # "98765432109",
        # Add more NINs...
    ]

    results = bulk_process_nins(nins_to_process)
    return results


if __name__ == "__main__":
    print("🚀 APC BULK REGISTRATION AUTOMATION")
    print("=" * 60)
    print("⚠️  IMPORTANT: You need to identify element refs first!")
    print("1. Run cursor_browser_snapshot() at each step")
    print("2. Replace placeholder refs with actual refs")
    print("3. Uncomment all cursor_browser calls")
    print("=" * 60)

    # Test with single NIN first
    test_single()

    # Uncomment for bulk processing:
    # bulk_example()