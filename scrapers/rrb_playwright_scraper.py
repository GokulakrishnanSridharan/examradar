from playwright.sync_api import sync_playwright
from datetime import datetime

def parse_date(date_str):
    """
    Tries multiple date formats since RRB uses different formats.
    Returns YYYY-MM-DD string or None.
    """
    formats = ["%d.%m.%Y", "%d/%m/%Y", "%B %Y", "%b %Y", "%d-%m-%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
        except:
            continue
    return None

def scrape_rrb():
    """
    Scrapes RRB exam calendar from testbook.com using Playwright.
    """
    exams = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print("Opening RRB exam calendar page...")
            page.goto("https://testbook.com/railway-jobs/rrb-exam-calendar", timeout=30000)
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

                apply_date = parse_date(date_text)
                exam_date = parse_date(exam_date_text) if exam_date_text else None

                if apply_date:  # Only add if we successfully parsed the date
                    exams.append({
                        "source": "RRB",
                        "exam_name": exam_name,
                        "apply_last_date": apply_date,
                        "exam_date": exam_date,
                        "notification_url": "https://testbook.com/railway-jobs/rrb-exam-calendar"
                    })

            browser.close()

    except Exception as e:
        print(f"Error scraping RRB: {e}")

    print(f"Found {len(exams)} exams from RRB")
    return exams

if __name__ == "__main__":
    exams = scrape_rrb()
    for exam in exams:
        print(exam)
