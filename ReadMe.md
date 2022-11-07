
# Running the locally
- Install docker, the [desktop application] (https://www.docker.com/products/docker-desktop/) will install docker and provide a GUI to manage your containers

- Run the database service locally with `docker compose up -d db`

- Build and run the application locally with `docker compose up --build pythonapp`

# Execute unit tests

# Execute integration tests

# TODOs
- Utility for Get ALL
- Batch inserts instead of one by one
- Use of generic for inserts
- Handle exceptions

# Questions
- Rank by market or 
# Dependencies
- flask: Python framework
- psycopg2-binary: To Create Postgres Database connection
- Flask-SQLAlchemy: Generate SQL queries automatically
- Flask-APScheduler: Schedule a job

# References
- Sample project for Python/Flask: https://www.tinystacks.com/blog-post/flask-crud-api-with-postgres/
- Flask/SQL Alchemy: https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/
- API Documentation: https://docs.cryptowat.ch/rest-api/
- Scheduling a function with Flask: https://www.techcoil.com/blog/how-to-create-an-interval-task-that-runs-periodically-within-your-python-3-flask-application-with-flask-apscheduler/