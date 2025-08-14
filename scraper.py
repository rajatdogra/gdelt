import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import json
import os
from asyncio import Semaphore
import nest_asyncio
from glob import glob
import datetime

# ----------------------------
# CONFIG
# ----------------------------
MAX_CONCURRENT = 200          # Max concurrent requests per file
MAX_FILES_CONCURRENT = 5     # Max files to process at the same time
TIMEOUT = 5                   # Timeout per request
SAVE_EVERY = 1000              # Save progress every N successful scrapes
SAVE_FOLDER = 'scraped_data'   # Folder to store output
MAX_URLS = 50000000            # Max URLs per file
INPUT_FOLDER = 'deduplicated_data/*'  # Accept all files
# ----------------------------

os.makedirs(SAVE_FOLDER, exist_ok=True)
nest_asyncio.apply()


async def scrape_url(session, url, date, batch_results, completed, successful, file_prefix, url_semaphore, batch_count):
    async with url_semaphore:
        try:
            async with session.get(url, timeout=TIMEOUT) as resp:
                if resp.status != 200:
                    raise Exception(f"HTTP {resp.status}")
                html = await resp.text(errors="ignore")
                soup = BeautifulSoup(html, 'lxml')

                # Try common selectors
                content_selectors = ['article', '.content', '.post-content', 'main', '.entry-content']
                content_text = ''
                for selector in content_selectors:
                    content = soup.select_one(selector)
                    if content:
                        content_text = content.get_text(strip=True)
                        break

                if not content_text:
                    body = soup.find('body')
                    content_text = body.get_text(strip=True) if body else 'No content'

                completed[0] += 1
                successful[0] += 1
                batch_results.append({'url': url, 'date': date, 'content': content_text[:5000]})

                # Save periodically
                if len(batch_results) >= SAVE_EVERY:
                    batch_count[0] += 1
                    save_path = os.path.join(SAVE_FOLDER, f"{file_prefix}_batch_{batch_count[0]}.json")
                    with open(save_path, 'w', encoding='utf-8') as f:
                        json.dump(batch_results, f, indent=2, ensure_ascii=False)
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 💾 Saved {SAVE_EVERY} results to {save_path}")
                    batch_results.clear()

                if completed[0] % 50 == 0:
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Processed {completed[0]} URLs in {file_prefix}...")

        except Exception:
            completed[0] += 1
            if completed[0] % 50 == 0:
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Processed {completed[0]} URLs in {file_prefix} (errors included)...")


async def process_file(file_path):
    file_prefix = os.path.splitext(os.path.basename(file_path))[0]
    completed = [0]
    successful = [0]
    batch_count = [0]
    batch_results = []
    url_semaphore = Semaphore(MAX_CONCURRENT)

    # Read URLs
    urls_and_dates = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            next(reader)  # Skip header
        except StopIteration:
            pass
        for i, row in enumerate(reader):
            if i >= MAX_URLS:
                break
            if len(row) >= 2:
                urls_and_dates.append((row[0], row[1]))

    print(f"\n📂 [{datetime.datetime.now().strftime('%H:%M:%S')}] Processing {file_prefix} with {len(urls_and_dates)} URLs...")

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url, date in urls_and_dates:
            tasks.append(scrape_url(session, url, date, batch_results, completed, successful, file_prefix, url_semaphore, batch_count))

        await asyncio.gather(*tasks)

    # Save remaining results
    if batch_results:
        batch_count[0] += 1
        save_path = os.path.join(SAVE_FOLDER, f"{file_prefix}_batch_{batch_count[0]}.json")
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(batch_results, f, indent=2, ensure_ascii=False)
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 💾 Saved final {len(batch_results)} results to {save_path}")

    print(f"✅ [{datetime.datetime.now().strftime('%H:%M:%S')}] Done {file_prefix}: {successful[0]} successful out of {completed[0]}")


async def main():
    files = sorted(glob(INPUT_FOLDER))
    print(f"Found {len(files)} files to process.")

    file_semaphore = Semaphore(MAX_FILES_CONCURRENT)

    async def sem_task(file):
        async with file_semaphore:
            await process_file(file)

    await asyncio.gather(*(sem_task(file) for file in files))


if __name__ == "__main__":
    asyncio.run(main())
