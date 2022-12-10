import random
from fastapi import FastAPI
import pickle
import os
from datetime import datetime as dt
import pandas as pd

app = FastAPI()

@app.get("/random-number")
def random_number():
    """
    create a random number
    Returns:
        _type_: _description_
    """
    return random.randint(0,100)


@app.get("/get-vote/{my_vote_for_btc_price_in_usd}")
async def get_vote(my_vote_for_btc_price_in_usd: float):
    d = get_d()
    now = dt.utcnow()
    today_date = now.date()
    d.append({'ts': now, 'date': today_date, 'px': my_vote_for_btc_price_in_usd})
    store_d(d)
    df = pd.DataFrame(d)
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
