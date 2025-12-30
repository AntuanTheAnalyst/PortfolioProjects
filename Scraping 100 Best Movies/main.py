from bs4 import BeautifulSoup
import requests

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"
response = requests.get(URL)
movie_webpage = response.content.decode("utf-8")
soup = BeautifulSoup(movie_webpage, "html.parser")

movie_titles = soup.find_all(name="h3", class_="title")
# print(movie_titles)
best_movie_titles = [movie_title.getText() for movie_title in movie_titles]
best_movie_titles.reverse()
print(best_movie_titles)

with open("movies.txt", "w", encoding="utf-8") as file:
    for movie_title in best_movie_titles:
        file.write(f"{movie_title}\n")


