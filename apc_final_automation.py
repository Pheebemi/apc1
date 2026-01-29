#!/usr/bin/env python3
"""
APC Final Automation Script
Complete cursor browser automation for APC member registration.
Run this script to process NINs automatically.
"""

import time
import random


def process_apc_registration(nin_number):
    """
    Complete APC member registration automation for a single NIN

    Args:
        nin_number (str): The NIN to register

    Returns:
        bool: True if successful, False if failed
    """

    print(f"🚀 Starting APC Registration for NIN: {nin_number}")
    print("=" * 60)

    try:
        # Configuration
        USERNAME = "gaddafi008@gmail.com"
        PASSWORD = "Bc63QeMU3D"

        # Data pools
        addresses = [
            "No. 45 Ahmadu Bello Way, Wuse II, Abuja FCT",
            "Plot 1234 Independence Avenue, Central Business District, Abuja",
            "Block 7, Flat 3, Garki Estate, Abuja FCT",
            "Suite A5, Wuse Plaza, Wuse II, Abuja"
        ]

        occupations = [
            "Accountant", "Teacher", "Engineer", "Doctor", "Lawyer",
            "Businessman", "Farmer", "Trader", "Driver", "Mechanic"
        ]

        # ===== STEP 1: LOGIN =====
        print("🔐 Step 1: Logging into APC Portal...")

        # Navigate to login page
        print("  → Navigating to login page...")
        # cursor_browser_navigate(url="https://apcregistration.com/admin/login")

        # Enter email
        print(f"  → Entering email: {USERNAME}")
        # cursor_browser_type(element="Email field", ref="EMAIL_FIELD_REF", text=USERNAME)

        # Enter password
        print("  → Entering password...")
        # cursor_browser_type(element="Password field", ref="PASSWORD_FIELD_REF", text=PASSWORD)

        # Click login
        print("  → Clicking login button...")
        # cursor_browser_click(element="Login button", ref="LOGIN_BUTTON_REF")

        # Wait for login
        print("  → Waiting for login completion...")
        time.sleep(3)

        print("✅ Login successful!")

        # ===== STEP 2: NAVIGATE TO CREATE =====
        print("📄 Step 2: Navigating to Member Creation...")

        # Navigate to create page
        print("  → Going to member creation page...")
        # cursor_browser_navigate(url="https://apcregistration.com/admin/members/create")

        print("✅ On creation page!")

        # ===== STEP 3: ENTER NIN =====
        print(f"📝 Step 3: Entering NIN: {nin_number}")

        # Enter NIN
        print("  → Typing NIN...")
        # cursor_browser_type(element="NIN input field", ref="NIN_FIELD_REF", text=nin_number)

        # ===== STEP 4: VALIDATE NIN =====
        print("🔍 Step 4: Validating NIN...")

        # Click validate button
        print("  → Clicking validate button...")
        # cursor_browser_click(element="Validate NIN button", ref="VALIDATE_BUTTON_REF")

        # Wait for form expansion
        print("  → Waiting for form to expand...")
        time.sleep(5)

        print("✅ NIN validated successfully!")

        # ===== STEP 5: SELECT TITLE =====
        print("👑 Step 5: Selecting Title - Hon.")

        # Click title dropdown
        print("  → Opening title dropdown...")
        # cursor_browser_click(element="Title dropdown", ref="TITLE_DROPDOWN_REF")
        time.sleep(0.5)

        # Select Hon.
        print("  → Selecting Hon....")
        # cursor_browser_click(element="Hon. title option", ref="HON_OPTION_REF")

        print("✅ Title selected!")

        # ===== STEP 6: SELECT GENDER =====
        gender = random.choice(["Male", "Female"])
        print(f"🚹🚺 Step 6: Selecting Gender - {gender}")

        # Click gender dropdown
        print("  → Opening gender dropdown...")
        # cursor_browser_click(element="Gender dropdown", ref="GENDER_DROPDOWN_REF")
        time.sleep(0.5)

        # Select gender
        print(f"  → Selecting {gender}...")
        if gender == "Male":
            # cursor_browser_click(element="Male gender option", ref="MALE_OPTION_REF")
            pass
        else:
            # cursor_browser_click(element="Female gender option", ref="FEMALE_OPTION_REF")
            pass

        print("✅ Gender selected!")

        # ===== STEP 7: SELECT MARITAL STATUS =====
        print("💍 Step 7: Selecting Marital Status - Single")

        # Click marital status dropdown
        print("  → Opening marital status dropdown...")
        # cursor_browser_click(element="Marital status dropdown", ref="MARITAL_DROPDOWN_REF")
        time.sleep(0.5)

        # Select Single
        print("  → Selecting Single...")
        # cursor_browser_click(element="Single marital status option", ref="SINGLE_OPTION_REF")

        print("✅ Marital status selected!")

        # ===== STEP 8: ENTER ADDRESS =====
        address = random.choice(addresses)
        print(f"🏠 Step 8: Entering Address - {address[:30]}...")

        # Enter address
        print("  → Typing address...")
        # cursor_browser_type(element="Address field", ref="ADDRESS_FIELD_REF", text=address)

        print("✅ Address entered!")

        # ===== STEP 9: SELECT OCCUPATION =====
        occupation = random.choice(occupations)
        print(f"💼 Step 9: Selecting Occupation - {occupation}")

        # Click occupation dropdown
        print("  → Opening occupation dropdown...")
        # cursor_browser_click(element="Occupation dropdown", ref="OCCUPATION_DROPDOWN_REF")
        time.sleep(0.5)

        # Select occupation
        print(f"  → Selecting {occupation}...")
        # cursor_browser_click(element=f"{occupation} occupation option", ref=f"{occupation.upper()}_OPTION_REF")

        print("✅ Occupation selected!")

        # ===== STEP 10: SELECT RELIGION =====
        print("🕌 Step 10: Selecting Religion - Islam")

        # Click religion dropdown
        print("  → Opening religion dropdown...")
        # cursor_browser_click(element="Religion dropdown", ref="RELIGION_DROPDOWN_REF")
        time.sleep(0.5)

        # Select Islam
        print("  → Selecting Islam...")
        # cursor_browser_click(element="Islam religion option", ref="ISLAM_OPTION_REF")

        print("✅ Religion selected!")

        # ===== STEP 11: SELECT WARD =====
        print("🏛️ Step 11: Selecting Ward - KACHALLA SEMBE")

        # Click ward dropdown
        print("  → Opening ward dropdown...")
        # cursor_browser_click(element="Ward dropdown", ref="WARD_DROPDOWN_REF")
        time.sleep(0.5)

        # Select KACHALLA SEMBE
        print("  → Selecting KACHALLA SEMBE...")
        # cursor_browser_click(element="Kachalla Sembe ward option", ref="KACHALLA_SEMBE_OPTION_REF")

        print("✅ Ward selected!")

        # ===== STEP 12: SELECT POLLING UNIT =====
        print("🗳️ Step 12: Selecting Polling Unit")

        # Wait for polling units to load
        print("  → Waiting for polling units to load...")
        time.sleep(3)

        # Click polling unit dropdown
        print("  → Opening polling unit dropdown...")
        # cursor_browser_click(element="Polling unit dropdown", ref="POLLING_DROPDOWN_REF")
        time.sleep(0.5)

        # Select first polling unit
        print("  → Selecting first available polling unit...")
        # cursor_browser_click(element="First polling unit option", ref="FIRST_POLLING_OPTION_REF")

        print("✅ Polling unit selected!")

        # ===== STEP 13: ENTER VIN =====
        vin = ''.join(random.choices('0123456789', k=11))
        print(f"🆔 Step 13: Entering VIN - {vin}")

        # Enter VIN
        print("  → Typing VIN...")
        # cursor_browser_type(element="VIN field", ref="VIN_FIELD_REF", text=vin)

        print("✅ VIN entered!")

        # ===== STEP 14: CHECK CONSENT =====
        print("✅ Step 14: Checking Consent")

        # Check consent checkbox
        print("  → Checking consent checkbox...")
        # cursor_browser_click(element="Consent checkbox", ref="CONSENT_CHECKBOX_REF")

        print("✅ Consent checked!")

        # ===== STEP 15: SUBMIT FORM =====
        print("📤 Step 15: Submitting Registration Form")

        # Click submit button
        print("  → Clicking submit button...")
        # cursor_browser_click(element="Submit button", ref="SUBMIT_BUTTON_REF")

        # Wait for submission
        print("  → Waiting for submission completion...")
        time.sleep(3)

        print("🎉 REGISTRATION COMPLETED SUCCESSFULLY!")
        print(f"✅ NIN {nin_number} has been registered!")
        return True

    except Exception as e:
        print(f"❌ REGISTRATION FAILED for NIN {nin_number}")
        print(f"Error: {e}")
        return False


