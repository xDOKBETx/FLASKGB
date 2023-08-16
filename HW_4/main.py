import os
import re
import time
import argparse
import requests
import aiohttp
import aiofiles
import asyncio
import concurrent.futures
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)

# Функция для создания имени папки из URL


def create_folder_from_url(url):
    parsed_url = urlparse(url)
    folder_name = parsed_url.netloc.replace('.', '_')
    return folder_name

# Функция для получения списков URL изображений с веб-страницы


def get_img_url_lists(url, parts):
    response = requests.get(url)
    img_urls = re.findall('img .*?src="(.*?)"', response.text)
    img_urls_lists = [img_urls[i * len(img_urls) // parts: (i + 1) * len(img_urls) // parts]
                      for i in range(parts)]
    return img_urls_lists

# Функция для загрузки изображений с использованием библиотеки requests (многопоточная версия)


def download_images_requests(pre_folder, img_urls):
    for img_url in img_urls:
        if 'http' in img_url:
            filename = img_url.rsplit('/', 1)[1]
            output_path = os.path.join(pre_folder, filename)
            try:
                start_time = time.time()
                response = requests.get(img_url)
                with open(output_path, "wb") as f:
                    f.write(response.content)
                download_time = time.time() - start_time
                logging.info(
                    f"Downloaded {img_url} using requests in {download_time:.2f} seconds")
            except Exception as err:
                logging.error(f"Error downloading {img_url}: {err}")

# Асинхронная функция для загрузки изображения с использованием aiohttp


async def download_image(session, img_url, output_path):
    try:
        async with session.get(img_url) as response:
            if response.status == 200:
                content = await response.read()
                async with aiofiles.open(output_path, 'wb') as f:
                    await f.write(content)
                start_time = time.time()
                download_time = time.time() - start_time
                logging.info(
                    f"Downloaded {img_url} using aiohttp in {download_time:.2f} seconds")
            else:
                logging.warning(
                    f"Failed to download {img_url} - Status code: {response.status}")
    except Exception as e:
        logging.error(f"Error downloading {img_url}: {e}")

# Функция для загрузки изображений с использованием ThreadPoolExecutor


def download_images(pre_folder, mode, img_urls):
    if mode:
        dir_name = pre_folder + '_images_thread'
    else:
        dir_name = pre_folder + '_images_process'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    for img_url in img_urls:
        if 'http' in img_url:
            filename = img_url.rsplit('/', 1)[1]
            output_path = os.path.join(dir_name, filename)
            try:
                start_time = time.time()
                response = requests.get(img_url)
                with open(output_path, "wb") as f:
                    f.write(response.content)
                download_time = time.time() - start_time
                logging.info(
                    f"Downloaded {img_url} using ThreadPoolExecutor in {download_time:.2f} seconds")
            except Exception as err:
                logging.error(f"Error downloading {img_url}: {err}")

# Функция для загрузки изображений с использованием ProcessPoolExecutor


def download_images_processes(pre_folder, img_urls):
    dir_name = pre_folder + '_images_process'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for img_url in img_urls:
            if 'http' in img_url:
                filename = img_url.rsplit('/', 1)[1]
                output_path = os.path.join(dir_name, filename)
                executor.submit(download_images, pre_folder, False, [img_url])

# Асинхронная функция для загрузки изображений с использованием aiohttp


async def download_images_async(pre_folder, img_urls, num_workers):
    dir_name = pre_folder + '_images_async'
    os.makedirs(dir_name, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for img_url in img_urls:
            if 'http' in img_url:
                filename = img_url.rsplit('/', 1)[1]
                output_path = os.path.join(dir_name, filename)
                tasks.append(download_image(session, img_url, output_path))
                print(f"Added task for {img_url}")

        if tasks:
            await asyncio.gather(*tasks)  # Ожидание выполнения всех задач

        print(f"Downloaded {len(tasks)} images using aiohttp")

# Функция для загрузки изображений с использованием ThreadPoolExecutor


def download_images_threads(pre_folder, img_urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for img_url in img_urls:
            if 'http' in img_url:
                executor.submit(download_images, pre_folder, True, [img_url])

# Основная функция для загрузки изображений


def main_download(urls, num_workers):
    parts = 5
    total_start_time = time.time()
    for url in urls:
        pre_folder = create_folder_from_url(url)
        img_urls_lists = get_img_url_lists(url, parts)
        download_images_threads(
            pre_folder, [url for urls in img_urls_lists for url in urls])
        download_images_processes(
            pre_folder, [url for urls in img_urls_lists for url in urls])
        asyncio.run(download_images_async(
            pre_folder, [url for urls in img_urls_lists for url in urls], num_workers))
    total_time = time.time() - total_start_time
    logging.info(f"Total program execution time: {total_time:.2f} seconds")

# Функция для парсинга аргументов командной строки


def parse_arguments():
    parser = argparse.ArgumentParser(description='Download images from URLs')
    parser.add_argument('url', metavar='F', type=str,
                        nargs='*', help='Please, enter URL.')
    parser.add_argument('--workers', type=int, default=5,
                        help='Number of workers for async download')
    args = parser.parse_args()
    main_download(args.url, args.workers)


if __name__ == '__main__':
    parse_arguments()

# python main.py "https://photoby.ru/"
