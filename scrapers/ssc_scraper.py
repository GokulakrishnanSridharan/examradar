def scrape_ssc():
    """
    Returns SSC exam data.
    Mock data for development — real dates from SSC 2026 calendar.
    Production version will scrape ssc.gov.in
    """
    exams = [
        {
            "source": "SSC",
            "exam_name": "SSC CGL 2026 - Combined Graduate Level",
            "apply_last_date": "2026-06-15",
            "exam_date": "2026-09-01",
            "notification_url": "https://ssc.gov.in"
        },
        {
            "source": "SSC",
            "exam_name": "SSC CHSL 2026 - Combined Higher Secondary Level",
            "apply_last_date": "2026-07-10",
            "exam_date": "2026-10-05",
            "notification_url": "https://ssc.gov.in"
        },
        {
            "source": "SSC",
            "exam_name": "SSC MTS 2026 - Multi Tasking Staff",
            "apply_last_date": "2026-08-20",
            "exam_date": "2026-11-15",
            "notification_url": "https://ssc.gov.in"
        }
    ]

    print(f"Found {len(exams)} exams from SSC")
    return exams

if __name__ == "__main__":
    exams = scrape_ssc()
    for exam in exams:
        print(exam)