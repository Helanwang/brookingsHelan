from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# === Setup WebDriver ===
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# === URL to scrape ===
url = "https://www.brookings.edu/articles/do-americans-really-want-a-policy-revolution/"
driver.get(url)

# === Wait until at least one <p> tag inside #content loads ===
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#content p"))
)

# === Extract the title ===
try:
    title = driver.find_element(By.TAG_NAME, "h1").text
except Exception as e:
    title = "N/A"
    print(f"❌ Could not extract title: {e}")

# === Extract clean article content ===
try:
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "#content p")

    content = []
    stop_words = ["RELATED CONTENT", "RELATED BOOKS", "AUTHORS", "The Brookings Institution"]

    for p in paragraphs:
        text = p.text.strip()

        # Stop if we reach footer or unrelated content
        if any(stop_word in text for stop_word in stop_words):
            break

        # Skip if paragraph has too few words (junk tags or very short labels)
        if len(text.split()) < 15:
            continue

        content.append(text)

    content = "\n\n".join(content)

except Exception as e:
    content = "N/A"
    print(f"❌ Could not extract content: {e}")

# === Close browser ===
driver.quit()

# === Output ===
print(f"Title:\n{title}\n")
print("Article Content:\n")
print(content)