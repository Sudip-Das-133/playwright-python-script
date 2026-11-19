#
# import re
# from pathlib import Path
#
# from playwright.sync_api import (
#     sync_playwright,
#     expect,
#     TimeoutError as PlaywrightTimeoutError
# )
#
#
# # ========================================================
# # TEST DATA
# # ========================================================
#
# URL = "https://org.dev.invorush.com/"
#
# EMAIL = "newscenarictravelsllp@gmail.com"
# PASSWORD = "password2026"
#
# ORGANIZATION = "SAPPHIRO CONSULTING SOLUTIONS PRIVATE LIMITED"
#
# EXCEL_FILE = Path(
#     r"C:\Users\Lenovo\Downloads\sample (8).xlsx"
# )
#
#
# # ========================================================
# # MAIN EXECUTION
# # ========================================================
#
# with sync_playwright() as p:
#
#     browser = p.chromium.launch(
#         headless=False
#     )
#
#     page = browser.new_page()
#
#     page.set_default_timeout(15000)
#
#     try:
#
#         # ========================================================
#         # 1. OPEN APPLICATION
#         # ========================================================
#
#         page.goto(URL, wait_until="domcontentloaded")
#
#         print("Application opened successfully")
#
#
#         # ========================================================
#         # 2. LOGIN
#         # ========================================================
#
#         email_field = page.locator(
#             "//input[@name='email']"
#         )
#
#         email_field.fill(EMAIL)
#
#         password_field = page.get_by_placeholder(
#             "Enter your password"
#         )
#
#         password_field.fill(PASSWORD)
#
#         sign_in_button = page.get_by_text(
#             "Sign In",
#             exact=True
#         )
#
#         sign_in_button.click()
#
#         print("Login button clicked")
#
#         # Wait for successful navigation.
#         # Adjust this assertion if your application uses another
#         # reliable post-login indicator.
#
#         page.get_by_text(
#             "Bulk Transaction List",
#             exact=True
#         ).wait_for(state="visible")
#
#         print("Login successful")
#
#
#         # ========================================================
#         # 3. OPEN BULK TRANSACTION LIST
#         # ========================================================
#
#         bulk_transaction_list = page.get_by_text(
#             "Bulk Transaction List",
#
#             exact=True
#         )
#
#         bulk_transaction_list.click()
#
#         print("Bulk Transaction List opened")
#
#
#         # ========================================================
#         # 4. CLICK CREATE BULK TRANSACTION
#         # ========================================================
#
#         create_bulk_transaction = page.get_by_text(
#             "Create Bulk Transaction",
#             exact=True
#         )
#
#         create_bulk_transaction.click()
#
#         print("Create Bulk Transaction button clicked")
#
#
#         # ========================================================
#         # 5. ORGANIZATION SELECTION
#         # ========================================================
#
#         organization_dropdown = page.get_by_text(
#             "Search organization",
#             exact=True
#         )
#
#         organization_dropdown.click()
#
#         # Select organization
#
#         organization_option = page.locator(
#             f"//div[@data-value={repr(ORGANIZATION)}]"
#         )
#
#         expect(organization_option).to_be_visible()
#
#         organization_option.click()
#
#         print("Organization selected:", ORGANIZATION)
#
#
#         # ========================================================
#         # 6. CLICK NEXT BUTTON
#         # ========================================================
#
#         next_button = page.locator(
#             "button[type='submit']"
#         )
#
#         next_button.click()
#
#         print("Organization selection completed")
#
#
#         # ========================================================
#         # 7. EXCEL FILE UPLOAD
#         # ========================================================
#
#         if not EXCEL_FILE.is_file():
#             raise FileNotFoundError(
#                 f"Excel file not found: {EXCEL_FILE}"
#             )
#
#         file_to_upload = page.locator(
#             "#file"
#         )
#
#         file_to_upload.set_input_files(
#             str(EXCEL_FILE)
#         )
#
#         # Verify uploaded filename
#
#         uploaded_filename = file_to_upload.evaluate(
#             "(element) => element.files[0]?.name"
#         )
#
#         assert uploaded_filename == EXCEL_FILE.name, (
#             f"File upload verification failed. "
#             f"Actual file: {uploaded_filename}"
#         )
#
#         print("Excel file uploaded successfully:", uploaded_filename)
#
#
#         # ========================================================
#         # 8. CLICK NEXT BUTTON AFTER FILE UPLOAD
#         # ========================================================
#
#         next_button = page.locator(
#             "button[type='submit']"
#         )
#
#         next_button.click()
#
#         print("Excel upload step completed")
#
#
#         # ========================================================
#         # 9. PAYMENT GATEWAY SELECTION
#         # ========================================================
#
#         # Your HTML contains two comboboxes:
#         #
#         # 1. Select Payment Gateway
#         # 2. Select Payment Gateway First
#         #
#         # We need the first one specifically.
#
#         payment_gateway = page.get_by_role(
#             "combobox"
#         ).filter(
#             has_text=re.compile(
#                 r"^\s*Select Payment Gateway\s*$"
#             )
#         )
#
#         # Verify that exactly one dropdown matches
#
#         expect(payment_gateway).to_have_count(1)
#
#         expect(payment_gateway).to_be_visible()
#
#         # Check current dropdown value
#
#         current_gateway = payment_gateway.inner_text().strip()
#
#         print("Current Payment Gateway:", current_gateway)
#
#         if current_gateway != "HDFC":
#
#             # Open Payment Gateway dropdown
#
#             payment_gateway.click()
#
#             print("Payment Gateway dropdown opened")
#
#             # Locate HDFC option.
#             # This assumes the opened custom dropdown exposes
#             # its options using role="option".
#
#             hdfc_option = page.get_by_role(
#                 "option",
#                 name="HDFC",
#                 exact=True
#             )
#
#             expect(hdfc_option).to_be_visible()
#
#             # Select HDFC
#
#             hdfc_option.click()
#
#             print("HDFC Payment Gateway selected")
#
#         else:
#
#             print("HDFC is already selected")
#
#         #
#         # # ========================================================
#         # # 10. VERIFY PAYMENT GATEWAY
#         # # ========================================================
#         #
#         # expect(payment_gateway).to_contain_text(
#         #     "HDFC"
#         #
#         #
#         # print("Payment Gateway validation successful")
#
#         # ========================================================
#         # 11. SELECT RATE OF INTEREST OF PAYMENT GATEWAY :
#         # ========================================================
#         # ========================================================
#         # 11. SELECT RATE
#         # ========================================================
#
#         # Find Rate label
#         rate_label = page.locator(
#             "label[data-slot='form-label']"
#         ).filter(
#             has_text=re.compile(r"^\s*Rate\b")
#         )
#
#         # Verify label
#         expect(rate_label).to_be_visible()
#
#         # Find dropdown belonging to Rate
#         rate_dropdown = rate_label.locator(
#             "xpath=.."
#         ).locator(
#             "button[role='combobox'][data-slot='select-trigger']"
#         )
#
#         # Verify dropdown
#         expect(rate_dropdown).to_be_visible()
#
#         print("Rate dropdown located successfully")
#
#         # Open Rate dropdown
#         rate_dropdown.click()
#
#         print("Rate dropdown opened successfully")
#
#         # Select required rate
#         required_rate = "T0 - 1.78%"
#
#         rate_option = page.get_by_role(
#             "option",
#             name=required_rate,
#             exact=True
#         )
#
#         # Wait for option
#         expect(rate_option).to_be_visible()
#
#         # Click option
#         rate_option.click()
#
#         print("Rate selected:", required_rate)
#
#         # Verify selected rate
#         expect(rate_dropdown).to_contain_text(required_rate)
#
#         print("Rate selection verified successfully")
#
#
#         # ====================================================================
#         # 11 : AFTER SELECT PAYMENT GATEWAY AND RATE , CLICK ON THE 'NEXT' BUTTON :
#         # ====================================================================
#
#         Next_Button = page.locator(
#             "//button[@type='submit']"
#         )
#
#         Next_Button.click()
#
#         print("Payment gateway and bulk transaction rate selected successfully")
#
#
#         # =====================================================================
#         # 12 : NOW CLICK ON THE 'LIST BULK TRANSACTION' BUTTON :
#         # =====================================================================
#
#         list_bulk_transaction = page.locator(
#             "//button[text()='List Bulk Transactions']"
#         )
#
#         list_bulk_transaction.click()
#
#         print("Successfully go back to the list of bulk transaction ")
#
#
#         # =======================================================================
#         # 13 : CLICK ON THE THREE DOT
#         # ========================================================================
#
#         three_dot = page.locator("//button[@data-slot='dropdown-menu-trigger']").nth(4)
#         three_dot.click()
#
#         print("Successfully clicked on the three dot option ")
#
#
#         # ==============================================================================
#         # 14 : Approve specific bulk transaction
#         # ==============================================================================
#
#         Approve_transaction = page.locator(
#             "(//span[text()='Approve'])"
#         )
#         Approve_transaction.click()
#         print("Approved the specific bulk transaction ")
#         # ==================================================================================
#         # 15 : CLICK ON THE 'CONTINUE' BUTTON :
#         # ===================================================================================
#
#         Continue_button = page.locator(
#             "(//button[text()='Continue'])"
#         )
#         Continue_button.click()
#
#         print("Continue with that specific bulk transaction ")
#
#
#         # =======================================================================
#         # 16 : AGAIN CLICK ON THE THREE DOT
#         # ========================================================================
#
#         three_dot = page.locator("//button[@data-slot='dropdown-menu-trigger']").nth(4)
#         three_dot.click()
#
#         print("Again click on the three dot option ")
#
#         # ==========================================================================
#         # 17 : CLICK ON THE PAYMENT OPTION BUTTON :
#         # =========================================================================
#
#         payment_option = page.locator(
#             "(//span[text()='Payment'])"
#         )
#         payment_option.wait_for(
#             state="visible",
#             timeout=30000
#         )
#         payment_option.click()
#
#         print("Successfully click on the payment option ")
#
#
#         # ============================================================================
#         # 18 : CLICK ON THE 'PAY SECURELY NOW' BUTTON :
#         # =============================================================================
#
#
#         pay_securely_now_button = page.locator(
#             "(//button[text()='Pay Securely Now'])"
#         )
#
#         pay_securely_now_button.wait_for(
#             state="visible",
#             timeout=30000
#         )
#
#         with page.expect_popup(timeout=30000) as popup_info:
#             pay_securely_now_button.click()
#
#         print("Successfully clicked on the pay securely now button ")
#
#         # ============================================================================
#         # 19 : SELECT THE HDFC BANK PAYMENT OPTION IN THE HDFC PAYMENT WINDOW:
#         # =============================================================================
#
#         Hdfc_window = popup_info.value
#         print("HDFC payment window opened")
#
#         hdfc_option = page.locator(
#             'div[configpath="PaymentPage.Expanded.NB.ListItem|topView|firstLine"]'
#         )
#         hdfc_option.wait_for(
#             state="visible",
#             timeout=30000
#         )
#
#         hdfc_option.click()
#
#         print(" Successfully select the payment option ")
#
#
#
#         # =================================================================================
#         # 20 " CLICK ON THE PROCEED TO PAY BUTTON :
#         # =================================================================================
#
#         Proceed_to_pay_button = page.locator(
#             "//article[text() ='proceed to pay ']"
#         )
#         Proceed_to_pay_button.click()
#
#         print("Successfully clicked on the proceed to pay button ")
#
#         # ==================================================================================
#         # 21 : CLICK ON THE 'TRANSACTION STATE' DROPDOWN
#         # ===================================================================================
#
#         Select_transaction_state = page.locator(
#             "//button[@id ='txnStateDropdownToggle']"
#         )
#         Select_transaction_state.click()
#
#
#
#         # ===============================================================================
#         # 22 : SELECT CHARGED OPTION FROM THE DROPDOWN
#         # ===============================================================================
#
#         Option_selection = page.locator(
#             "//span[text()='CHARGED']"
#         )
#         Option_selection.click()
#
#         print(" successfully select on the charged option from the dropdown ")
#
#         # ==========================================================================
#         # 23 : CLICK ON THE SUBMIT BUTTON
#         # ==========================================================================
#
#         click_submit_button = page.locator(
#             "//button[@id='submitButton']"
#         )
#
#         click_submit_button.click()
#
#         print("At the very end click on the submit button ")
#
#
#         print(" As of now bulk transaction is completed ")
#
#
#
#
#
#         # ========================================================
#         # 11. FINAL VALIDATION :
#         # ========================================================
#
#         print("--------------------------------------")
#         print("BULK TRANSACTION AUTOMATION COMPLETED")
#         print("--------------------------------------")
#
#         print("Login                  : SUCCESS")
#         print("Organization Selection : SUCCESS")
#         print("Excel Upload           : SUCCESS")
#         print("Payment Gateway        : HDFC")
#         print("Rate Selected          : T0 - 1.78% ")
#         print("Click on the bulk transaction list :")
#         print("--------------------------------------")
#
#
#         # Keep browser open for manual inspection
#
#         page.pause()
#
#
#     except FileNotFoundError as error:
#
#         print("FILE ERROR:", error)
#
#     except PlaywrightTimeoutError as error:
#
#         print("PLAYWRIGHT TIMEOUT ERROR:")
#         print(error)
#
#         page.screenshot(
#             path="bulk_transaction_error.png",
#             full_page=True
#         )
#
#         print("Error screenshot saved")
#
#
#     except Exception as error:
#
#         print("UNEXPECTED ERROR:")
#         print(error)
#
#         page.screenshot(
#             path="bulk_transaction_error.png",
#             full_page=True
#         )
#
#         print("Error screenshot saved")
#
#
#     finally:
#
#         browser.close()
#
#









































