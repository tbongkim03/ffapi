from typing import Union

from fastapi import FastAPI, HTTPException

from fastapi.responses import FileResponse
import pandas as pd

app = FastAPI()
df = pd.read_parquet('/home/michael/code/ffapi/data')

#@app.get("/")
#def read_root():
#    return {"Hello": "World"}

@app.get("/")
def read_root():
    return FileResponse('index.html')

@app.get('/sample/')
def sample():
    sdf = df.sample(n=5)
    return sdf

@app.get("/movie/{movie_cd}")
def movie_meta(movie_cd: str):
    #df = pd.read_parquet('/home/michael/code/ffapi/data')

    # df에서 movieCd == movie_cd row를 조회
    # 조회된 데이터를 .to_dict()로 만들어 아래에서 return
    sdf = df.sample(n=5)
    
    movie_cd_df = df[df['movieCd'] == movie_cd]
    if movie_cd_df.empty:
        raise HTTPException(status_code=404, detail='영화를 찾을 수 없습니다')
    dict_movie_cd = movie_cd_df.iloc[0].to_dict()
    #dict_sdf = sdf.to_dict(orient='records')

    #return {"movie_cd": movie_cd, "df_count": len(df)}
    return dict_movie_cd
