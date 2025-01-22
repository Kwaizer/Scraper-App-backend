from flask import jsonify, request, Blueprint

from Scraper.models import JobPostings, Source, db, Categories
from Scraper.utils.utils import get_job_scraper


router = Blueprint('router', __name__)

@router.route('/jobs')
def jobs():
    chosen_site = request.args.get('site', 'Djinni')
    scraper = get_job_scraper(chosen_site)
    job_postings = scraper.scrape_jobs()
    liked_jobs = {job.link for job in JobPostings.query.all()}

    for job in job_postings:
        # Check if the job link is in liked_jobs
        job_post = JobPostings.query.filter_by(link=job.link).first()
        if job.link in liked_jobs:
            job_post.is_liked = True
            job.is_liked = True
        db.session.commit()
    return {"jobs": [vars(job) for job in job_postings]}


# Route to like a job
@router.route('/api/jobs/like', methods=['POST'])
def like_job():
    data = request.json
    job_link = data.get('link')

    # Check if the job already exists
    job = JobPostings.query.filter_by(link=job_link).first()

    # Handle source
    source_name = data.get('source')
    source = Source.query.filter_by(name=source_name).first()
    if not source:
        source = Source(name=source_name, url="")
        db.session.add(source)
        db.session.commit()

    # Handle categories
    categories = data.get('categories', [])
    if isinstance(categories, str):  # If it's a string, convert it to a single-item list
        categories = [categories]
    category_objects = []
    print(type(categories))
    for category_name in categories:
        print(category_name)
        category = Categories.query.filter_by(name=category_name).first()
        if not category:
            category = Categories(name=category_name)
            db.session.add(category)
            db.session.commit()
        category_objects.append(category)

    if job:
        # Update the existing job posting
        job.is_liked = True
    else:
        # Create a new job posting
        job = JobPostings(
            title=data['title'],
            link=job_link,
            description=data.get('description'),
            pub_date=data.get('pub_date'),
            guid=data.get('guid'),
            is_liked=True,
            source=source  # Link to the source
        )
        db.session.add(job)

    db.session.commit()

    # Link job posting to categories
    job.categories.extend(category_objects)
    db.session.commit()

    return jsonify({'message': 'Job liked successfully'}), 201

# Route to unlike a job
@router.route('/api/jobs/like', methods=['DELETE'])
def unlike_job():
    job_key = request.json.get('jobKey')
    job = JobPostings.query.filter_by(link=job_key).first()
    if job:
        db.session.delete(job)
        db.session.commit()
        return jsonify({'message': 'Job unliked successfully'}), 200
    return jsonify({'message': 'Job not found'}), 404