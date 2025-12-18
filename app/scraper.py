from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time, json

URL = "https://www.shl.com/solutions/products/product-catalog/"

def scrape_shl():
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 20)
    driver.get(URL)

    # Accept cookies
    try:
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Allow all cookies')]")
            )
        ).click()
        time.sleep(3)
    except:
        pass

    results = {}

    # 🔹 Find all filter checkboxes
    filters = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    print(f"Found {len(filters)} filters")

    for i, f in enumerate(filters):
        try:
            driver.execute_script("arguments[0].click();", f)
            time.sleep(2)
        except:
            continue

        print(f"\nApplying filter {i+1}")

        last_count = 0
        for _ in range(10):
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(3)

            anchors = driver.find_elements(By.XPATH, "//a[@href]")
            for a in anchors:
                href = a.get_attribute("href")
                if not href:
                    continue
                if "/products/" not in href:
                    continue
                if "job" in href.lower():
                    continue

                results[href] = {
                    "name": href.split("/")[-1].replace("-", " ").title(),
                    "url": href,
                    "description": "",
                    "test_type": ""
                }

            if len(results) == last_count:
                break
            last_count = len(results)

        # Uncheck filter
        try:
            driver.execute_script("arguments[0].click();", f)
            time.sleep(2)
        except:
            pass

        print(f"Total collected so far: {len(results)}")

    driver.quit()

    final = list(results.values())
    print(f"\nFINAL COUNT: {len(final)} assessments")

    with open("data/shl_raw.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2)

if __name__ == "__main__":
    scrape_shl()
