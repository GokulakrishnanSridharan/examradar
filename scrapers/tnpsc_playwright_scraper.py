from playwright.sync_api import sync_playwright
from datetime import datetime

def parse_date(date_str):
    """
    Converts date from DD.MM.YYYY format to YYYY-MM-DD format
    which PostgreSQL understands.
    Example: 20.05.2026 -> 2026-05-20
    """
    try:
        return datetime.strptime(date_str.strip(), "%d.%m.%Y").strftime("%Y-%m-%d")
    except:
        return None

def scrape_tnpsc():
    """
    Scrapes TNPSC exam calendar from testbook.com using Playwright.
    Playwright opens a real Chromium browser, waits for JavaScript
    to render the page, then extracts exam rows from the table.
    """
    exams = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Opening TNPSC exam calendar page...")
        page.goto("https://testbook.com/tnpsc/exam-calendar", timeout=30000)
        page.wait_for_load_state("networkidle")

        print("Page loaded. Extracting exam data...")

        # get all table rows
        rows = page.query_selector_all("table tr")

        for row in rows:
            cells = row.query_selector_all("td")

            # we need exactly 5 columns — skip header rows
            if len(cells) != 5:
                continue

            serial_no = cells[0].inner_text().strip()

            # skip if first column is not a number
            if not serial_no.isdigit():
                continue

            exam_name = cells[1].inner_text().strip()
            notification_date = parse_date(cells[2].inner_text().strip())
            exam_date = parse_date(cells[3].inner_text().strip())

            exams.append({
                "source": "TNPSC",
                "exam_name": exam_name,
                "apply_last_date": notification_date,
                "exam_date": exam_date,
                "notification_url": "https://testbook.com/tnpsc/exam-calendar"
            })

        browser.close()

    print(f"Found {len(exams)} exams from TNPSC")
    return exams


if __name__ == "__main__":
    exams = scrape_tnpsc()
    for exam in exams:
        print(exam)