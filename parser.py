import argparse
import asyncio
import csv
import os.path
import time

from progress.bar import Bar

from loader import BASEURL, CHUNK, ClientSession, News, close_session, get_session, logger, page_number, period_in_hours


async def get_json(url: str, session: ClientSession) -> dict | None:
    async with session.get(url) as response:
        try:
            return await response.json()
        except Exception as parsing_error:
            logger.error(f'An error occurred during parsing : {str(parsing_error)}')
            return None


async def get_pages(session: ClientSession, page: int = 0, period: int = 1440) -> int:
    json = await get_json(session=session, url=BASEURL + page_number.format(page) + period_in_hours.format(period))
    total = json['metadata']['total']
    pages = total // CHUNK if total % CHUNK == 0 else total // CHUNK + 1
    logger.info(f'Fetching {total} news in {pages} steps. Please wait.')
    return pages


async def get_news_list(session: ClientSession, page: int = 0, period: int = 1440, delay: int = 0) -> list:
    url = BASEURL + page_number.format(page) + period_in_hours.format(period)
    await asyncio.sleep(delay)
    json = await get_json(session=session, url=url)
    titles = [item['title'] for item in json['items']]
    links = [BASEURL + item['link'] for item in json['items']]
    dates = [item['pubdate'] for item in json['items']]
    news_list = []
    for title, link, date in zip(titles, links, dates):
        news = News(title, link, date)
        news_list.append(news)
    return news_list


async def get_all_news_from_pages(session: ClientSession, pages: int, period: int, delay: int = 0) -> list:
    all_news = []
    with Bar(f'Work in progress', fill='■', empty_fill='=', max=pages) as bar:
        for page in range(pages):
            news_list = await get_news_list(session=session, page=page, period=period, delay=delay)
            try:
                all_news.extend(news_list)
            except Exception as fetching_error:
                logger.error(f'An error occurred during fetching news: {str(fetching_error)}')
            bar.next()
    return all_news


async def export_all_news_to_csv(all_news: list) -> None:
    timestamp = int(time.time() * 1000)
    data = argparser.parse_args()
    directory = 'exports'
    filename = f'{timestamp}_news_for_{int(data.days)}_days.csv'
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', newline='', encoding='UTF-16') as file:
        writer = csv.writer(file, dialect='excel-tab')
        writer.writerow(['Title', 'Link', 'Publish date'])
        for news in all_news:
            try:
                writer.writerow([news.title, news.link, news.pubdate])
            except Exception as writing_error:
                logger.error(f'An error occurred during csv writing: {str(writing_error)}')
    logger.info(f'All bitcoin news recorded in file: {filename}')


async def main(page: int = 0, period: int = 60, delay: int = 0):
    session = await get_session()
    try:
        pages = await get_pages(session=session, page=page, period=period)
        all_news = await get_all_news_from_pages(session=session, pages=pages, period=period, delay=delay)
        await export_all_news_to_csv(all_news)
    except Exception as script_error:
        logger.error(f'An error occurred during main script execution: {str(script_error)}')
    finally:
        await close_session()


if __name__ == '__main__':
    start_time = time.monotonic()
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--days', type=int, default=60, help='period for fetching news (days)')
    argparser.add_argument('--delay', type=int, default=0, help='add delay between requests (milliseconds)')
    try:
        args = argparser.parse_args()
    except argparse.ArgumentTypeError:
        exit(1)
    hours = int(args.days * 24)
    try:
        asyncio.run(main(period=hours, delay=args.delay))
    except Exception as error:
        logger.error(f'An error occurred during main script execution: {str(error)}')
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    logger.info(f'Script execution time: {round(elapsed_time, 2)} seconds')
