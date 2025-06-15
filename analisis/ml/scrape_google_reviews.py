from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time


def scroll_with_arrow_keys(page, scroll_count=50):
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


def scrape_google_reviews(map_url, scroll_times=15):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(locale='id-ID')  # paksa Bahasa Indonesia
        page = context.new_page()
        page.goto(map_url)
        page.wait_for_timeout(5000)

        # Klik tombol "Ulasan" / "All reviews"
        try:
            page.click('text="Ulasan"')
            time.sleep(3)
        except:
            pass

        # Klik "Urutkan" → "Terbaru"
        try:
            page.click('text="Urutkan"')  # atau 'Sort by' jika English
            time.sleep(1)

            # Ambil elemen berdasarkan urutan dropdown ke-2 (biasanya "Terbaru")
            terbaru_btn = page.query_selector('div[role="menu"] div[role="menuitemradio"]:nth-child(2)')
            if terbaru_btn:
                page.evaluate("(el) => el.click()", terbaru_btn)
                time.sleep(2)
            else:
                print("Selector 'Terbaru' tidak ditemukan.")
        except Exception as e:
            print("Gagal mengatur urutan ke terbaru:", e)

       
        scroll_with_arrow_keys(page, scroll_count=100)

        html = page.content()
        browser.close()

    return extract_reviews_from_page(html)



if __name__ == "__main__":
    PLACE_REVIEW_URL = "https://maps.app.goo.gl/JAYDZXsL4wGNSYgC6?g_st=iw"
    review_data = scrape_google_reviews(PLACE_REVIEW_URL)

    df = pd.DataFrame(review_data)
    df.to_csv("google_reviews.csv", index=False)
    print(f"{len(df)} review berhasil disimpan ke google_reviews.csv")
