import os
import asyncio
import logging
import json

import aiohttp

from data import titles

# CODE USED FOR LOCAL TESTS

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL', 'http://www.omdbapi.com/')
URL = f"{BASE_URL}?apikey={API_KEY}"


async def get_movie_data(async_session, title):
    url = f"{URL}&t={title}"
    try:
        async with async_session.get(url) as response:
            movie_data = await response.json()
            return movie_data
    except Exception as e:
        logging.error(f"Error fetching data for {title}: {e}")
        return None


async def fetch_movies_data(movie_titles):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(get_movie_data(session, title)) for title in movie_titles]
        movies_data = await asyncio.gather(*tasks, return_exceptions=True)
        return movies_data


def save_movies_to_json(movies_data, filename="movies_data.json"):
    valid_movies = [movie for movie in movies_data if movie and movie.get('Response') == 'True']
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(valid_movies, f, ensure_ascii=False, indent=4)


def main(lista_filmes):
    try:
        movie_titles = lista_filmes
        movies_data = asyncio.run(fetch_movies_data(movie_titles))

        print(f"How much movies? {len(movies_data)}")

        save_movies_to_json(movies_data)
    except Exception as e:
        print(f"An error occurred during execution: {e}")


if __name__ == "__main__":
    lista_filmes = titles
    main(lista_filmes)

