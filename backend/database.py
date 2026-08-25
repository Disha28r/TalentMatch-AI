import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():

    return psycopg.connect(DATABASE_URL)

def create_interviews_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (

            id SERIAL PRIMARY KEY,

            candidate VARCHAR(255) NOT NULL,

            interview_date DATE NOT NULL,

            interview_time TIME NOT NULL,

            mode VARCHAR(50) NOT NULL

        );
    """)

    connection.commit()

    cursor.close()

    connection.close()