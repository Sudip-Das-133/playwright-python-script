
import time
from datetime import datetime

from playwright.sync_api import sync_playwright, expect


# ============================================================
# MANUAL FALLBACK DATA
# ============================================================

MANUAL_DATA = {
    "invoice_number": "13856",
    "invoice_issue_date": "June 13, 2026",
    "invoice_due_date": "September 13, 2026",
    "invoice_amount": "2631.48"
}


# ============================================================
# INPUT FIELD HANDLER
# ============================================================

def fill_input_if_empty(locator, field_name, fallback_value):

    current_value = locator.input_value().strip()

    if current_value:
        print(f"✓ {field_name} → OCR value found: {current_value}")
    else:
        print(f"⚠ {field_name} → OCR value NOT found")
        print(f"→ Filling manually: {fallback_value}")

        locator.fill(fallback_value)


# ============================================================
# DATE FIELD HANDLER
# ============================================================

def fill_date_if_empty(locator, field_name, fallback_value):

    current_value = locator.inner_text().strip()

    if current_value and current_value != "Pick a date":

        print(f"✓ {field_name} → OCR value found: {current_value}")
        return

    print(f"⚠ {field_name} → OCR value NOT found")
    print(f"→ Selecting manually: {fallback_value}")

    target_date = datetime.strptime(
        fallback_value,
        "%B %d, %Y"
    )

    day = str(target_date.day)
    month = target_date.strftime("%B")
    year = str(target_date.year)

    # Open date picker
    locator.click()

    page = locator.page

    # --------------------------------------------------------
    # Try to select month/year if calendar has visible selectors
    # --------------------------------------------------------

    month_year_text = page.get_by_text(
        f"{month} {year}",
        exact=True
    )

    if not month_year_text.is_visible():

        # Try next-month button until target month/year appears
        for _ in range(24):

            if page.get_by_text(
                f"{month} {year}",
                exact=True
            ).is_visible():

                break

            next_month = page.locator(
                "button[aria-label*='next month' i], "
                "button[aria-label*='Next Month' i], "
                "button[aria-label*='next' i]"
            ).first

            if next_month.is_visible():
                next_month.click()
                page.wait_for_timeout(200)
            else:
                break

    # --------------------------------------------------------
    # Select target day
    # --------------------------------------------------------

    day_locator = page.get_by_role(
        "gridcell",
        name=day,
        exact=True
    )

    if day_locator.count() > 0:

        for i in range(day_locator.count()):

            candidate = day_locator.nth(i)

            if candidate.is_visible():
                candidate.click()
                return

    # Alternative date-picker selectors
    day_locator = page.locator(
        "[data-day]"
    ).filter(
        has_text=day
    ).first

    if day_locator.is_visible():
        day_locator.click()
        return

    raise Exception(
        f"Could not select {fallback_value} "
        f"for {field_name}"
    )


