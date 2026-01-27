#!/usr/bin/env python3
"""
Open https://www.syzygyai.in/ in Chrome using Selenium and optionally click the
"Research" link.

Usage:
    python scripts/open_syzygy_chrome.py [--headless] [--url URL] [--click-research]

This script uses `webdriver-manager` to automatically download a matching ChromeDriver.
"""
import argparse
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find_and_click_research(driver, timeout=10, screenshot=None):
    """Try several XPath strategies to find the Research link and click it.

    Returns the element text and the XPath used on success, otherwise raises Exception.
    """
    xpaths = [
        "//a[normalize-space(.)='Research']",
        "//button[normalize-space(.)='Research']",
        "//*[normalize-space(text())='Research']",
        "//a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'research')]",
        "//a[contains(@href,'research')]"
    ]

    # Use WebDriverWait to find any of these
    wait = WebDriverWait(driver, timeout)
    for xp in xpaths:
        try:
            elem = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
            elem.click()
            # optional screenshot after click
            if screenshot:
                time.sleep(1)
                driver.save_screenshot(screenshot)
            return elem.text, xp
        except Exception:
            # try next xpath
            continue
    # If none matched, raise
    raise Exception('Unable to find a clickable "Research" element using candidate XPaths')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='https://www.syzygyai.in/')
    parser.add_argument('--headless', action='store_true', help='Run Chrome in headless mode')
    parser.add_argument('--click-research', action='store_true', help='Locate and click the Research link after opening')
    parser.add_argument('--wait', type=int, default=10, help='Timeout in seconds to wait for elements')
    parser.add_argument('--screenshot', type=str, default=None, help='Optional path to save a screenshot after clicking')
    args = parser.parse_args()

    options = Options()
    if args.headless:
        # Use the new headless mode flag when supported
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Install ChromeDriver automatically and start the browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(args.url)

    try:
        if args.click_research:
            try:
                text, used_xpath = find_and_click_research(driver, timeout=args.wait, screenshot=args.screenshot)
                print(f'Clicked element with text: "{text}" using XPath: {used_xpath}')
            except Exception as e:
                print('Error locating/clicking Research element:', e)
        # If running headless and not taking a screenshot, wait briefly then exit
        if args.headless:
            time.sleep(2)
        else:
            try:
                input('Press Enter to close the browser and exit...')
            except KeyboardInterrupt:
                pass
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
