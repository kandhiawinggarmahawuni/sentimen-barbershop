from playwright.sync_api import sync_playwright, TimeoutError
from bs4 import BeautifulSoup
import pandas as pd
import time


def scroll_with_arrow_keys(page, scroll_count=300):
    for _ in range(scroll_count):
        page.keyboard.press("ArrowDown")
        time.sleep(0.2)


def extract_reviews_from_page(page_content):
    soup = BeautifulSoup(page_content, "html.parser")
    review_blocks = soup.select('.jftiEf')  # Selector untuk blok ulasan
    reviews = []

    for block in review_blocks:
        try:
            name = block.select_one('.d4r55').text
            rating = block.select_one('.kvMYJc')['aria-label']
            review_text = block.select_one('.MyEned').text
            date = block.select_one('.rsqaWe').text
            reviews.append({
                "name": name,
                "rating": rating,
                "review": review_text,
                "date": date
            })
        except Exception as e:
            continue

    return reviews


def scrape_google_reviews(map_url, scroll_times=50):
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                locale='id-ID',  # paksa Bahasa Indonesia
                viewport={'width': 1920, 'height': 1080}  # Set viewport size
            )
            page = context.new_page()
            
            # Set timeout lebih lama (60 detik)
            page.set_default_timeout(60000)
            
            # Navigate dengan retry
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    page.goto(map_url, wait_until='networkidle')
                    break
                except TimeoutError:
                    if attempt == max_retries - 1:
                        raise
                    print(f"Retry {attempt + 1}/{max_retries}...")
                    time.sleep(5)
            
            # Tunggu halaman dimuat
            page.wait_for_load_state('networkidle')
            time.sleep(5)

            # Klik tombol "Ulasan" / "All reviews"
            try:
                page.click('text="Ulasan"', timeout=10000)
                time.sleep(3)
            except Exception as e:
                print(f"Gagal klik tombol Ulasan: {e}")
                pass

            # Klik "Urutkan" → "Terbaru"
            try:
                page.click('text="Urutkan"', timeout=10000)  # atau 'Sort by' jika English
                time.sleep(1)

                # Ambil elemen berdasarkan urutan dropdown ke-2 (biasanya "Terbaru")
                terbaru_btn = page.query_selector('div[role="menu"] div[role="menuitemradio"]:nth-child(2)')
                if terbaru_btn:
                    page.evaluate("(el) => el.click()", terbaru_btn)
                    time.sleep(2)
                else:
                    print("Selector 'Terbaru' tidak ditemukan.")
            except Exception as e:
                print(f"Gagal mengatur urutan ke terbaru: {e}")

            scroll_with_arrow_keys(page, scroll_count=300)

            html = page.content()
            browser.close()
            return extract_reviews_from_page(html)

        except Exception as e:
            print(f"Error dalam scrape_google_reviews: {e}")
            if 'browser' in locals():
                browser.close()
            raise

if __name__ == "__main__":
    PLACE_REVIEW_URL = "https://maps.app.goo.gl/JAYDZXsL4wGNSYgC6?g_st=iw"
    review_data = scrape_google_reviews(PLACE_REVIEW_URL)

    df = pd.DataFrame(review_data)
    df.to_csv("google_reviews.csv", index=False)
    print(f"{len(df)} review berhasil disimpan ke google_reviews.csv")
