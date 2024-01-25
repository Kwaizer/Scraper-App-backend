class JobPosting:
    def __init__(self, company_name, job_title, published_date, skills, salary, more_info):
        self.company_name = company_name
        self.job_title = job_title
        self.published_date = published_date
        self.skills = skills
        self.salary = salary
        self.more_info = more_info

    def __str__(self):
        return f"Company Name: {self.company_name}\n" \
               f"Job Title: {self.job_title}\n" \
               f"Skills: {self.skills}\n" \
               f"Salary: {self.salary}\n" \
               f"Published Date: {self.published_date}\n" \
               f"More Info: {self.more_info}\n" \
               f"----------------------------------"
    
    def to_dict(self):
        return {
            "company_name": self.company_name,
            "job_title": self.job_title,
            "published_date": self.published_date,
            "skills": self.skills,
            "salary": self.salary,
            "more_info": self.more_info,
        }
