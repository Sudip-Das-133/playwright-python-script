import os
import re
import time

from pathlib import Path

from playwright.sync_api import (
    sync_playwright,
    expect,
    TimeoutError as PlaywrightTimeoutError
)


# ============================================================
# 1. TEST DATA AND CONFIGURATION
# ============================================================


# ============================================================
# CONFIGURATION
# ============================================================

URL = "https://org.dev.invorush.com/"

EMAIL = "abcd@mailinator.com"
PASSWORD = "password2026"

EXCEL_FILE = Path(
    r"C:\Users\Lenovo\Downloads\sample (8).xlsx"
)

ORGANIZATION_NAME = "SAPPHIRO CONSULTING SOLUTIONS PRIVATE LIMITED"

# HDFC TEST CARD DETAILS — use authorized test credentials only
CARD_NUMBER = "4012 0000 0000 1097"
CARD_EXPIRY = "12/32"
CARD_CVV = "123"
CARD_HOLDER_NAME = "TEST USER"

# Keep False until you are ready to submit an authorized test payment.
ALLOW_TEST_PAYMENT_SUBMIT = True

ORGANIZATION = "SAPPHIRO CONSULTING SOLUTIONS PRIVATE LIMITED"



REQUIRED_GATEWAY = "HDFC"
REQUIRED_RATE = "T0 - 2.5%"

# Use only authorized test card details.

CARD_NAME = os.getenv("HDFC_TEST_CARD_NAME", "TEST USER")

# Final submission is disabled unless explicitly enabled.


SCREENSHOT_PATH = Path("bulk_transaction_error.png")


# ============================================================
# 2. VALIDATE TEST DATA
# ============================================================

if not EMAIL or not PASSWORD:
    raise ValueError(
        "Set INVORUSH_EMAIL and INVORUSH_PASSWORD environment variables."
    )

if not EXCEL_FILE.is_file():
    raise FileNotFoundError(
        f"Excel file not found: {EXCEL_FILE}"
    )

if not all([CARD_NUMBER, CARD_EXPIRY, CARD_CVV]):
    raise ValueError(
        "Set HDFC_TEST_CARD_NUMBER, HDFC_TEST_CARD_EXPIRY "
        "and HDFC_TEST_CARD_CVV environment variables."
    )


