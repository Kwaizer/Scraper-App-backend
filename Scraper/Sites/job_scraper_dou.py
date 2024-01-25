from typing import List
from bs4 import BeautifulSoup
import requests
from Scraper.job_scraper import JobScraper
from Scraper.job_posting import JobPosting


class JobScraperDou(JobScraper):
    def scrape_jobs(self) -> List[JobPosting]:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        html_text = requests.get(self.url, headers=hdr)
        soup = BeautifulSoup(html_text.text, 'lxml')
        jobs = soup.find_all('li', class_='l-vacancy')

        job_posts = []
        for job in jobs:
            company_name = job.find('a', class_='company').text.replace('  ', '').strip()
            job_title = job.find('a', class_='vt').text.replace('  ', '').strip()
            published_date = job.div.text.replace('  ', '').strip()
            skills = "TODO"
            job_salary_element = job.find('span', class_='salary')
            salary = (job_salary_element.text
                      .replace('  ', '').strip()) if job_salary_element is not None else "Isn't available"
            more_info: str = job.find('a', class_='vt').get('href')
            job_post = JobPosting(company_name, job_title, published_date, skills, salary, more_info)
            job_posts.append(job_post)

        return job_posts
