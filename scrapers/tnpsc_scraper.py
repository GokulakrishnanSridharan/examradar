from datetime import datetime

def scrape_tnpsc():
    """
    Returns TNPSC exam data.
    Currently uses mock data for development.
    Production version will scrape tnpsc.gov.in or aggregator sites.
    """
    exams = [
        {
            "source": "TNPSC",
            "exam_name": "TNPSC Group 1 - Combined Civil Services Examination",
            "apply_last_date": "2026-07-15",
            "exam_date": "2026-09-06",
            "notification_url": "https://www.tnpsc.gov.in"
        },
        {
            "source": "TNPSC",
            "exam_name": "TNPSC Group 2 - Combined Civil Services Examination",
            "apply_last_date": "2026-09-10",
            "exam_date": "2026-10-25",
            "notification_url": "https://www.tnpsc.gov.in"
        },
        {
            "source": "TNPSC",
            "exam_name": "TNPSC Group 4 - Combined Civil Services Examination IV",
            "apply_last_date": "2026-11-01",
            "exam_date": "2026-12-20",
            "notification_url": "https://www.tnpsc.gov.in"
        },
        {
            "source": "TNPSC",
            "exam_name": "TNPSC CTS Non-Interview 2026",
            "apply_last_date": "2026-06-25",
            "exam_date": "2026-08-30",
            "notification_url": "https://www.tnpsc.gov.in"
        }
    ]

    print(f"Found {len(exams)} exams from TNPSC")
    return exams

if __name__ == "__main__":
    exams = scrape_tnpsc()
    for exam in exams:
        print(exam)