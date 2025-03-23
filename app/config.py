# Change this file according to your MySQL configuration
MYSQL_HOST = '127.0.0.1'  # Use 127.0.0.1 instead of localhost
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Chunniboy123#'
MYSQL_DB = 'soilmarket'

# Construct the SQLAlchemy URI dynamically
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DB}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
