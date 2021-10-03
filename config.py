import os

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('POSTGRES_DB', 'gis_lab')
DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'andreasmc10')

DB_CONFIG = {
    'host':     DB_HOST,
    'database': DB_NAME,
    'user':     DB_USER,
    'password': DB_PASS,
}