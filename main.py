import asyncio
import aiohttp
import os
from google.cloud import firestore
from google.cloud import storage
import logging

API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BASE_URL", f"http://www.omdbapi.com/?apikey=")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "movies_ombd")
FILE_PATH = os.environ.get("FILE_PATH", "100_movies_titles")
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


def read_titles_from_gcs(bucket_name, file_path):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        data = blob.download_as_text()
        titles = data.splitlines()
        return titles
    except Exception as e:
        logging.error(f"Error reading titles from GCS: {e}")
        return []


def entry_point(event, context):
    try:
        movie_titles = read_titles_from_gcs(BUCKET_NAME, FILE_PATH)

        movies_data = asyncio.run(fetch_movies_data(movie_titles))

        db = firestore.Client()
        for movie in movies_data:
            if movie.get('Response') == 'True':
                doc_ref = db.collection('movies').document(movie['imdbID'])
                doc_ref.set(movie)

        logging.info('Movies data fetched and stored successfully.')
    except Exception as e:
        logging.error(f"An error occurred during the Cloud Function execution: {e}")
