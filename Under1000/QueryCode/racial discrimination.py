import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ======= Setup Chrome (headless) =======
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ======= Input & Output =======
keyword = "racial discrimination"

input_csv = f"/Users/helanwang/PycharmProjects/brookingsHelan/Under1000/URL/brookings_{keyword.replace(' ', '_')}_urls.csv"
output_csv = f"/Users/helanwang/PycharmProjects/brookingsHelan/Under1000/Articles/brookings_{keyword.replace(' ', '_')}_articles2.csv"
think_tank = "Brookings Institution"

# ======= Helper Functions =======
def find_author(driver):
    authors = []
    try:
        author1 = driver.find_element(By.CSS_SELECTOR, "#person-hover-1").text.strip()
        if author1:
            authors.append(author1)
    except:
        pass
    try:
        author2 = driver.find_element(By.CSS_SELECTOR, "#person-hover-2").text.strip()
        if author2:
            authors.append(author2)
    except:
        pass

    if authors:
        return ", ".join(authors)  # Joins both authors with comma
    else:
        return "N/A"

def find_date(driver):
    selectors = [
        "#hero > div.tm-article-research.tm-container.no-takeaways > div.grid-4-8.wrapper > div > div.left-col.md\\:col-span-6.lg\\:col-span-5.xl\\:col-span-4 > div > div.article-meta > div > p",
        ".article-meta p",
        "#hero > div.tm-article-research.tm-container.no-takeaways.theme-light-gray.tm-article-commentary.no-img > div > div > div > div > div > div:nth-child(2) > div > p",
        "#hero > div.tm-article-research.tm-container.with-takeaways > div.grid-4-8.wrapper > div > div.left-col.md\\:col-span-6.lg\\:col-span-5.xl\\:col-span-4 > div > div > div > p",
        "#hero > div.key-details.event-key-details.px-outer.lg\\:px-outer-lg > div > div.content-well.lg\\:col-span-6.flex.flex-col > div > ul > li > h5",
    ]
    for selector in selectors:
        try:
            return driver.find_element(By.CSS_SELECTOR, selector).text
        except:
            continue
    return "N/A"

# ======= Load URLs from CSV =======
urls = []
with open(input_csv, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        urls.append(row['Article URL'])

# ======= Prepare Output File with Custom Headers =======
with open(output_csv, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.writer(f_out)
    writer.writerow([
        "Index", "Article Title", "URL",
        "Author", "Content", "Date", "Think Tank", "Matched Keywords"
    ])

    # ======= Process Each Article =======
    for index, url in enumerate(urls, start=1):
        print(f"🔗 Scraping ({index}): {url}")
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#content p"))
            )

            # === Get Title ===
            try:
                title = driver.find_element(By.TAG_NAME, "h1").text
            except:
                title = "N/A"

            # === Get Author (new helper) ===
            author = find_author(driver)

            # === Get Date (new helper) ===
            date = find_date(driver)

            # === Get Clean Content ===
            try:
                paragraphs = driver.find_elements(By.CSS_SELECTOR, "#content p")

                content = []
                stop_words = ["RELATED CONTENT", "RELATED BOOKS", "AUTHORS", "The Brookings Institution"]
                reference_pattern = re.compile(r"^\[\w+\]")  # Matches [i], [ii], etc.

                for p in paragraphs:
                    text = p.text.strip()

                    # Skip if paragraph is inside an .editors-note div
                    try:
                        parent = p.find_element(By.XPATH, "./ancestor::div[contains(@class, 'editors-note')]")
                        continue
                    except:
                        pass

                    # Stop at footer content
                    if any(stop_word in text for stop_word in stop_words):
                        break

                    # Stop at references like [i], [ii], [iii]
                    if reference_pattern.match(text):
                        break

                    # Skip short paragraphs (<25 words)
                    if len(text.split()) < 25:
                        continue

                    content.append(text)

                content = "\n\n".join(content)

            except Exception as e:
                content = "N/A"
                print(f"❌ Could not clean content: {e}")

            # === Write Final Row ===
            writer.writerow([
                index, title, url,
                author, content, date, think_tank, keyword
            ])

        except Exception as e:
            print(f"❌ Failed to scrape {url}: {e}")
            writer.writerow([
                index, "ERROR", url, "", "", "", think_tank, keyword
            ])

# ======= Finish =======
driver.quit()
print(f"\n✅ Finished. Clean article data saved to {output_csv}")