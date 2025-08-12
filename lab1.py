import requests
from bs4 import BeautifulSoup
import pandas as pd
BASE_URL = "https://remoteok.com/remote-dev-jobs"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}
response = requests.get(BASE_URL, headers=HEADERS)
if response.status_code != 200:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
    exit()
soup = BeautifulSoup(response.text, "html.parser")
job_listings = soup.find_all("tr", class_="job")
jobs_data = []
for job in job_listings:
    company = job.find("td", class_="company").get_text(strip=True) if job.find("td", class_="company") else None
    role = job.find("h2", itemprop="title").get_text(strip=True) if job.find("h2", itemprop="title") else None
    location = job.find("div", class_="location").get_text(strip=True) if job.find("div", class_="location") else "Remote"
    tags = [tag.get_text(strip=True) for tag in job.find_all("div", class_="tag")]
    
    jobs_data.append({
        "Company Name": company,
        "Job Role": role,
        "Location": location,
        "Features/Tags": ", ".join(tags) if tags else None
    })
df = pd.DataFrame(jobs_data)
df.to_csv("remoteok_jobs_1RUA24CSE0141.csv", index=False, encoding="utf-8")
print(f"Scraped {len(df)} job postings and saved to 'remoteok_jobs_1RUA24CSE0141.csv'")
