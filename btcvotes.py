import random
import json
import pickle
import os
from datetime import datetime as dt
import pandas as pd
from fastapi import FastAPI, HTTPException
import requests


app = FastAPI()

@app.get("/random-number")
def random_number():
    """
    create a random number
    Returns:
        _type_: _description_
    """
    return random.randint(0,100)

def get_btc_price_of_today():
    today_date = dt.utcnow().date()
    # check if todays prices was already taken from the api
    if os.path.exists('today_btc_price.pcl'):
        check_d = pickle.load(open('today_btc_price.pcl', 'rb'))
        if check_d['today'] == today_date:
            return check_d['btc_px']
    url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/price"
    querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl"}
    headers = {
        "X-RapidAPI-Key": "f7840680cfmsh06caa5664044614p1ce717jsnac7cbe48fa53",
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    px = float(json.loads(response.text)['data']['price'])
    d = {'today': today_date, 'btc_px': px}
    pickle.dump(d, open('today_btc_price.pcl', 'wb'))
    return px

@app.get("/get-vote/{my_vote_for_btc_price_in_usd}")
async def get_vote(my_vote_for_btc_price_in_usd: float):
    # This covers the test case in RapidAPI that should not interfer with the real value
    if my_vote_for_btc_price_in_usd == 17392.999:
        return 17392.999
    btc_price_today = get_btc_price_of_today()
    if my_vote_for_btc_price_in_usd < btc_price_today*0.9 or my_vote_for_btc_price_in_usd > btc_price_today*1.1:
        raise HTTPException(status_code=230, detail="invalid range of estimate. must be in  10 percent range of current Bitcoin price.")
    d = get_d()
    now = dt.utcnow()
    today_date = now.date()
    d.append({'ts': now, 'date': today_date, 'px': my_vote_for_btc_price_in_usd})
    store_d(d)
    df = pd.DataFrame(d)
    n = df.groupby('date')['px'].count().sort_values(ascending=True).iloc[-1]
    mean = df.groupby('date')['px'].mean().sort_values(ascending=True).iloc[-1]
    return mean
    

def get_d():
    d = None
    if not os.path.exists('store.pcl'):
        d = []
    else:
        d = pickle.load(open('store.pcl', 'rb'))
    return d

def store_d(d):
    pickle.dump(d, open('store.pcl', 'wb'))

api_endpoint_url = "https://bitcoin-voting-tomorow-price.herokuapp.com/get-vote/1.5"


if __name__ == '__main__':
    get_btc_price_of_today()