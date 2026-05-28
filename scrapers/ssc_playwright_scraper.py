from playwright.sync_api import sync_playwright
from datetime import datetime

def parse_date(date_str):
    formats = ["%d.%m.%Y", "%d/%m/%Y", "%B %Y", "%b %Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
        except:
            continue
    return None

def scrape_ssc():
    """
    Scrapes SSC exam calendar from testbook.com using Playwright.
    """
    exams = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Opening SSC exam calendar page...")
        page.goto("https://testbook.com/ssc-jobs/exam-calendar", timeout=30000)
        page.wait_for_load_state("networkidle")

        print("Page loaded. Extracting exam data...")

        rows = page.query_selector_all("table tr")

        for row in rows:
            cells = row.query_selector_all("td")

            if len(cells) < 3:
                continue

            serial_no = cells[0].inner_text().strip()
            if not serial_no.isdigit():
                continue

            exam_name = cells[1].inner_text().strip()
            date_text = cells[2].inner_text().strip()
            exam_date_text = cells[3].inner_text().strip() if len(cells) > 3 else None

            exams.append({
                "source": "SSC",
                "exam_name": exam_name,
                "apply_last_date": parse_date(date_text),
                "exam_date": parse_date(exam_date_text) if exam_date_text else None,
                "notification_url": "https://testbook.com/ssc-jobs/exam-calendar"
            })

        browser.close()

    print(f"Found {len(exams)} exams from SSC")
    return exams

if __name__ == "__main__":
    exams = scrape_ssc()
    for exam in exams:
        print(exam)