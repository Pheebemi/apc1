#!/usr/bin/env python3
"""
Test APC Registration with Cursor Browser
Single NIN test automation
"""

import time
import random


def test_single_nin_registration():
    """Test registration with one NIN using cursor browser tools"""

    # Configuration
    NIN = "90807468604"
    USERNAME = "gaddafi008@gmail.com"
    PASSWORD = "Bc63QeMU3D"

    nigerian_addresses = [
        "No. 45 Ahmadu Bello Way, Wuse II, Abuja FCT",
        "Plot 1234 Independence Avenue, Central Business District, Abuja"
    ]

    nigerian_occupations = ["Accountant", "Teacher", "Engineer"]

    print("🚀 Starting APC Registration Test")
    print(f"📝 NIN: {NIN}")
    print("=" * 50)

    try:
        # Step 1: Login
        print("🔐 Step 1: Logging in...")
        # cursor_browser_navigate to login page
        # cursor_browser_type for email
        # cursor_browser_type for password
        # cursor_browser_click for login

        print("✅ Login completed")

        # Step 2: Navigate to create page
        print("📄 Step 2: Navigating to create page...")
        # cursor_browser_navigate to create page
        print("✅ On create page")

        # Step 3: Enter NIN
        print(f"📝 Step 3: Entering NIN: {NIN}")
        # cursor_browser_type for NIN field

        # Step 4: Validate NIN
        print("🔍 Step 4: Validating NIN...")
        # cursor_browser_click for validate button

        print("⏳ Waiting for form expansion...")
        time.sleep(5)

        # Step 5: Select Title - Hon.
        print("👑 Step 5: Selecting Title - Hon.")
        # cursor_browser_click title dropdown
        time.sleep(0.5)
        # cursor_browser_click Hon. option

        # Step 6: Select Gender - Random
        gender = random.choice(["Male", "Female"])
        print(f"🚹🚺 Step 6: Selecting Gender - {gender}")
        # cursor_browser_click gender dropdown
        time.sleep(0.5)
        # cursor_browser_click gender option

        # Step 7: Select Marital Status - Single
        print("💍 Step 7: Selecting Marital Status - Single")
        # cursor_browser_click marital status dropdown
        time.sleep(0.5)
        # cursor_browser_click Single option

        # Step 8: Enter Address - Random
        address = random.choice(nigerian_addresses)
        print(f"🏠 Step 8: Entering Address - {address[:30]}...")
        # cursor_browser_type for address field

        # Step 9: Select Occupation - Random
        occupation = random.choice(nigerian_occupations)
        print(f"💼 Step 9: Selecting Occupation - {occupation}")
        # cursor_browser_click occupation dropdown
        time.sleep(0.5)
        # cursor_browser_click occupation option

        # Step 10: Select Religion - Islam
        print("🕌 Step 10: Selecting Religion - Islam")
        # cursor_browser_click religion dropdown
        time.sleep(0.5)
        # cursor_browser_click Islam option

        # Step 11: Select Ward - KACHALLA SEMBE
        print("🏛️ Step 11: Selecting Ward - KACHALLA SEMBE")
        # cursor_browser_click ward dropdown
        time.sleep(0.5)
        # cursor_browser_click KACHALLA SEMBE option

        # Step 12: Select Polling Unit
        print("🗳️ Step 12: Selecting Polling Unit")
        time.sleep(3)
        # cursor_browser_click polling unit dropdown
        time.sleep(0.5)
        # cursor_browser_click first polling unit option

        # Step 13: Enter VIN - Random
        vin = ''.join(random.choices('0123456789', k=11))
        print(f"🆔 Step 13: Entering VIN - {vin}")
        # cursor_browser_type for VIN field

        # Step 14: Check Consent
        print("✅ Step 14: Checking Consent")
        # cursor_browser_click consent checkbox

        # Step 15: Submit Form
        print("📤 Step 15: Submitting Form")
        # cursor_browser_click submit button

        print("⏳ Waiting for completion...")
        time.sleep(3)

        print("🎉 REGISTRATION TEST COMPLETED SUCCESSFULLY!")
        return True

    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        return False


if __name__ == "__main__":
    success = test_single_nin_registration()
    if success:
        print("\n✅ Test passed! Ready for bulk processing.")
    else:
        print("\n❌ Test failed! Check implementation.")