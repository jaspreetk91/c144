import pandas as pd
import csv

with open('movies.csv') as f:
  reader = csv.reader(f)
  data = list(reader)
  all_movies = data[1:]
  headers = data[0]

headers.append('poster_link')

with open('final.csv', 'a+') as f:
  csv_writer = csv.writer(f)
  csv_writer.writerow(headers)

with open('movie_links.csv') as f:
  reader = csv.reader(f)
  data = list(reader)
  allmovielinks = data[1:]

for movie_item in all_movies:
    posterfound = any(movie_item[8]in movielinkitem for movielinkitem in allmovielinks)
    if posterfound:
        for movielinkitem in allmovielinks:
            if movie_item[8]==movielinkitem[0]:
                movie_item.append(movielinkitem[1])
                if len(movie_item) == 28:
                    with open('final.csv', 'a+') as f:
                        csv_writer = csv.writer(f)
                        csv_writer.writerow(movie_item)