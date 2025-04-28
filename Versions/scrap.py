from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

search_url = "https://www.brookings.edu/?s=racial%20bias"
driver.get(search_url)
time.sleep(3)

# Scroll to load more Algolia hits
for _ in range(8):  # scroll more times if needed
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Get all article links from Algolia-powered search
article_elements = driver.find_elements(By.CSS_SELECTOR, "#algolia-hits article a")
article_urls = [a.get_attribute("href") for a in article_elements]

print(f"🔗 Found {len(article_urls)} article links.")
for url in article_urls:
    print(url)

driver.quit()