from Scraper.db import db


class Source(db.Model):
    __tablename__ = 'sources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.Text, nullable=False)

    # Relationships
    job_postings = db.relationship('JobPostings', back_populates='source')

class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

class JobPostings(db.Model):
    __tablename__ = 'job_postings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.String, nullable=True)
    guid = db.Column(db.String, unique=True, nullable=True)
    is_liked = db.Column(db.Boolean, default=False, nullable=False)

    # Foreign key and relationships
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'), nullable=False)
    source = db.relationship('Source', back_populates='job_postings')
    categories = db.relationship(
        'Categories',
        secondary='job_posting_categories',
        back_populates='job_postings'
    )

class JobPostingCategories(db.Model):
    __tablename__ = 'job_posting_categories'
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_postings.id', ondelete='CASCADE'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)

# Update `Categories` with reverse relationship
Categories.job_postings = db.relationship(
    'JobPostings',
    secondary='job_posting_categories',
    back_populates='categories'
)