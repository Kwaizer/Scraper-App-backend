from typing import List
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup
import requests
from Scraper.job_scraper import JobScraper
from Scraper.job_posting import JobPosting


class JobScraperDou(JobScraper):
    def scrape_jobs(self) -> List[JobPosting]:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        print(self.url)
        response = requests.get(self.url, headers=hdr)
        if response.status_code == 200:
            # Parse the XML content
            soup = BeautifulSoup(response.content, 'xml')
            job_posts = []
            # Find all <item> elements from .RSS
            items = soup.find_all('item')
            for item in items:
                title = item.title.text if item.title else "No title"
                link = item.link.text if item.link else "No link"
                description = item.description.text if item.description else "No description"
                pub_date = item.pubDate.text if item.pubDate else "No publication date"
                guid = item.guid.text if item.guid else "No GUID"
                categories = \
                    parse_qs(urlparse(self.url).query).get(
                    'category', ['No category'])[0]
                description_soup = BeautifulSoup(description, 'html.parser')
                description_text = description_soup.get_text(strip=True)
                job_post = JobPosting(title, link, description_text, pub_date, guid, categories, False, "Dou")
                job_posts.append(job_post)

            return job_posts
        else:
            print("Failed to fetch RSS feed:", response.status_code)

