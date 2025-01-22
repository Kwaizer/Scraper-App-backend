from Scraper.Sites.job_scraper_djinni import JobScraperDjinni
from Scraper.Sites.job_scraper_dou import JobScraperDou
from Scraper.job_scraper import JobScraper


def get_job_scraper(site: str) -> JobScraper:
    if site == "Djinni":
        return JobScraperDjinni('https://djinni.co/jobs/rss/?primary_keyword=Python&amp;exp_level=2y')
    elif site == "Dou":
        return JobScraperDou('https://jobs.dou.ua/vacancies/feeds/?exp=1-3&category=Python')
    else:
        raise ValueError(f"Unsupported site: {site}")