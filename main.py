from flask import Flask, jsonify, render_template, request
#from flask_cors import CORS
from Scraper.job_scraper import JobScraper
from Scraper.Sites.job_scraper_djinni import JobScraperDjinni
from Scraper.Sites.job_scraper_dou import JobScraperDou

app = Flask(__name__)
#CORS(app, resources={r"/jobs": {"origins": "http://localhost:3000"}})

def get_job_scraper(site: str) -> JobScraper:
    if site == "Djinni":
        return JobScraperDjinni('https://djinni.co/jobs/?q_company=&primary_keyword=Python&exp_level=2y')
    elif site == "Dou":
        return JobScraperDou('https://jobs.dou.ua/vacancies/?category=Python&exp=1-3')
    else:
        raise ValueError(f"Unsupported site: {site}")


#if __name__ == "__main__":


    #for job_posting in job_postings:
     #   print(job_posting)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/jobs')
def jobs():
    chosen_site = request.args.get('site', 'Djinni')
    scraper = get_job_scraper(chosen_site)
    job_postings = scraper.scrape_jobs()
    #return render_template('jobs.html', job_postings=job_postings)
    return {"jobs": [vars(job) for job in job_postings]}

@app.route('/members')
def members():
    return {"members": ["member1", "member2", "member3"]}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
