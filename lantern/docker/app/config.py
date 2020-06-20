class Config:
    PG_USER = "postgres"
    PG_PASSWORD = 'docker'
    PG_HOST = "db"
    PG_PORT = 5432
    DB_NAME = "postgres"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False