# ============================================================
# PLAYWRIGHT
# ============================================================

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    # ========================================================
    # 1. OPEN APPLICATION
    # ========================================================

    page.goto(
        "https://org.dev.invorush.com/",
        wait_until="domcontentloaded"
    )

    print("✓ Application opened")


    # ========================================================
    # 2. LOGIN
    # ========================================================

    page.locator(
        "//input[@name='email']"
    ).fill(
        "sapphiro.consulting@gmail.com"
    )

    page.locator(
        "//input[@placeholder='Enter your password']"
    ).fill(
        "password2026"
    )

    page.locator(
        "//span[normalize-space()='Sign In']"
    ).click()

    page.wait_for_timeout(5000)

    print("✓ Login completed")


    # ========================================================
    # 3. GO TO INVOICE LIST
    # ========================================================

    invoice_list = page.locator(
        "//span[normalize-space()='Invoice List']"
    )

    invoice_list.wait_for(
        state="visible",
        timeout=30000
    )

    invoice_list.scroll_into_view_if_needed()
    invoice_list.click()

    page.wait_for_timeout(3000)

    print("✓ Invoice List opened")


    # ========================================================
    # 4. CREATE INVOICE
    # ========================================================

    create_invoice_button = page.locator(
        "//a[normalize-space()='Create Invoice']"
    )

    create_invoice_button.wait_for(
        state="visible",
        timeout=30000
    )

    create_invoice_button.click()

    page.wait_for_timeout(3000)

    print("✓ Create Invoice clicked")


    # ========================================================
    # 5. PROCEED
    # ========================================================

    proceed_button = page.locator(
        "//span[normalize-space()='Proceed']"
    )

    proceed_button.wait_for(
        state="visible",
        timeout=30000
    )

    proceed_button.click()

    page.wait_for_timeout(3000)

    print("✓ Proceed clicked")


    # ========================================================
    # 6. SELECT ORGANIZATION
    # ========================================================

    org_selection = page.locator(
        "//button[normalize-space()='Search organization']"
    )

    org_selection.wait_for(
        state="visible",
        timeout=30000
    )

    org_selection.click()

    org = page.locator(
        "//div[@data-value='NEW SCENARIC TRAVELS LLP']"
    )

    org.wait_for(
        state="visible",
        timeout=30000
    )

    org.click()

    page.wait_for_timeout(3000)

    print("✓ Organization selected")


    # ========================================================
    # 7. NEXT → UPLOAD INVOICE PAGE
    # ========================================================

    next_button = page.locator(
        "//span[normalize-space()='Next']"
    )

    next_button.wait_for(
        state="visible",
        timeout=30000
    )

    next_button.click()

    page.wait_for_timeout(3000)

    print("✓ Moved to Upload Invoice page")


    # ========================================================
    # 8. UPLOAD PDF
    # ========================================================

    print("\n========================================")
    print("UPLOADING INVOICE PDF")
    print("========================================")

    invoice_browse = page.locator(
        "//input[@id='file']"
    )

    invoice_browse.wait_for(
        state="attached",
        timeout=30000
    )

    invoice_browse.set_input_files(
        r"C:\Users\Lenovo\Downloads\1000+ PDF_Invoice_Folder (1)\1000+ PDF_Invoice_Folder\invoice_Troy Staebel_30585.pdf"
    )

    print("✓ PDF uploaded")

    page.wait_for_timeout(3000)


    # ========================================================
    # 9. SUBMIT PDF / START OCR
    # ========================================================

    upload_button = page.locator(
        "//button[@type='submit']"
    )

    expect(upload_button).to_be_enabled(
        timeout=10000
    )

    upload_button.click()

    print("✓ PDF submitted")
    print("Waiting for OCR processing...")


    # ========================================================
    # 10. WAIT FOR INVOICE FORM
    # ========================================================

    page.get_by_text(
        "Invoice Form",
        exact=True
    ).wait_for(
        state="visible",
        timeout=30000
    )

    print("✓ Invoice Form loaded")

    page.wait_for_timeout(3000)


    # ========================================================
    # 11. DEFINE INVOICE FIELDS
    # ========================================================

    invoice_fields = {

        "invoice_number": {

            "name": "Invoice Number",

            "type": "input",

            "locator": page.locator(
                "//input[@name='invoiceNumber']"
            ),

            "fallback": MANUAL_DATA[
                "invoice_number"
            ]
        },


        "invoice_issue_date": {

            "name": "Invoice Issue Date",

            "type": "date",

            "locator": page.locator(
                "xpath=//label[contains(normalize-space(), 'Invoice Issue Date')]/following-sibling::button"
            ),

            "fallback": MANUAL_DATA[
                "invoice_issue_date"
            ]
        },


        "invoice_due_date": {

            "name": "Invoice Due Date",

            "type": "date",

            "locator": page.locator(
                "xpath=//label[contains(normalize-space(), 'Invoice Due Date')]/following-sibling::button"
            ),

            "fallback": MANUAL_DATA[
                "invoice_due_date"
            ]
        },


        "invoice_amount": {

            "name": "Invoice Amount",

            "type": "input",

            "locator": page.locator(
                "//input[@aria-label='Invoice Amount']"
            ),

            "fallback": MANUAL_DATA[
                "invoice_amount"
            ]
        }
    }


    # ========================================================
    # 12. OCR VALIDATION
    # ========================================================

    print("\n========================================")
    print("OCR FIELD VALIDATION")
    print("========================================")


    for field in invoice_fields.values():

        locator = field["locator"]

        field_name = field["name"]

        fallback_value = field["fallback"]

        field_type = field["type"]

        locator.wait_for(
            state="visible",
            timeout=30000
        )

        if field_type == "date":

            fill_date_if_empty(
                locator=locator,
                field_name=field_name,
                fallback_value=fallback_value
            )

        else:

            fill_input_if_empty(
                locator=locator,
                field_name=field_name,
                fallback_value=fallback_value
            )


    # ========================================================
    # 13. FINAL VALIDATION
    # ========================================================

    print("\n========================================")
    print("FINAL INVOICE VALIDATION")
    print("========================================")

    missing_fields = []


    for field in invoice_fields.values():

        locator = field["locator"]

        field_name = field["name"]

        field_type = field["type"]


        if field_type == "date":

            final_value = locator.inner_text().strip()

            if (
                final_value
                and final_value != "Pick a date"
            ):

                print(
                    f"✓ {field_name}: "
                    f"{final_value}"
                )

            else:

                print(
                    f"❌ {field_name}: EMPTY"
                )

                missing_fields.append(
                    field_name
                )


        else:

            final_value = (
                locator.input_value().strip()
            )

            if final_value:

                print(
                    f"✓ {field_name}: "
                    f"{final_value}"
                )

            else:

                print(
                    f"❌ {field_name}: EMPTY"
                )

                missing_fields.append(
                    field_name
                )


    # ========================================================
    # 14. FAIL IF MANDATORY FIELD IS EMPTY
    # ========================================================

    if missing_fields:

        raise AssertionError(
            "The following mandatory invoice fields "
            "are empty: "
            + ", ".join(missing_fields)
        )


    print(
        "\n✓ All 4 mandatory invoice fields "
        "are populated successfully."
    )


    # ========================================================
    # 15. CLICK NEXT ON INVOICE FORM
    # ========================================================

    invoice_form_next = page.get_by_role(
        "button",
        name="Next",
        exact=True
    )

    expect(
        invoice_form_next
    ).to_be_enabled(
        timeout=10000
    )

    invoice_form_next.click()

    print(
        "✓ Invoice Form submitted successfully"
    )


    # ========================================================
    # 16. VERIFY CHECKERS CONFIG
    # ========================================================

    page.get_by_text(
        "Checkers Config",
        exact=True
    ).wait_for(
        state="visible",
        timeout=15000
    )

    print(
        "✓ Successfully moved to Checkers Config"
    )


    # ========================================================
    # 17. COMPLETED
    # ========================================================

    print("\n========================================")
    print("INVOICE OCR FLOW COMPLETED")
    print("========================================")

    #  ==========================================================================================

    print("\n========================================")
    print("Select checker in Checker configure  Page :")
    print("========================================")



    Select_checker_config = page.locator("//span[text()='(No checker verification required.)']")
    Select_checker_config.click()
    time.sleep(3)

    print("Sucessfully checker configuration selected ")

    ## click on  the 'Next' button in the Checker configuration page :

    click_next_button = page.locator("//button[text()='Next']")
    click_next_button.click()
    time.sleep(3)




    browser.close()