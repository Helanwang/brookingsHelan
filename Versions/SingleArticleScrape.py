from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.brookings.edu/articles/do-americans-really-want-a-policy-revolution/"
driver.get(url)

# Wait until at least one <p> tag inside #content is loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#content p"))
)

# Get the title
title = driver.find_element(By.TAG_NAME, "h1").text

# Grab all paragraphs inside the #content container
paragraphs = driver.find_elements(By.CSS_SELECTOR, "#content p")
content = "\n\n".join(p.text for p in paragraphs if p.text.strip())

print(f"Title:\n{title}\n")
print("Article Content:\n")
print(content)

driver.quit()