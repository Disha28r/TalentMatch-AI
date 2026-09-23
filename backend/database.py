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

def create_candidates_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (

            id SERIAL PRIMARY KEY,

            candidate_id VARCHAR(36) UNIQUE NOT NULL,

            name VARCHAR(255) NOT NULL,

            resume_score INTEGER,

            resume_details TEXT,

            matched_skills JSONB,

            missing_required_skills JSONB,

            missing_preferred_skills JSONB,

            partially_matched_skills JSONB,

            skill_gap_summary TEXT,

            recommendations JSONB,

            selection_status VARCHAR(50)

        );
    """)

    

    connection.commit()

    cursor.close()

    connection.close()
    
if __name__ == "__main__": 
    create_candidates_table() 
    print("Candidates table created successfully.")