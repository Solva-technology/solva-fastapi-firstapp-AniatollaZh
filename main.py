from fastapi import FastAPI, HTTPException, Query
from typing import Optional

app = FastAPI(title="Mini Movie Catalog")

MOVIES = [
    {"id": 1, "title": "Inception", "year": 2010, "genre": "sci-fi"},
    {"id": 2, "title": "Interstellar", "year": 2014, "genre": "sci-fi"},
    {"id": 3, "title": "The Dark Knight", "year": 2008, "genre": "action"},
    {"id": 4, "title": "Tenet", "year": 2020, "genre": "thriller"},
]

@app.get("/movies")
def get_movies(
    genre: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    limit: Optional[int] = Query(None),
    sort: Optional[str] = Query(None)
):
    results = MOVIES.copy()
    if genre:
        results = [movie for movie in results if movie["genre"] == genre]
    if year:
        results = [movie for movie in results if movie["year"] == year]
    if sort:
        if sort not in results[0]:
            raise HTTPException(status_code=400, detail=f"Cannot sort by '{sort}'")
        results = sorted(results, key=lambda x: x[sort])
    if limit:
        results = results[:limit]
    return results

@app.get("/movies/{movie_id}")
def get_movie_by_id(movie_id: int):
    movie = next((m for m in MOVIES if m["id"] == movie_id), None)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
