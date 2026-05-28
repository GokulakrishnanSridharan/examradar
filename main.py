import sys
import os
import schedule
import time

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from scrapers.tnpsc_playwright_scraper import scrape_tnpsc
from scrapers.rrb_playwright_scraper import scrape_rrb
from scrapers.ssc_playwright_scraper import scrape_ssc
from pipeline.loader import load_exams
from data.database import create_tables, cleanup_expired_exams, get_applicable_exams

def run_pipeline():
    print("=" * 40)
    print("ExamRadar Pipeline Running...")
    print("=" * 40)

    # step 1 — ensure tables exist
    print("\n[1/4] Setting up database...")
    create_tables()

    # step 2 — clean up expired exams
    print("\n[2/4] Cleaning up expired exams...")
    cleanup_expired_exams()

    # step 3 — scrape all sources
    print("\n[3/4] Scraping exam sources...")
    all_exams = []
    all_exams.extend(scrape_tnpsc())
    all_exams.extend(scrape_rrb())
    all_exams.extend(scrape_ssc())
    print(f"Total exams fetched: {len(all_exams)}")

    # step 4 — load into database
    print("\n[4/4] Loading into database...")
    load_exams(all_exams)

    print("\nPipeline complete.")
    print("=" * 40)
    
    # Show applicable exams summary
    print("\n📊 APPLICABLE EXAMS TRACKING")
    print("=" * 40)
    tracking = get_applicable_exams()
    print(f"✅ Applicable (can apply): {tracking['applicable_count']}")
    print(f"❌ Expired (cannot apply): {tracking['expired_count']}")
    print(f"📈 Total exams in database: {tracking['total_count']}")
    print("=" * 40)
    
    print("\nNext run in 24 hours.")

if __name__ == "__main__":
    # run once immediately on startup
    run_pipeline()

    # then schedule every 24 hours
    # schedule.every(1).minutes.do(run_pipeline)
    schedule.every(24).hours.do(run_pipeline)

    print("\nScheduler running. Dashboard launching...")
    print("Press Ctrl+C to stop.\n")

    # launch dashboard in background
    os.system("start cmd /k streamlit run dashboard/app.py")

    # keep scheduler alive
    while True:
        schedule.run_pending()
        time.sleep(60)  # check every minute