# ============================================================
# 3. MAIN EXECUTION
# ============================================================

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context()

    page = context.new_page()

    page.set_default_timeout(15000)

    hdfc_page = None
    new_page = None

    try:

        # ====================================================
        # STEP 1: OPEN APPLICATION
        # ====================================================

        page.goto(
            URL,
            wait_until="domcontentloaded"
        )

        print("Application opened successfully")


        # ====================================================
        # STEP 2: LOGIN
        # ====================================================

        email_field = page.locator(
            "//input[@name='email']"
        )

        expect(email_field).to_be_visible()

        email_field.fill(EMAIL)

        password_field = page.get_by_placeholder(
            "Enter your password"
        )

        expect(password_field).to_be_visible()

        password_field.fill(PASSWORD)

        sign_in_button = page.get_by_text(
            "Sign In",
            exact=True
        )

        sign_in_button.click()

        print("Login button clicked")

        bulk_list_indicator = page.get_by_text(
            "Bulk Transaction List",
            exact=True
        )

        expect(
            bulk_list_indicator
        ).to_be_visible(timeout=30000)

        print("Login successful")


        # ====================================================
        # STEP 3: OPEN BULK TRANSACTION LIST
        # ====================================================

        bulk_transaction_list = page.get_by_text(
            "Bulk Transaction List",
            exact=True
        )

        bulk_transaction_list.click()

        print("Bulk Transaction List opened")


        # ====================================================
        # STEP 4: CREATE BULK TRANSACTION
        # ====================================================

        create_bulk_transaction = page.get_by_text(
            "Create Bulk Transaction",
            exact=True
        )

        expect(
            create_bulk_transaction
        ).to_be_visible()

        create_bulk_transaction.click()

        print("Create Bulk Transaction clicked")


        # ====================================================
        # STEP 5: SELECT ORGANIZATION
        # ====================================================

        organization_dropdown = page.get_by_text(
            "Search organization",
            exact=True
        )

        expect(
            organization_dropdown
        ).to_be_visible()

        organization_dropdown.click()

        organization_option = page.locator(
            f"//div[@data-value={repr(ORGANIZATION)}]"
        )

        expect(
            organization_option
        ).to_be_visible()

        organization_option.click()

        print("Organization selected:", ORGANIZATION)


        # ====================================================
        # STEP 6: CLICK NEXT AFTER ORGANIZATION
        # ====================================================

        next_button = page.locator(
            "button[type='submit']"
        )

        expect(next_button).to_be_enabled()

        next_button.click()

        print("Organization selection completed")


        # ====================================================
        # STEP 7: UPLOAD EXCEL FILE
        # ====================================================

        file_to_upload = page.locator(
            "#file"
        )

        expect(
            file_to_upload
        ).to_be_attached()

        file_to_upload.set_input_files(
            str(EXCEL_FILE)
        )

        uploaded_filename = file_to_upload.evaluate(
            "(element) => element.files[0]?.name"
        )

        assert uploaded_filename == EXCEL_FILE.name, (
            f"Excel upload failed. Actual filename: {uploaded_filename}"
        )

        print(
            "Excel file uploaded successfully:",
            uploaded_filename
        )


        # ====================================================
        # STEP 8: CLICK NEXT AFTER EXCEL UPLOAD
        # ====================================================

        next_button = page.locator(
            "button[type='submit']"
        )

        expect(next_button).to_be_enabled()

        next_button.click()

        print("Excel upload step completed")


        # ====================================================
        # STEP 9: SELECT PAYMENT GATEWAY
        # ====================================================

        payment_gateway = page.get_by_role(
            "combobox"
        ).filter(
            has_text=re.compile(
                r"^\s*Select Payment Gateway\s*$"
            )
        )

        expect(
            payment_gateway
        ).to_have_count(1)

        expect(
            payment_gateway
        ).to_be_visible()

        current_gateway = (
            payment_gateway.inner_text().strip()
        )

        print(
            "Current Payment Gateway:",
            current_gateway
        )

        if current_gateway != REQUIRED_GATEWAY:

            payment_gateway.click()

            print("Payment Gateway dropdown opened")

            hdfc_gateway_option = page.get_by_role(
                "option",
                name=REQUIRED_GATEWAY,
                exact=True
            )

            expect(
                hdfc_gateway_option
            ).to_be_visible()

            hdfc_gateway_option.click()

            print("HDFC Payment Gateway selected")

        else:

            print("HDFC Gateway already selected")


        # ====================================================
        # STEP 10: SELECT PAYMENT GATEWAY RATE
        # ====================================================

        rate_label = page.locator(
            "label[data-slot='form-label']"
        ).filter(
            has_text=re.compile(r"^\s*Rate\b")
        )

        expect(
            rate_label
        ).to_be_visible()

        rate_dropdown = rate_label.locator(
            "xpath=.."
        ).locator(
            "button[role='combobox']"
        )

        expect(
            rate_dropdown
        ).to_be_visible()

        rate_dropdown.click()

        print("Rate dropdown opened")

        rate_option = page.get_by_role(
            "option",
            name=REQUIRED_RATE,
            exact=True
        )

        expect(
            rate_option
        ).to_be_visible()

        rate_option.click()

        print("Rate selected:", REQUIRED_RATE)

        expect(
            rate_dropdown
        ).to_contain_text(REQUIRED_RATE)

        print("Rate selection verified")


        # ====================================================
        # STEP 11: CLICK NEXT AFTER GATEWAY AND RATE
        # ====================================================

        next_button = page.locator(
            "//button[@type='submit']"
        )

        expect(next_button).to_be_enabled()

        next_button.click()

        print("Payment gateway and rate selection completed")


        # ====================================================
        # STEP 12: RETURN TO BULK TRANSACTION LIST
        # ====================================================

        list_bulk_transaction = page.get_by_role(
            "button",
            name="List Bulk Transactions",
            exact=True
        )

        expect(
            list_bulk_transaction
        ).to_be_visible()

        list_bulk_transaction.click()

        print("Returned to Bulk Transaction List")


        ### Reload the webpage :

        page.reload()
        time.sleep(2)

        # ====================================================
        # STEP 13: OPEN THREE-DOT MENU
        # ====================================================


        three_dot = page.locator("//button[@data-slot='dropdown-menu-trigger']").nth(4)
        three_dot.click()

        print("Bulk Transaction three-dot menu opened")


        # ====================================================
        # STEP 14: APPROVE BULK TRANSACTION
        # ====================================================

        approve_transaction = page.get_by_text(
            "Approve",
            exact=True
        )

        expect(
            approve_transaction
        ).to_be_visible()

        approve_transaction.click()

        print("Approve option selected")


        # ====================================================
        # STEP 15: CLICK CONTINUE
        # ====================================================

        continue_button = page.get_by_role(
            "button",
            name="Continue",
            exact=True
        )

        expect(
            continue_button
        ).to_be_visible()

        expect(
            continue_button
        ).to_be_enabled()

        continue_button.click()

        print("Bulk Transaction approval continued")


        time.sleep(5)


        # ====================================================
        # STEP 16: OPEN THREE-DOT MENU AGAIN
        # ====================================================

        three_dot = page.locator("//button[@data-slot='dropdown-menu-trigger']").nth(4)
        three_dot.click()

        print("Three-dot menu opened again")


        # ====================================================
        # STEP 17: CLICK PAYMENT OPTION
        # ====================================================

        payment_option = page.get_by_text(
            "Payment",
            exact=True
        )

        expect(
            payment_option
        ).to_be_visible(timeout=30000)

        payment_option.click()

        print("Payment option selected")


        # ====================================================
        # STEP 18: CLICK PAY SECURELY NOW
        # ====================================================

        pay_securely_now_button = page.get_by_role(
            "button",
            name="Pay Securely Now",
            exact=True
        )

        expect(
            pay_securely_now_button
        ).to_be_visible(timeout=30000)

        expect(
            pay_securely_now_button
        ).to_be_enabled()

        # Capture HDFC popup.

        with page.expect_popup(timeout=30000) as popup_info:

            pay_securely_now_button.click()

        hdfc_page = popup_info.value

        print("HDFC Payment Gateway window opened")

        hdfc_page.wait_for_load_state(
            "domcontentloaded",
            timeout=30000
        )

        print("HDFC Payment URL:", hdfc_page.url)

        print("HDFC Payment Title:", hdfc_page.title())


        # ====================================================
        # STEP 19: CLICK ADD CREDIT/DEBIT CARDS
        # ====================================================

        add_credit_card = hdfc_page.get_by_text(
            "Add Credit/Debit Cards",
            exact=True
        )

        expect(
            add_credit_card
        ).to_be_visible(timeout=30000)

        add_credit_card.click()

        print("Add Credit/Debit Cards clicked")


        # ====================================================
        # STEP 20: ENTER CARD NUMBER
        # ====================================================

        card_number = hdfc_page.get_by_placeholder(
            "Enter Card Number"
        )

        expect(
            card_number
        ).to_be_visible(timeout=30000)

        card_number.fill(CARD_NUMBER)

        print("Card number entered")


        # ====================================================
        # STEP 21: ENTER EXPIRY DATE
        # ====================================================

        expiry_date = hdfc_page.get_by_placeholder(
            "MM/YY"
        )

        expect(
            expiry_date
        ).to_be_visible(timeout=30000)

        expiry_date.fill(CARD_EXPIRY)

        print("Expiry date entered")


        # ====================================================
        # STEP 22: ENTER CVV
        # ====================================================

        cvv_number = hdfc_page.get_by_placeholder(
            "Enter CVV"
        )

        expect(
            cvv_number
        ).to_be_visible(timeout=30000)

        cvv_number.fill(CARD_CVV)

        print("CVV entered")


        # ====================================================
        # STEP 23: ENTER NAME ON CARD
        # ====================================================

        name_of_card = hdfc_page.get_by_placeholder(
            "Enter your name on card"
        )

        expect(
            name_of_card
        ).to_be_visible(timeout=30000)

        name_of_card.fill(CARD_NAME)

        print("Name on card entered")


        # ====================================================
        # STEP 24: CLICK PROCEED TO PAY
        # ====================================================

        proceed_to_pay_button = hdfc_page.locator(
            "//article[contains(normalize-space(.), 'proceed to pay')]"
        )

        expect(
            proceed_to_pay_button
        ).to_be_visible(timeout=30000)

        proceed_to_pay_button.click()

        print("Proceed to Pay clicked")


        # ====================================================
        # STEP 25: CLICK SECURE & PAY
        # ====================================================

        secure_and_pay_button = hdfc_page.locator(
            "//article[normalize-space()='Secure & Pay']"
        )

        expect(
            secure_and_pay_button
        ).to_be_visible(timeout=30000)

        secure_and_pay_button.click()

        print("Secure & Pay clicked")


        # ====================================================
        # STEP 26: CLICK TO PROCEED
        # ====================================================

        click_to_proceed_button = hdfc_page.locator(
            "//article[normalize-space()='Click to proceed']"
        )

        expect(
            click_to_proceed_button
        ).to_be_visible(timeout=30000)

        print("Click to proceed button found")


        # ====================================================
        # STEP 27: CAPTURE SECOND POPUP
        # ====================================================

        with hdfc_page.expect_popup(
            timeout=30000
        ) as popup_info_2:

            click_to_proceed_button.click()

        new_page = popup_info_2.value

        print("New HDFC verification window opened")

        new_page.wait_for_load_state(
            "domcontentloaded",
            timeout=30000
        )

        print("New Window URL:", new_page.url)

        print("New Window Title:", new_page.title())


        # ====================================================
        # STEP 28: OPEN TRANSACTION STATE DROPDOWN
        # ====================================================

        select_transaction_state = new_page.locator(
            "//div[@id='txnStateDropdownText']"
        )

        expect(
            select_transaction_state
        ).to_be_visible(timeout=30000)

        select_transaction_state.click()

        print("Transaction state dropdown opened")


        # ====================================================
        # STEP 29: SELECT CHARGED OPTION
        # ====================================================

        option_selection = new_page.locator(
            "//li[@class='dropdown-item' and @data-value='CHARGED']"
        )

        expect(
            option_selection
        ).to_be_visible(timeout=30000)

        option_selection.click()

        print("CHARGED option selected")


        # ====================================================
        # STEP 30: VERIFY SUBMIT BUTTON
        # ====================================================

        submit_button = new_page.locator(
            "//button[@id='submitButton']"
        )

        expect(
            submit_button
        ).to_be_visible(timeout=30000)

        expect(
            submit_button
        ).to_be_enabled()

        print("Submit button is ready")


        # ====================================================
        # STEP 31: FINAL PAYMENT SUBMISSION
        # ====================================================

        if ALLOW_TEST_PAYMENT_SUBMIT:

            submit_button.click()

            print("Test payment submission button clicked")

            print(
                "Payment submission action completed. "
                "Verify the actual gateway response."
            )

        else:

            print("------------------------------------------")
            print("FINAL PAYMENT SUBMISSION NOT EXECUTED")
            print("------------------------------------------")

            print(
                "To enable authorized test submission, "
                "set ALLOW_TEST_PAYMENT_SUBMIT=YES."
            )


        # ====================================================
        # STEP 32: FINAL EXECUTION REPORT
        # ====================================================

        print("\n")
        print("=" * 55)
        print("BULK TRANSACTION AUTOMATION EXECUTION REPORT")
        print("=" * 55)

        print("Application Login          : SUCCESS")
        print("Organization Selection     : SUCCESS")
        print("Excel Upload               : SUCCESS")
        print("Payment Gateway            : HDFC")
        print("Payment Gateway Rate       :", REQUIRED_RATE)
        print("Bulk Transaction Approval  : SUBMITTED")
        print("Payment Option             : SELECTED")
        print("HDFC Payment Window        : OPENED")
        print("Card Details               : ENTERED")
        print("Transaction State          : CHARGED")
        print("Final payment submission   : SUBMITTED")

        if ALLOW_TEST_PAYMENT_SUBMIT:
            print("Final Submit               : CLICKED")
        else:
            print("Final Submit               : SKIPPED")

        print("=" * 55)

        print(
            "Automation reached the final configured step."
        )


        # ====================================================
        # OPTIONAL DEBUG PAUSE
        # ====================================================

        if os.getenv("DEBUG_PAUSE") == "YES":
            page.pause()


    # ========================================================
    # 4. EXCEPTION HANDLING
    # ========================================================

    except FileNotFoundError as error:

        print("\nFILE ERROR:")
        print(error)


    except PlaywrightTimeoutError as error:

        print("\nPLAYWRIGHT TIMEOUT ERROR:")
        print(error)


        # Capture HDFC screenshot if available.

        try:

            if hdfc_page and not hdfc_page.is_closed():

                hdfc_page.screenshot(
                    path="hdfc_payment_error.png",
                    full_page=True
                )

                print("HDFC error screenshot saved")


            if new_page and not new_page.is_closed():

                new_page.screenshot(
                    path="hdfc_verification_error.png",
                    full_page=True
                )

                print("HDFC verification screenshot saved")


            if not page.is_closed():

                page.screenshot(
                    path=str(SCREENSHOT_PATH),
                    full_page=True
                )

                print("Invorush error screenshot saved")

        except Exception as screenshot_error:

            print("Screenshot error:", screenshot_error)


    except Exception as error:

        print("\nUNEXPECTED ERROR:")
        print(type(error).__name__, ":", error)


        try:

            if hdfc_page and not hdfc_page.is_closed():

                hdfc_page.screenshot(
                    path="hdfc_payment_error.png",
                    full_page=True
                )


            if new_page and not new_page.is_closed():

                new_page.screenshot(
                    path="hdfc_verification_error.png",
                    full_page=True
                )


            if not page.is_closed():

                page.screenshot(
                    path=str(SCREENSHOT_PATH),
                    full_page=True
                )

            print("Error screenshots saved")

        except Exception as screenshot_error:

            print("Screenshot error:", screenshot_error)


    finally:

        browser.close()

        print("\nBrowser closed")