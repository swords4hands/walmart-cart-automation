#!/usr/bin/env python3
"""
Walmart Quick Cart Automation Bot — Robotic Process Automation with Selenium & Persistent Profiles.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from colorama import Fore, Style, init

DEFAULT_PRODUCT_URL = (
    "https://www.walmart.com/ip/Great-Value-Disinfecting-Wipes-4-Pack-300-Total-Wipes/423259576"
)


def print_section(message: str, *, color: str = Fore.CYAN) -> None:
    line = "─" * len(message)
    print(color + line + Style.RESET_ALL)
    print(color + message + Style.RESET_ALL)
    print(color + line + Style.RESET_ALL)


def is_logged_in(driver: webdriver.Firefox) -> bool:
    """Heuristic check: detect presence of prominent login UI elements."""
    try:
        sign_in_candidates = driver.find_elements(
            By.XPATH,
            "//a[contains(., 'Sign in') or contains(., 'Sign In')] | "
            "//button[contains(., 'Sign in') or contains(., 'Sign In')]",
        )
        return len(sign_in_candidates) == 0
    except Exception:
        return False


def close_possible_modal(wait: WebDriverWait) -> None:
    """Closes introductory/promotional popups or modals if present."""
    try:
        modal_close = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@aria-label, 'Close') or contains(., 'Not now') or "
                    "contains(., 'Cancel') or contains(., 'Continue')]",
                )
            )
        )
        modal_close.click()
        time.sleep(0.5)
    except Exception:
        pass


def run_bot(driver_factory: Callable[[], webdriver.Firefox], product_url: str) -> None:
    init(autoreset=True)

    driver = driver_factory()
    try:
        wait = WebDriverWait(driver, 25)

        print_section("Opening product page", color=Fore.GREEN)
        driver.get(product_url)
        close_possible_modal(wait)

        if not is_logged_in(driver):
            print_section("Not logged in (profile has no active session)", color=Fore.YELLOW)
            print(Fore.YELLOW + "Please sign in normally in the opened Firefox window." + Style.RESET_ALL)
            driver.get("https://www.walmart.com/account/login")
            input(Fore.YELLOW + "After you have successfully logged in, press Enter to continue…" + Style.RESET_ALL)

            print_section("Returning to product page", color=Fore.GREEN)
            driver.get(product_url)
            close_possible_modal(wait)

        print_section("Attempting to add the item to your cart", color=Fore.GREEN)
        add_to_cart_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(., 'Add to cart')] or contains(., 'Add to cart')]")
            )
        )
        add_to_cart_button.click()

        print_section("Opening cart page for verification", color=Fore.GREEN)
        driver.get("https://www.walmart.com/cart")

        print(Fore.YELLOW + "Item added successfully. Check the cart in the browser window." + Style.RESET_ALL)
        input(Fore.YELLOW + "Press Enter to finish and close the browser. " + Style.RESET_ALL)

    finally:
        driver.quit()


def main():
    parser = argparse.ArgumentParser(description="Automate adding items to Walmart cart using Selenium RPA")
    parser.add_argument(
        "--url",
        default=DEFAULT_PRODUCT_URL,
        help="Walmart product page URL to add to cart",
    )
    args = parser.parse_args()

    def create_driver() -> webdriver.Firefox:
        profile_dir = Path.home() / ".mozilla" / "firefox" / "walmart-selenium-profile"
        profile_dir.mkdir(parents=True, exist_ok=True)

        options = FirefoxOptions()
        options.add_argument("-profile")
        options.add_argument(str(profile_dir))
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("permissions.default.desktop-notification", 2)

        service = FirefoxService()
        return webdriver.Firefox(service=service, options=options)

    try:
        run_bot(create_driver, args.url)
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting…")


if __name__ == "__main__":
    main()
