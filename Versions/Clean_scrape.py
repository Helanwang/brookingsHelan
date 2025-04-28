import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium WebDriver in headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Target URL
url = "https://www.brookings.edu/articles/why-the-world-anti-doping-agency-should-revisit-its-cannabis-ban-2/"
driver.get(url)
time.sleep(5)  # Wait for content to fully load

# === Extract Title ===
try:
    title = driver.find_element(
        By.CSS_SELECTOR,
        "#hero > div.tm-article-research.tm-container.no-takeaways.tm-article-commentary > div.grid-4-8.wrapper > div > div.left-col.md\\:col-span-6.lg\\:col-span-5.xl\\:col-span-4 > div > div:nth-child(1) > h1"
    ).text
except Exception as e:
    title = "N/A"
    print(f"❌ Could not extract title: {e}")

# === Extract Date ===
try:
    date = driver.find_element(
        By.CSS_SELECTOR,
        "#hero > div.tm-article-research.tm-container.no-takeaways.tm-article-commentary > div.grid-4-8.wrapper > div > div.left-col.md\\:col-span-6.lg\\:col-span-5.xl\\:col-span-4 > div > div.article-meta > div > p"
    ).text
except Exception as e:
    date = "N/A"
    print(f"❌ Could not extract date: {e}")

# === Extract Author ===
try:
    author = driver.find_element(
        By.CSS_SELECTOR,
        "#hero > div.tm-article-research.tm-container.no-takeaways.tm-article-commentary > div.grid-4-8.wrapper > div > div.left-col.md\\:col-span-6.lg\\:col-span-5.xl\\:col-span-4 > div > div.article-meta > h5 > div"
    ).text
except Exception as e:
    author = "N/A"
    print(f"❌ Could not extract author: {e}")

# === Extract Article Content ===
try:
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "#content p")

    content = []
    stop_words = ["RELATED CONTENT", "RELATED BOOKS", "AUTHORS", "The Brookings Institution"]

    for p in paragraphs:
        text = p.text.strip()

        # Stop if footer/disclaimer content appears
        if any(stop_word in text for stop_word in stop_words):
            break

        # Skip short paragraphs (junk intro tags etc.)
        if len(text) < 50:  # you can tweak 50 depending on articles
            continue

        content.append(text)

    content = "\n\n".join(content)

except Exception as e:
    content = "N/A"
    print(f"❌ Could not extract content: {e}")

# Close browser
driver.quit()

# === Print Result ===
print(f"Title:\n{title}\n")
print(f"Date:\n{date}\n")
print(f"Author:\n{author}\n")
print("Content:\n")
print(content)