import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

DELAY_RANGE = (2.5, 4)
BASE_URL = "https://vedabase.io/en/library/bg"

tag_class = input("Translation Class name (e.g., 'translation'): ").strip()
verset_class = input("Verse Sanskrit Class name: ").strip()

def scrape_verse(chapter, verse_ref, verset_class, tag_class):
    """Scrape a single verse or verse range"""
    url = f"{BASE_URL}/{chapter}/{verse_ref}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            translation_element = soup.find("div", class_=tag_class)
            verse_sans = soup.find("div", class_=verset_class)

            if verse_sans:
                for br in verse_sans.find_all('br'):
                    br.replace_with('\n')

            if translation_element and verse_sans:
                return {
                    "Verse": f"{chapter}/{verse_ref}",
                    "Verse_sans": verse_sans.get_text(strip=True),
                    "Translation": translation_element.get_text(strip=True),
                    "Link": url
                }
        return None
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

def scrape_gita_verses(chapter, total_verses):
    translations = []
    verse = 1

    while verse <= total_verses:
        verse_data = scrape_verse(chapter, verse, verset_class, tag_class)

        if verse_data is not None:
            translations.append(verse_data)
            print(f"✅ Scraped: Chapter {chapter}, Verse {verse}")
            verse += 1
        else:
            verse_range_data = None
            for range_size in [2, 3, 4, 5]:
                if verse + range_size - 1 > total_verses:
                    continue
                verse_ref = f"{verse}-{verse + range_size - 1}"
                verse_range_data = scrape_verse(chapter, verse_ref, verset_class, tag_class)
                if verse_range_data is not None:
                    translations.append(verse_range_data)
                    print(f"✅ Scraped: Chapter {chapter}, Verses {verse_ref}")
                    verse += range_size
                    break

            if verse_range_data is None:
                print(f"❌ Failed to scrape: Chapter {chapter}, Verse {verse}")
                verse += 1

        time.sleep(random.uniform(*DELAY_RANGE))

    return translations

def save_to_csv(data, filename="gita_translations.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"\n✅ Data saved to {filename}")

if __name__ == "__main__":
    verse_counts = [46, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78]
    all_translations = []

    for chapter in range(1, 19):
        total_verses = verse_counts[chapter - 1]
        print(f"\n📖 Scraping Chapter {chapter} (total verses: {total_verses})...")
        translations = scrape_gita_verses(chapter, total_verses)
        all_translations.extend(translations)
        print(f"Chapter {chapter} done. Scraped {len(translations)} entries.")

    save_to_csv(all_translations, "gita_translations_all_with_sans.csv")
