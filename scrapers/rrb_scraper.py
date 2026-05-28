def scrape_rrb():
    """
    Returns RRB exam data.
    Mock data for development — real dates from RRB 2026 calendar.
    Production version will scrape indianrailways.gov.in
    """
    exams = [
        {
            "source": "RRB",
            "exam_name": "RRB NTPC Graduate Level 2026",
            "apply_last_date": "2026-06-30",
            "exam_date": "2026-09-15",
            "notification_url": "https://www.rrbchennai.gov.in"
        },
        {
            "source": "RRB",
            "exam_name": "RRB Junior Engineer 2026",
            "apply_last_date": "2026-07-20",
            "exam_date": "2026-10-10",
            "notification_url": "https://www.rrbchennai.gov.in"
        },
        {
            "source": "RRB",
            "exam_name": "RRB Group D 2026",
            "apply_last_date": "2026-08-05",
            "exam_date": "2026-11-20",
            "notification_url": "https://www.rrbchennai.gov.in"
        }
    ]

    print(f"Found {len(exams)} exams from RRB")
    return exams

if __name__ == "__main__":
    exams = scrape_rrb()
    for exam in exams:
        print(exam)