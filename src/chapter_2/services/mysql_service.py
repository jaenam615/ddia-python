from chapter_2.constants import DummyData
from chapter_2.interfaces.database_interface import DatabaseInterface

class MySQLService(DatabaseInterface):
    def __init__(self, client):
        self._conn = client.connect()
        self.create_tables_if_not_exist()

    def create_resume(self):
        self.create_dummy_data()

    def create_dummy_data(self):
        dummy = DummyData

        with self._conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO resumes (first_name, last_name, date_of_birth) VALUES (%s, %s, %s)",
                (dummy.first_name, dummy.last_name, dummy.date_of_birth),
            )
            resume_id = cursor.lastrowid

            for w in dummy.work_experiences:
                cursor.execute(
                    """
                    INSERT INTO work_experiences (resume_id, company, title, start_date, end_date)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        resume_id,
                        w.get("company"),
                        w.get("title"),
                        w.get("start_date"),
                        w.get("end_date"),
                    ),
                )

            for e in dummy.education:
                cursor.execute(
                    """
                    INSERT INTO education (resume_id, school, degree, start_date, end_date)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        resume_id,
                        e.get("school"),
                        e.get("degree"),
                        e.get("start_date"),
                        e.get("end_date"),
                    ),
                )

            self._conn.commit()
            return resume_id



    def get_resume(self, resume_id: int) -> dict | None:
        with self._conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, first_name, last_name, date_of_birth FROM resumes WHERE id = %s",
                (resume_id,),
            )
            resume = cursor.fetchone()
            if not resume:
                return None

            resume_obj = {
                "id": resume[0],
                "first_name": resume[1],
                "last_name": resume[2],
                "date_of_birth": resume[3].isoformat() if resume[3] else None,
            }

            cursor.execute(
                """
                SELECT company, title, start_date, end_date
                FROM work_experiences
                WHERE resume_id = %s
                ORDER BY start_date
                """,
                (resume_id,),
            )
            work_exp = cursor.fetchall()
            resume_obj["work_experiences"] = [
                {
                    "company": w[0],
                    "title": w[1],
                    "start_date": w[2].isoformat() if w[2] else None,
                    "end_date": w[3].isoformat() if w[3] else None,
                }
                for w in work_exp
            ]

            cursor.execute(
                """
                SELECT school, degree, start_date, end_date
                FROM education
                WHERE resume_id = %s
                ORDER BY start_date
                """,
                (resume_id,),
            )
            education = cursor.fetchall()
            resume_obj["education"] = [
                {
                    "school": e[0],
                    "degree": e[1],
                    "start_date": e[2].isoformat() if e[2] else None,
                    "end_date": e[3].isoformat() if e[3] else None,
                }
                for e in education
            ]

            return resume_obj

    def clean_up(self):
        with self._conn.cursor() as cursor:
            cursor.execute("DELETE FROM resumes")
            cursor.execute("DELETE FROM work_experiences")
            cursor.execute("DELETE FROM education")
            self._conn.commit()

    def close(self):
        self._conn.close()

    def create_tables_if_not_exist(self):
        with self._conn.cursor() as cursor:
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS resumes
                           (
                               id
                               INT
                               AUTO_INCREMENT
                               PRIMARY
                               KEY,
                               first_name
                               VARCHAR
                           (
                               100
                           ) NOT NULL,
                               last_name VARCHAR
                           (
                               100
                           ) NOT NULL,
                               date_of_birth DATE
                               )
                           """)

            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS work_experiences
                           (
                               id
                               INT
                               AUTO_INCREMENT
                               PRIMARY
                               KEY,
                               resume_id
                               INT
                               NOT
                               NULL,
                               company
                               VARCHAR
                           (
                               255
                           ),
                               title VARCHAR
                           (
                               255
                           ),
                               start_date DATE,
                               end_date DATE,
                               FOREIGN KEY
                           (
                               resume_id
                           ) REFERENCES resumes
                           (
                               id
                           ) ON DELETE CASCADE
                               )
                           """)

            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS education
                           (
                               id
                               INT
                               AUTO_INCREMENT
                               PRIMARY
                               KEY,
                               resume_id
                               INT
                               NOT
                               NULL,
                               school
                               VARCHAR
                           (
                               255
                           ),
                               degree VARCHAR
                           (
                               255
                           ),
                               start_date DATE,
                               end_date DATE,
                               FOREIGN KEY
                           (
                               resume_id
                           ) REFERENCES resumes
                           (
                               id
                           ) ON DELETE CASCADE
                               )
                           """)
            self._conn.commit()