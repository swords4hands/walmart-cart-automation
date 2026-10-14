# Walmart Cart Automation Bot (Selenium RPA)

A browser automation bot built with **Selenium WebDriver** and Python that automates the product carting workflow on Walmart.com with session state persistence.

---

## ✨ Features

- **Persistent Session & Cookies**: Utilizes a persistent Firefox browser profile (`~/.mozilla/firefox/walmart-selenium-profile`), keeping your session authenticated across executions without storing cleartext passwords.
- **Intelligent Authentication Detection**: Inspects the live DOM for login anchors and prompts the user only if the current session has expired.
- **Modal & Promo Dismissal**: Automatically detects and dismisses location, promotional, or notification modals before interacting with cart buttons.
- **Explicit Webdriver Waits**: Implements resilient `WebDriverWait` polling to handle dynamic single-page application (SPA) state changes.

---

## 🛠️ Setup

### Prerequisites
- Python 3.10+
- Firefox browser & [GeckoDriver](https://github.com/mozilla/geckodriver/releases)

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run with Default Essential Item
```bash
python3 add_to_walmart_cart.py
```

### Run with a Specific Product URL
```bash
python3 add_to_walmart_cart.py --url "https://www.walmart.com/ip/Your-Product-URL/12345678"
```

---

## 📄 License

MIT
