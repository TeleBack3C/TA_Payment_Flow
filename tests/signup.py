import os

from playwright.sync_api import sync_playwright, expect

from TA_Payment_Flow.tests.common_functions import unique_credentials, display_initial_page

def enter_cc_details(page):
    # Enter full name on card
    page.get_by_placeholder(" ", exact=True).fill("John Doe")
    page.locator("iframe[name=\"__privateStripeFrame6364\"]").content_frame().get_by_label(
        "Credit or debit card number").fill("4242 4242 4242 4242")
    page.locator("iframe[name=\"__privateStripeFrame6366\"]").content_frame().get_by_label("ZIP").fill("12345")
    page.locator("iframe[name=\"__privateStripeFrame6365\"]").content_frame().get_by_label("Credit or debit card").fill(
        "11 / 33")
    page.locator("iframe[name=\"__privateStripeFrame6363\"]").content_frame().get_by_label(
        "Credit or debit card CVC/CVV").fill("123")


def manager_signup(pw1) -> None:
    # Convert the returned string to a boolean
    headless_mode = os.getenv("HEADLESS_MODE", "false").strip().lower() == "true"
    # test it in all 3 browsers
    browser_types = ['chromium', 'firefox', 'webkit']
    for browser_type in browser_types:
        email, fullname, userpass = unique_credentials()
        page, browser, context, stage_manager_url = display_initial_page(pw, browser_type, headless_mode, 'ta_reg', 500)
        page.get_by_role("textbox").fill(email)
        page.locator("button").filter(has_text="Continue with email").click()
        page.locator("#app input[name=\"full_name\"]").fill(fullname)
        page.locator("input[name=\"password\"]").fill(userpass)
        page.locator("input[name=\"confirm_password\"]").fill(userpass)
        # Click the Continue button
        page.get_by_label("tc-button").click()
        # from this point, we test the Payment Details modal
        # Verify the modal is displayed
        try:
            expect(page.get_by_role("dialog")).to_contain_text("To activate your 7 day FREE trial")
        except AssertionError as e:
            print(f"An unexpected error occurred: {e}")
        # Enter cc Details
        enter_cc_details(page)






with sync_playwright() as pw:
    manager_signup(pw)