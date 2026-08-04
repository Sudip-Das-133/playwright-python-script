import time

from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://org.dev.invorush.com/")
    time.sleep(10)
    ## Locate email id text field and fill the data :
   # page.get_by_placeholder("Enter your email").fill("newscenarictravelsllp@gmail.com")
    page.locator("//input[@name ='email']").fill("newscenarictravelsllp@gmail.com")

    time.sleep(10)

    ## Locate password textfield and fill the data :

    #page.get_by_placeholder("Enter your password").fill("password2026")
    page.locator("//input[@placeholder='Enter your password']").fill("password2026")
    time.sleep(5)

    # locate the click button and click on 'sign in ' button :

    page.locator("//span[text()='Sign In']").click()
    time.sleep(10)
    browser.close()