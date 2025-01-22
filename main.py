from flask import Flask

from Scraper.db import db
from Scraper.router import router

app = Flask(__name__)
# Configure your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/postgres'
db.init_app(app)  # Initialize the database with the app
app.register_blueprint(router)



if __name__ == "__main__":
    app.run(debug=False, port=5000)
