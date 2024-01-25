from abc import ABC, abstractmethod
from typing import List


class JobScraper(ABC):

    def __init__(self, url):
        self.url = url

    @abstractmethod
    def scrape_jobs(self) -> List:
        pass
