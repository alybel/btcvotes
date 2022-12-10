import random
from fastapi import FastAPI

app = FastAPI()

@app.get("/random-number")
def random_number():
    """
    create a random number
    Returns:
        _type_: _description_
    """
    return random.randint(0,100)
