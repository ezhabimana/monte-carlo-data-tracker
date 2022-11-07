
# Running the locally
- Install docker, the [desktop application] (https://www.docker.com/products/docker-desktop/) will install docker and provide a GUI to manage your containers

- Run the database service locally with `docker compose up -d db`

- Build and run the application locally with `docker compose up --build pythonapp`

# Execute unit tests

# Execute integration tests

# Dependencies
- flask: Python framework
- psycopg2-binary: To Create Postgres Database connection
- Flask-SQLAlchemy: Generate SQL queries automatically

# References
- Sample project for Python/Flask: https://www.tinystacks.com/blog-post/flask-crud-api-with-postgres/
- Flask/SQL Alchemy: https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/
- API Documentation: https://docs.cryptowat.ch/rest-api/