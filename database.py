import mysql.connector
import random

# Database connection

def get_db_connection():
    return mysql.connector.connect(
        host="",
        user="",
        password="",
        database="",
    )


def retrieve_random_joke():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT Nr FROM witzdestages")
        result = cursor.fetchall()
        if not result:
            print("No jokes found in database.")
            return None
        
        joke_nr = [row[0] for row in result]
        random_id = random.choice(joke_nr)
        cursor.execute("SELECT Jokes FROM witzdestages WHERE Nr = %s", (random_id,))
        MyResult = cursor.fetchone()[0]

        return MyResult
    except Exception as e:
        print(f"Fehler beim Abrufen eines zufälligen Witzes: {e}")
        return None
    finally:
        cursor.close()
        db.close()

