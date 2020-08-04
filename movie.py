import requests
from bs4 import BeautifulSoup
import csv
import re
 
soup_objects = []

base_url = 'https://movie.naver.com/movie/running/current.nhn#'

URL = base_url 

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

soup_objects.append(soup)

for soup in soup_objects:
    movies_section = soup.select( 
        'div[id=content] > div[class=article] > div[class=obj_section] > div[class=lst_wrap] > ul[class=lst_detail_t1] > li')
    for movie in movies_section: 
        a_tag = movie.select_one('dl > dt > a')
        movie_title = a_tag.text
        movie_link = a_tag['href']
        code = movie_link[movie_link.find('code=')+5:]

        movie_data = {
            'title' : movie_title,
            'code' : code
        }
        # csv에 저장
        with open('./movie.csv', 'a', newline='') as csvfile:
            fieldnames = ['title','code']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(movie_data)
        print(movie_data)
        

