
import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Keywords with under 1000 results
under_1000 = {
    'race prejudice': 85,
    'racial prejudice': 39,
    'race discrimination': 847,
    'racial discrimination': 518,
    'racial disparity': 705,
    'racial inequality': 730,
    'racial difference': 985,
    'racism': 981
}

# Setup Chrome
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")  # Uncomment if you want to run headless
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_keyword(keyword):
    search_url = f"https://www.brookings.edu/?s={keyword.replace(' ', '%20')}"
    driver.get(search_url)
    time.sleep(5)

    seen_urls = set()
    print(f"\n📡 Scraping for: {keyword}")

    while True:
        links = driver.find_elements(By.CSS_SELECTOR, "#algolia-hits article a")
        for link in links:
            href = link.get_attribute("href")
            if href:
                seen_urls.add(href)

        if len(seen_urls) >= 1000:
            print("🛑 Reached Algolia 1000-article limit.")
            break

        try:
            show_more_btn = driver.find_element(By.CSS_SELECTOR, "button.ais-InfiniteHits-loadMore")
            if not show_more_btn.is_enabled():
                print("🛑 'Show More' is disabled. Done.")
                break

            print(f"🔘 Clicking 'Show More'... total: {len(seen_urls)}")
            driver.execute_script("arguments[0].click();", show_more_btn)
            time.sleep(random.uniform(2, 4))

        except Exception as e:
            print(f"❌ Error or no more button: {e}")
            break

    filename = f"brookings_{keyword.replace(' ', '_')}_urls.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Keyword", "Article URL"])
        for url in seen_urls:
            writer.writerow([keyword, url])

    print(f"✅ Saved {len(seen_urls)} articles for '{keyword}' to {filename}")

# Run scraper for each keyword
for kw in under_1000.keys():
    scrape_keyword(kw)

driver.quit()
print("\n✅ All scraping done.")