import re
from typing import List
from bs4 import BeautifulSoup
import requests
from Scraper.job_scraper import JobScraper
from Scraper.job_posting import JobPosting


class JobScraperDjinni(JobScraper):

    def scrape_jobs(self) -> List[JobPosting]:
        # Fetch the RSS content
        job_posts = []
        response = requests.get(self.url)
        if response.status_code == 200:
            # Parse the XML content
            soup = BeautifulSoup(response.content, 'xml')

            # Find all <item> elements from .RSS
            jobs = soup.find_all('item')
            for job in jobs:
                title = job.title.text if job.title else "No title"
                link = job.link.text if job.link else "No link"
                description = job.description.text if job.description else "No description"
                description_soup = BeautifulSoup(description, 'html.parser')
                description_text = description_soup.get_text(strip=True)
                pub_date = job.pubDate.text if job.pubDate else "No publication date"
                guid = job.guid.text if job.guid else "No GUID"
                categories = [cat.text for cat in job.find_all('category') if cat.text]
                job_post = JobPosting(title, link, description_text, pub_date, guid, categories, False, "Djinni")
                job_posts.append(job_post)

            return job_posts
        else:
            print("Failed to fetch RSS feed:", response.status_code)
