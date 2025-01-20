from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS
from Scraper.job_scraper import JobScraper
from Scraper.Sites.job_scraper_djinni import JobScraperDjinni
from Scraper.Sites.job_scraper_dou import JobScraperDou

app = Flask(__name__)
# Configure your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/postgres'
db = SQLAlchemy(app)
#CORS(app, resources={r"/jobs": {"origins": "http://localhost:3000"}})

def get_job_scraper(site: str) -> JobScraper:
    if site == "Djinni":
        return JobScraperDjinni('https://djinni.co/jobs/rss/?primary_keyword=Python&amp;exp_level=2y')
    elif site == "Dou":
        return JobScraperDou('https://jobs.dou.ua/vacancies/feeds/?exp=1-3&category=Python')
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

# Job model
class LikedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String, nullable=False)
    more_info = db.Column(db.String, unique=True, nullable=False)
    published_date = db.Column(db.String, nullable=True)
    salary = db.Column(db.String, nullable=True)

# Route to like a job
@app.route('/api/jobs/like', methods=['POST'])
def like_job():
    data = request.json
    job = LikedJob(**data)
    db.session.add(job)
    db.session.commit()
    return jsonify({'message': 'Job liked successfully'}), 201

# Route to unlike a job
@app.route('/api/jobs/like', methods=['DELETE'])
def unlike_job():
    job_key = request.json.get('jobKey')
    job = LikedJob.query.filter_by(more_info=job_key).first()
    if job:
        db.session.delete(job)
        db.session.commit()
        return jsonify({'message': 'Job unliked successfully'}), 200
    return jsonify({'message': 'Job not found'}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