import os
import re
from pathlib import Path
import time

from playwright.sync_api import (
    sync_playwright,
    expect,
    TimeoutError as PlaywrightTimeoutError
)


# ============================================================
# 1. TEST DATA AND CONFIGURATION
# ============================================================

URL = "https://org.dev.invorush.com/"

EMAIL = os.getenv("newscenarictravelsllp@gmail.com")
PASSWORD = os.getenv("password2026")

ORGANIZATION = "SAPPHIRO CONSULTING SOLUTIONS PRIVATE LIMITED"

EXCEL_FILE = Path(
    r"C:\Users\Lenovo\Downloads\sample (8).xlsx"
)

REQUIRED_GATEWAY = "HDFC"

REQUIRED_RATE = "T0 - 1.78%"

# IMPORTANT:
# This is the fifth matching dropdown trigger,
# as in your original script.
# Verify this index against the actual transaction row.
# ROW_ACTION_INDEX = 4

SCREENSHOT_PATH = Path("bulk_transaction_error.png")


# ============================================================
# 2. VALIDATE TEST DATA
# ============================================================

if not EXCEL_FILE.is_file():
    raise FileNotFoundError(
        f"Excel file not found: {EXCEL_FILE}"
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

    Hdfc_window = None

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

        email_field.fill('newscenarictravelsllp@gmail.com')

        password_field = page.get_by_placeholder(
            "Enter your password"
        )

        password_field.fill('password2026')

        sign_in_button = page.get_by_text(
            "Sign In",
            exact=True
        )

        sign_in_button.click()

        print("Login button clicked")

        # Verify successful login

        bulk_list_indicator = page.get_by_text(
            "Bulk Transaction List",
            exact=True
        )

        expect(bulk_list_indicator).to_be_visible(
            timeout=30000
        )

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
        # STEP 4: CLICK CREATE BULK TRANSACTION
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
        # STEP 5: ORGANIZATION SELECTION
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

        print(
            "Organization selected:",
            ORGANIZATION
        )


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
        # STEP 7: EXCEL FILE UPLOAD
        # ====================================================

        file_to_upload = page.locator(
            "#file"
        )

        expect(file_to_upload).to_be_attached()

        file_to_upload.set_input_files(
            str(EXCEL_FILE)
        )

        # Verify uploaded filename

        uploaded_filename = file_to_upload.evaluate(
            "(element) => element.files[0]?.name"
        )

        assert uploaded_filename == EXCEL_FILE.name, (
            f"Excel upload failed. "
            f"Actual filename: {uploaded_filename}"
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

            print(
                "Payment Gateway dropdown opened"
            )

            hdfc_gateway_option = page.get_by_role(
                "option",
                name=REQUIRED_GATEWAY,
                exact=True
            )

            expect(
                hdfc_gateway_option
            ).to_be_visible()

            hdfc_gateway_option.click()

            print(
                "HDFC Payment Gateway selected"
            )

        else:

            print(
                "HDFC Gateway already selected"
            )


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

        print(
            "Rate selected:",
            REQUIRED_RATE
        )

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

        print(
            "Payment gateway and rate selection completed"
        )


        # ====================================================
        # STEP 12: GO BACK TO BULK TRANSACTION LIST
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

        print(
            "Successfully returned to Bulk Transaction List"
        )


        # ====================================================
        # STEP 13: OPEN SPECIFIC TRANSACTION THREE-DOT MENU
        # ====================================================

        # three_dot_buttons = page.locator(
        #     "button[data-slot='dropdown-menu-trigger']"
        # )
        #
        # expect(
        #     three_dot_buttons
        # ).to_have_count(
        #     ROW_ACTION_INDEX + 1
        # )
        #
        # three_dot = three_dot_buttons.nth(
        #     ROW_ACTION_INDEX
        # )
        #
        # expect(three_dot).to_be_visible()
        #
        # three_dot.click()

        three_dot = page.locator("//button[@data-slot='dropdown-menu-trigger']").nth(4)
        three_dot.click()


        print(
            "Bulk Transaction three-dot menu opened"
        )


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

        print(
            "Approve option selected"
        )


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

        print(
            "Bulk Transaction approval continued"
        )


        # ====================================================
        # STEP 16: OPEN THREE-DOT MENU AGAIN
        # ====================================================

        # three_dot_buttons = page.locator(
        #     "button[data-slot='dropdown-menu-trigger']"
        # )
        #
        # three_dot = three_dot_buttons.nth(
        #     ROW_ACTION_INDEX
        # )
        #
        # expect(three_dot).to_be_visible()
        #
        # three_dot.click()

        three_dot = page.locator("//button[@data-slot='dropdown-menu-trigger']").nth(4)
        three_dot.click()


        print(
            "Three-dot menu opened again"
        )


        # ====================================================
        # STEP 17: CLICK PAYMENT OPTION
        # ====================================================

        payment_option = page.get_by_text(
            "Payment",
            exact=True
        )

        expect(
            payment_option
        ).to_be_visible(
            timeout=30000
        )

        payment_option.click()

        print(
            "Payment option selected"
        )


        # ====================================================
        # STEP 18: CLICK PAY SECURELY NOW
        # AND CAPTURE HDFC POPUP
        # ====================================================

        pay_securely_now_button = page.get_by_role(
            "button",
            name="Pay Securely Now",
            exact=True
        )

        expect(
            pay_securely_now_button
        ).to_be_visible(
            timeout=30000
        )

        expect(
            pay_securely_now_button
        ).to_be_enabled()

        # Wait for the new HDFC window

        with page.expect_popup(
            timeout=30000
        ) as popup_info:

            pay_securely_now_button.click()

        print(
            "Pay Securely Now button clicked"
        )

        # Capture the new page

        Hdfc_window = popup_info.value

        print(
            "HDFC Payment Gateway window opened"
        )

        # Wait for HDFC page

        Hdfc_window.wait_for_load_state(
            "domcontentloaded",
            timeout=30000
        )

        print(
            "HDFC Payment URL:",
            Hdfc_window.url
        )

        print(
            "HDFC Payment Title:",
            Hdfc_window.title()
        )


        # ====================================================
        # STEP 19: SELECT HDFC BANK PAYMENT OPTION
        # ====================================================

        # hdfc_bank_option = Hdfc_window.locator(
        #     'div[configpath="PaymentPage.Expanded.NB.ListItem|topView|firstLine"]'
        # )
        #
        # expect(
        #     hdfc_bank_option
        # ).to_be_visible(
        #     timeout=30000
        # )
        #
        # hdfc_bank_option.click()
        #
        #print("Successfully selected HDFC bank payment option")



    #     # ====================================================
    #     # STEP 20: CLICK PROCEED TO PAY
    #     # ====================================================
    #
    #     proceed_to_pay_button = Hdfc_window.locator(
    #         "//article[normalize-space()='proceed to pay']"
    #     )
    #
    #     expect(
    #         proceed_to_pay_button
    #     ).to_be_visible(
    #         timeout=30000
    #     )
    #
    #     proceed_to_pay_button.click()
    #
    #     print(
    #         "Successfully clicked Proceed to Pay"
    #     )
    #
    #
    #     # ====================================================
    #     # STEP 21: OPEN TRANSACTION STATE DROPDOWN
    #     # ====================================================
    #
    #     select_transaction_state = Hdfc_window.locator(
    #         "//button[@id='txnStateDropdownToggle']"
    #     )
    #
    #     expect(
    #         select_transaction_state
    #     ).to_be_visible(
    #         timeout=30000
    #     )
    #
    #     select_transaction_state.click()
    #
    #     print(
    #         "Transaction state dropdown opened"
    #     )
    #
    #
    #     # ====================================================
    #     # STEP 22: SELECT CHARGED OPTION
    #     # ====================================================
    #
    #     charged_option = Hdfc_window.locator(
    #         "//span[normalize-space()='CHARGED']"
    #     )
    #
    #     expect(
    #         charged_option
    #     ).to_be_visible(
    #         timeout=30000
    #     )
    #
    #     charged_option.click()
    #
    #     print(
    #         "Successfully selected CHARGED option"
    #     )
    #
    #
    #     # ====================================================
    #     # STEP 23: CLICK SUBMIT BUTTON
    #     # ====================================================
    #
    #     submit_button = Hdfc_window.locator(
    #         "//button[@id='submitButton']"
    #     )
    #
    #     expect(
    #         submit_button
    #     ).to_be_visible(
    #         timeout=30000
    #     )
    #
    #     expect(
    #         submit_button
    #     ).to_be_enabled()
    #
    #     submit_button.click()
    #
    #     print(
    #         "Successfully clicked HDFC Submit button"
    #     )
    #
    #
    #     # ====================================================
    #     # STEP 24: PAYMENT RESPONSE VALIDATION
    #     # ====================================================
    #
    #     print(
    #         "HDFC payment submission completed"
    #     )
    #
    #     print(
    #         "HDFC current URL:",
    #         Hdfc_window.url
    #     )
    #
    #     # IMPORTANT:
    #     # Add the actual success/failure response locator
    #     # from your HDFC test gateway here.
    #     #
    #     # Do not assume that clicking Submit means payment
    #     # was successful.
    #
    #
    #     # ====================================================
    #     # STEP 25: FINAL EXECUTION REPORT
    #     # ====================================================
    #
    #     print("\n")
    #     print("=" * 55)
    #     print("BULK TRANSACTION AUTOMATION EXECUTION REPORT")
    #     print("=" * 55)
    #
    #     print("Application Login          : SUCCESS")
    #     print("Organization Selection     : SUCCESS")
    #     print("Excel Upload               : SUCCESS")
    #     print("Payment Gateway            : HDFC")
    #     print("Payment Gateway Rate       :", REQUIRED_RATE)
    #     print("Bulk Transaction Approval  : SUBMITTED")
    #     print("Payment Option             : SELECTED")
    #     print("HDFC Payment Window        : OPENED")
    #     print("HDFC Bank Option           : SELECTED")
    #     print("Proceed to Pay             : CLICKED")
    #     print("Transaction State          : CHARGED")
    #     print("HDFC Submit                : CLICKED")
    #
    #     print("=" * 55)
    #
    #     print(
    #         "Automation reached the final payment submission step."
    #     )
    #
    #     # Keep browser open for manual inspection
    #
    #     page.pause()
    #
    #
    # # ========================================================
    # # 4. EXCEPTION HANDLING
    # # ========================================================
    #
    # except FileNotFoundError as error:
    #
    #     print(
    #         "FILE ERROR:",
    #         error
    #     )
    #
    #
    # except PlaywrightTimeoutError as error:
    #
    #     print(
    #         "\nPLAYWRIGHT TIMEOUT ERROR:"
    #     )
    #
    #     print(error)
    #
    #     try:
    #
    #         if Hdfc_window and not Hdfc_window.is_closed():
    #
    #             Hdfc_window.screenshot(
    #                 path="hdfc_payment_error.png",
    #                 full_page=True
    #             )
    #
    #             print(
    #                 "HDFC error screenshot saved"
    #             )
    #
    #         page.screenshot(
    #             path=str(SCREENSHOT_PATH),
    #             full_page=True
    #         )
    #
    #         print(
    #             "Invorush error screenshot saved"
    #         )
    #
    #     except Exception as screenshot_error:
    #
    #         print(
    #             "Screenshot error:",
    #             screenshot_error
    #         )
    #
    #
    # except Exception as error:
    #
    #     print(
    #         "\nUNEXPECTED ERROR:"
    #     )
    #
    #     print(error)
    #
    #     try:
    #
    #         if Hdfc_window and not Hdfc_window.is_closed():
    #
    #             Hdfc_window.screenshot(
    #                 path="hdfc_payment_error.png",
    #                 full_page=True
    #             )
    #
    #         page.screenshot(
    #             path=str(SCREENSHOT_PATH),
    #             full_page=True
    #         )
    #
    #         print(
    #             "Error screenshots saved"
    #         )
    #
    #     except Exception as screenshot_error:
    #
    #         print(
    #             "Screenshot error:",
    #             screenshot_error
    #         )
    #
    #
    # finally:
    #
    #     browser.close()
    #
    #     print(
    #         "\nBrowser closed"
    #     )

    # ============================================================
    # HDFC WINDOW REFERENCE
    # ============================================================

    hdfc_page = Hdfc_window

    # ============================================================
    # CLICK "ADD CREDIT/DEBIT CARDS"
    # ============================================================

    Add_credit_card = hdfc_page.get_by_text(
        "Add Credit/Debit Cards",
        exact=True
    )

    Add_credit_card.wait_for(
        state="visible",
        timeout=30000
    )

    Add_credit_card.click()

    print("✓ Add Credit/Debit Cards clicked")

    # ============================================================
    # ENTER CARD NUMBER
    # ============================================================

    card_number = hdfc_page.get_by_placeholder(
        'Enter Card Number'
    )

    card_number.wait_for(
        state="visible",
        timeout=30000
    )

    card_number.fill(
        "4012 0000 0000 1097"
    )

    print("✓ Card number entered")

    # ============================================================
    # ENTER EXPIRY DATE
    # ============================================================

    expiry_date = hdfc_page.get_by_placeholder(
        "MM/YY"
    )

    expiry_date.wait_for(
        state="visible",
        timeout=30000
    )

    expiry_date.fill(
        "09/32"
    )

    print("✓ Expiry date entered")

    # ============================================================
    # ENTER CVV
    # ============================================================

    cvv_number = hdfc_page.get_by_placeholder(
        'Enter CVV'
    )

    cvv_number.wait_for(
        state="visible",
        timeout=30000
    )

    cvv_number.fill(
        "123"
    )

    print("✓ CVV entered")

    # ============================================================
    # FILL NAME ON THE CARD
    # ============================================================

    Name_of_Card = hdfc_page.get_by_placeholder(
        "Enter your name on card"
    )

    Name_of_Card.wait_for(
        state="visible",
        timeout=30000
    )

    Name_of_Card.fill('aaaaa')

    print("✓ Name on card entered")

    # ============================================================
    # CLICK "PROCEED TO PAY"
    # ============================================================

    Proceed_to_pay_button = hdfc_page.locator(
        "//article[contains(normalize-space(.), 'proceed to pay')]"
    )

    Proceed_to_pay_button.wait_for(
        state="visible",
        timeout=30000
    )

    Proceed_to_pay_button.click()

    print("✓ Proceed to Pay clicked")

    # ============================================================
    # CLICK "SECURE & PAY"
    # ============================================================

    Secure_and_pay_button = hdfc_page.locator(
        "//article[text()='Secure & Pay']"
    )

    Secure_and_pay_button.wait_for(
        state="visible",
        timeout=30000
    )

    Secure_and_pay_button.click()

    print("✓ Secure & Pay clicked")

    # ============================================================
    # CLICK "CLICK TO PROCEED"
    # ============================================================

    Click_to_Proceed_button = hdfc_page.locator(
        "//article[normalize-space()='Click to proceed']"
    )

    Click_to_Proceed_button.wait_for(
        state="visible",
        timeout=30000
    )

    print("✓ Click to proceed button found")

    # ============================================================
    # CAPTURE THE NEW WINDOW
    # ============================================================

    with hdfc_page.expect_popup(
            timeout=30000
    ) as popup_info_2:

        Click_to_Proceed_button.click()

    print("✓ Click to proceed clicked")

    # ============================================================
    # GET THE NEW WINDOW
    # ============================================================

    new_page = popup_info_2.value

    print("✓ New window opened")

    new_page.wait_for_load_state(
        "domcontentloaded",
        timeout=30000
    )

    print("New Window URL:", new_page.url)
    print("New Window Title:", new_page.title())

    # ============================================================
    # WORK INSIDE THE NEW WINDOW
    # ============================================================

    # CLICK TRANSACTION STATE DROPDOWN

    select_transaction_state = new_page.locator(
        "//div[@id='txnStateDropdownText']"
    )

    select_transaction_state.wait_for(
        state="visible",
        timeout=30000
    )

    select_transaction_state.click()

    print("✓ Transaction state dropdown opened")

    # ============================================================
    # SELECT CHARGED OPTION
    # ============================================================

    option_selection = new_page.locator(
        "//li[@class='dropdown-item' and @data-value='CHARGED']"
    )

    option_selection.wait_for(
        state="visible",
        timeout=30000
    )

    option_selection.click()

    print("✓ CHARGED option selected")

    # ============================================================
    # CLICK SUBMIT BUTTON
    # ============================================================

    Submit_button_click = new_page.locator(
        "//button[@id='submitButton']"
    )

    Submit_button_click.wait_for(
        state="visible",
        timeout=30000
    )

    Submit_button_click.click()

    print("✓ Submit button clicked")

    # ============================================================
    # WAIT FOR PAYMENT PROCESSING
    # ============================================================

    time.sleep(5)

    print("HDFC payment submission step completed")
