from datetime import timedelta

DATABASE_URL="postgresql://neondb_owner:npg_7V0mWajfNbHt@ep-blue-flower-adnx839z-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
uri = DATABASE_URL

if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)

class Config:
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "dev-secret-key"
    JWT_SECRET_KEY = "dev-jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)