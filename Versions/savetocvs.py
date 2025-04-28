import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Keyword to search
keyword = "racial bias"
search_url = f"https://www.brookings.edu/?s={keyword.replace(' ', '%20')}"
driver.get(search_url)
time.sleep(3)

# Scroll to load more results
for _ in range(8):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Extract article URLs
article_elements = driver.find_elements(By.CSS_SELECTOR, "#algolia-hits article a")
article_urls = [a.get_attribute("href") for a in article_elements if a.get_attribute("href")]

# Save to CSV
csv_filename = "brookings_racial_bias_articles.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Keyword", "Article URL"])
    for url in article_urls:
        writer.writerow([keyword, url])

driver.quit()
print(f"✅ Saved {len(article_urls)} articles to {csv_filename}")