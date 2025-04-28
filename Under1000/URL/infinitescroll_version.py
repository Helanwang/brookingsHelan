import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # see browser if needed
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Define search keyword and URL
keyword = "racism"
search_url = f"https://www.brookings.edu/?s={keyword.replace(' ', '%20')}"
driver.get(search_url)
time.sleep(5)

# Repeatedly click the "Show More" button
seen_urls = set()
print("📡 Loading search results by clicking 'Show More'...")

while True:
    # Grab all article links so far
    links = driver.find_elements(By.CSS_SELECTOR, "#algolia-hits article a")
    for link in links:
        href = link.get_attribute("href")
        if href:
            seen_urls.add(href)

    try:
        show_more_btn = driver.find_element(By.CSS_SELECTOR, "button.ais-InfiniteHits-loadMore")
        if not show_more_btn.is_enabled():
            print("🛑 'Show More' button is disabled — no more results.")
            break

        print(f"🔘 Clicking 'Show More'... total articles so far: {len(seen_urls)}")
        driver.execute_script("arguments[0].click();", show_more_btn)
        time.sleep(3)

    except Exception as e:
        print("❌ 'Show More' button not found. Ending scroll.")
        break

print(f"✅ Finished loading. Total unique articles: {len(seen_urls)}")

# Save to CSV
filename = f"brookings_{keyword.replace(' ', '_')}_urls.csv"
with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Keyword", "Article URL"])
    for url in seen_urls:
        writer.writerow([keyword, url])

driver.quit()
print(f"✅ All article URLs saved to: {filename}")