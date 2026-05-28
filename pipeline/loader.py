import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.database import get_connection

def load_exams(exams):
    """
    Takes a list of exam dictionaries and inserts them into the database.
    Skips duplicates — same source + exam_name won't be inserted twice.
    """
    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    for exam in exams:
        # check if this exam already exists
        cursor.execute("""
            SELECT id FROM exams 
            WHERE source = %s AND exam_name = %s
        """, (exam["source"], exam["exam_name"]))

        existing = cursor.fetchone()

        if existing:
            skipped += 1
            continue  # don't insert duplicate

        # insert new exam
        cursor.execute("""
            INSERT INTO exams (source, exam_name, apply_last_date, exam_date, notification_url)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            exam["source"],
            exam["exam_name"],
            exam["apply_last_date"],
            exam["exam_date"],
            exam["notification_url"]
        ))
        inserted += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Inserted: {inserted} | Skipped (duplicates): {skipped}")

if __name__ == "__main__":
    from scrapers.tnpsc_scraper import scrape_tnpsc
    from scrapers.rrb_scraper import scrape_rrb
    from scrapers.ssc_scraper import scrape_ssc

    all_exams = []
    all_exams.extend(scrape_tnpsc())
    all_exams.extend(scrape_rrb())
    all_exams.extend(scrape_ssc())

    load_exams(all_exams)