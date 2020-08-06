import requests
from bs4 import BeautifulSoup
import csv
 
base_url = 'https://movie.naver.com/movie/running/current.nhn#'

URL = base_url 

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

final_movie_data = []
movies_section = soup.select( 
    '#content > .article > .obj_section > .lst_wrap > ul > li')

for movie in movies_section: 

    a_tag = movie.select_one('dl > dt > a')

    movie_title = a_tag.contents[0] # 배열에 저장되므로 
    code = a_tag['href'].split("code=")[1]
    # code = movie_code[movie_code.find('code=')+len('code='):]

    movie_data = {
        'title' : movie_title,
        'code' : code
    }
    final_movie_data.append(movie_data)
    # csv에 저장
    # with open('./movie.csv', 'a', newline='') as csvfile:
    #     fieldnames = ['title','code']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writerow(movie_data)
# print(final_movie_data)

for movie in final_movie_data:
    movie_code = movie['code']

    # headers 없어도 됨
    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )
    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', params=params)
    # print("status code :", response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')    
    # movie_code = movie['code']
    # REVIEW_URL = f'https://movie.naver.com/movie/bi/mi/point.nhn?code={movie_code}'
    # response = requests.get(REVIEW_URL)
    # soup = BeautifulSoup(response.text, 'html.parser')

    print(movie_code,"=============")
    review_section = soup.select('body > div > div > div.score_result > ul > li')
    i=0
    for review in review_section:
        reple_tag = review.select_one(f'div.score_reple > p > span#_filtered_ment_{i}')
        spo_tag = review.select_one(f'div.score_reple > p > span#_text_spo_{i}')
        unfold = review.select_one(f'div.score_reple > p > span#_filtered_ment_{i} > span#_unfold_ment{i} > a')
        em_tag = review.select_one('div.star_score > em')

        review_content = reple_tag.text.strip()
        star_score = em_tag.text
        
        if spo_tag is not None: # 스포일러가 포함된 감상평
            print(star_score, spo_tag.text)
        else:
            if unfold is not None: 
                print(star_score, unfold.get('data-src'))
                # print(star_score, unfold['data-src'])
            else:
                print(star_score, review_content)
        i+=1
    