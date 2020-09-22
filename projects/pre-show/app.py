import os
import sys
from moviepy.editor import (VideoFileClip,
                            concatenate_videoclips)
import tmdbsimple as tmdb
from googlesearch import search as googlesearch
from download_trailers import get_trailer_file_urls

tmdb.API_KEY = "YOUR API KEY"
query = sys.argv[-1]
print("[Pre-show Generator] Movie:", query)

search = tmdb.Search()
response = search.movie(query=query)

upcoming = tmdb.Movies()
response = upcoming.upcoming()

similar_movies = []
for movie in response['results']:
    if search.results[0]['genre_ids'][0] in movie['genre_ids']:
        similar_movies.append(movie)

print('[Pre-show Generator] Which movies seem interesting?\
 Type the indexes like this: 3,4,6 \n')
for c, movie in enumerate(similar_movies):
    print(c+1, ".", movie['title'])

select_movies = input('[Pre-show Generator] Ans: ')
select_movies = [int(index)-1 for index in select_movies.split(',')]
final_movie_list = [similar_movies[index] for index in select_movies]

print('[Pre-show Generator] Searching trailers')
trailer_urls = []
for movie in final_movie_list:
    for url in googlesearch('site:trailers.apple.com ' + movie['title'], stop=10):
        break
    trailer = get_trailer_file_urls(url, "720", "single_trailer", [])[0]
    trailer_urls.append(trailer['url'])

print('[Pre-show Generator] Combining trailers')

trailer_clips = [VideoFileClip(url) for url in trailer_urls]
trailer_clips.append(VideoFileClip('turn-off.mp4').resize(0.60))
trailer_clips.append(VideoFileClip('countdown.mp4').resize(0.60))

final_clip = concatenate_videoclips(trailer_clips, method="compose")
final_clip.write_videofile("combined trailers.mp4")