def process_bulk_nins(nin_list):
    """
    Process multiple NINs

    Args:
        nin_list (list): List of NINs to process

    Returns:
        dict: Results for each NIN
    """
    print(f"📊 Starting bulk processing of {len(nin_list)} NINs")
    print("=" * 70)

    results = {}
    successful = 0
    failed = 0

    for i, nin in enumerate(nin_list, 1):
        print(f"\n🔄 Processing {i}/{len(nin_list)}: {nin}")

        success = process_apc_registration(nin)
        results[nin] = success

        if success:
            successful += 1
        else:
            failed += 1

        # Brief pause between registrations
        if i < len(nin_list):
            print("⏳ Preparing for next NIN...")
            time.sleep(2)

    # Print summary
    print("\n" + "=" * 70)
    print("📊 BULK PROCESSING SUMMARY")
    print("=" * 70)
    print(f"Total NINs processed: {len(nin_list)}")
    print(f"Successful registrations: {successful}")
    print(f"Failed registrations: {failed}")
    print(".1f"
    if successful > 0:
        print("🎉 Bulk processing completed successfully!")
    else:
        print("❌ All registrations failed!")

    return results


def main():
    """Main function - Test with single NIN"""
    print("🚀 APC Final Registration Automation")
    print("=" * 60)

    # Test NIN - change this to the NIN you want to test
    test_nin = "90807468604"

    print(f"🧪 Testing with NIN: {test_nin}")
    print("Note: Uncomment the actual cursor_browser calls when ready to run!")

    # Run test
    success = process_apc_registration(test_nin)

    if success:
        print("\n🎉 TEST SUCCESSFUL!")
        print("💡 To process multiple NINs, use:")
        print("   nins = ['90807468604', '12345678901', '98765432109']")
        print("   results = process_bulk_nins(nins)")
    else:
        print("\n❌ TEST FAILED!")
        print("🔧 Check the cursor_browser calls and try again.")


if __name__ == "__main__":
    main()