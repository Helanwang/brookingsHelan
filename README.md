# Comprehensive Overview: Brookings Search Results and Alternative Scraping Strategies

## 📄 Task Summary
The primary task was to search for **13 specific race-related queries** on the Brookings Institution’s website and retrieve all related articles.

**Keywords searched:**

[‘race bias’, ‘racial bias’, ‘race prejudice’, ‘racial prejudice’, ‘race discrimination’,
‘racial discrimination’, ‘race disparity’, ‘racial disparity’, ‘race inequality’, ‘racial inequality’,
‘race difference’, ‘racial difference’, ‘racism’]

---

## 📊 Search Results Breakdown
All articles found for each keyword:

| Query               | Number of Articles |
|----------------------|--------------------|
| race bias            | 8676               |
| racial bias          | 1261               |
| race prejudice       | 85                 |
| racial prejudice     | 39                 |
| race discrimination  | 847                |
| racial discrimination| 518                |
| race disparity       | 1083               |
| racial disparity     | 705                |
| race inequality      | 2141               |
| racial inequality    | 730                |
| race difference      | 5897               |
| racial difference    | 985                |
| racism               | 981                |

---

## ✅ Queries with Fewer than 1000 Results
These queries are feasible to scrape directly without issues:

```python
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

```
⚠️ Queries with Over 1000 Results

These queries exceed Algolia’s 1000-record limit:

```python
over_1000 = {
    'race bias': 8676,
    'racial bias': 1261,
    'race disparity': 1083,
    'race inequality': 2141,
    'race difference': 5897
}
```
---
🗂 Planned CSV Output

Each row in the CSV will include:
- Index
- Article Title
- URL
- Author
- Content
- Date
- Think Tank
- Matched Keywords
---
🛑 Technical Limitation: Algolia Search Cap

Brookings uses Algolia as its internal search engine. Algolia limits external users to 1000 search results per query. Even with pagination or endless scrolling, the cap remains at 1000 accessible articles.

---

⚠️ Key Obstacle

Brookings does not offer public-facing filters (e.g., by year, category, topic) to narrow down results.
This makes it impossible to scrape the entire dataset for queries with over 1000 results directly.

---

## 💡 Alternative Options Explored
- **Wayback Machine:**  
  Snapshots available, but URLs are often outdated or irrelevant for scraping.
- **LexisNexis:**  
  University LexisNexis does not include Brookings. Awaiting potential Stanford access.
- **✅ Google Search API:**  
  Free trial allows scraping up to 100 URLs with year-based filters. Additional scraping requires payment and further testing.

🚀 Next Steps
Explore Google Search API for feasible extended scraping.
---

Written by:
Helan Wang
📧 helanwang_12@berkeley.edu