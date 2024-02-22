# Movies Data Import Cloud Function

This Cloud Function is designed to automate the process of requesting movies data for the OMDB API and storing it in Google Cloud Firestore. It reads a list of movie titles from a file stored in Google Cloud Storage (GCS).

## Environment Variables

The function uses the following environment variables:

- `API_KEY`: OMDB API key.
- `BASE_URL`: The base URL of the OMDB API. Defaults to `http://www.omdbapi.com/?apikey=`.
- `BUCKET_NAME`: The name of the GCS bucket where the file with movie titles is stored. Defaults to `movies_ombd`.
- `FILE_PATH`: The path to the file within the GCS bucket. Defaults to `100_movies_titles.csv`.

## How It Works

1. First the function is triggered by a pub/sub message.
2. Then the function reads the list of movie titles from a specified file in a GCS bucket.
3. It then uses `aiohttp` to asynchronously fetch data for each movie title from the OMDB API.
4. The movie data is then stored in Firestore under a collection named `movies`, with each document named by its `imdbID`.



