from typing import Union

from fastapi import FastAPI, HTTPException

from fastapi.responses import FileResponse
import pandas as pd
import os
import requests

app = FastAPI()
df = pd.read_parquet('/home/michael/code/ffapi/data')

key = os.getenv('MOVIE_API_KEY')
base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"

#def get_key():
#    key = os.getenv('MOVIE_API_KEY')
#    return key

def req(movie_cd):
    url = f"{base_url}?key={key}&movieCd={movie_cd}"
    r = requests.get(url)
    code = r.status_code
    data = r.json()
    return data

def req2nationCd(movie_cd):
    data = req(movie_cd)
    nationCds = []
    nations = data.get('movieInfoResult').get('movieInfo').get('nations')
    for nation in nations:
        if nation.get('nationNm') == '한국':
            nationCode = 'K'
        else:
            nationCode = 'F'
        nationCds.append(nationCode)
    return nationCds

@app.get("/")
def read_root():
    #return FileResponse('index.html')
    return "hello"

@app.get('/sample/')
def sample():
    sdf = df.sample(n=5)
    return sdf

@app.get("/movie/{movie_cd}")
def movie_meta(movie_cd: str):
    #df = pd.read_parquet('/home/michael/code/ffapi/data')

    # df에서 movieCd == movie_cd row를 조회
    # 조회된 데이터를 .to_dict()로 만들어 아래에서 return
   
    movie_cd_df = df[df['movieCd'] == movie_cd]
    nationCodes = req2nationCd(movie_cd)

    for key, value in movie_cd_df['repNationCd'].items():
        if value is None:
            movie_cd_df['repNationCd'][key] = ','.join(nationCodes)

    if movie_cd_df.empty:
        raise HTTPException(status_code=404, detail='영화를 찾을 수 없습니다')
    dict_movie_cd = movie_cd_df.iloc[0].to_dict()
    #dict_sdf = sdf.to_dict(orient='records')

    #return {"movie_cd": movie_cd, "df_count": len(df)}
    return dict_movie_cd



