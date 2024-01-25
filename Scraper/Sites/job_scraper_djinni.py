from typing import List
from bs4 import BeautifulSoup
import requests
from Scraper.job_scraper import JobScraper
from Scraper.job_posting import JobPosting


class JobScraperDjinni(JobScraper):

    def scrape_jobs(self) -> List[JobPosting]:
        html_text = requests.get(self.url)
        soup = BeautifulSoup(html_text.text, 'lxml')
        jobs = soup.find_all('li', class_='mb-4')
        job_ids = [job.get('id') for job in jobs]

        job_posts = []
        for job in jobs:
            company_name = job.find('a', class_='text-body js-analytics-event').text.replace('  ', '').strip()
            job_title = job.find('a', class_='job-item__title-link').text.replace('  ', '').strip()
            published_date = "TODO"  
            skills = "TODO"  
            job_salary_element = job.find('span', class_='text-success text-nowrap')
            salary = (job_salary_element.text
                      .replace('  ', '').strip()) if job_salary_element is not None else "Isn't available"
            more_info = f"https://djinni.co{job.h3.find('a', class_='job-item__title-link').get('href')}"

            job_post = JobPosting(company_name, job_title, published_date, skills, salary, more_info)
            job_posts.append(job_post)

        return job_posts
