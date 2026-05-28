import sys
import traceback

print("Python path:", sys.path)
print("\nTrying to import scrapers.rrb_playwright_scraper...")

try:
    from scrapers import rrb_playwright_scraper
    print("Module imported successfully!")
    print("Dir:", dir(rrb_playwright_scraper))
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()

print("\nTrying to import scrape_rrb directly...")
try:
    from scrapers.rrb_playwright_scraper import scrape_rrb
    print("Import successful!")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
