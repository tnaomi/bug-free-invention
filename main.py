import sys
import math

from fastapi import FastAPI
from pydantic import UUID4, BaseModel, Field

app = FastAPI(title="Testing Helper")

global args #initiate a global var to prevent looping

args = sys.argv[1:]

class PriceCheck(BaseModel):
  id: UUID4
  item_name: str | None = Field(
    default= None, title= "Item name (optional)", max_length= 50
    )
  original_price: float = Field(
    gt= 0, title= "Original Price", description= "The original price as listed on the website, before discounts."
    )
  original_discount: float = Field(
    ge=0, title= "The discount as listed on the website (the amount to be tested)."
    )
  discount_price: float | None = Field(
    gt=0, title= "The calculated discount (the amount to test).", default= None
    )
  discount: float = Field(
    gt= 0, title= "Listed discount (%)"
    )

def process_args() -> list[float]:
  try:
    result = list(map(float, args))
  except Exception as X:
    raise Exception("An error occurred while attempting to process the args", X)
  if 0 < result[0] > 100:
    raise Exception("Come on! A discount can be within 0 and 100%")
  if len(result[1:]) % 2 != 0:
    raise Exception("Prices should be paired: original and discounted")
  return result

def compare_prices() -> dict[str, str]:
  input_args = process_args()
  discount = input_args[0]/100
  prices = input_args[1:]

  original_prices = [prices[i] for i in range(0, len(prices), 2)]
  original_discounts = [prices[i+1] for i in range(0, len(prices), 2)]
  discounted_prices = list(map(lambda x: math.fma(discount,  -1*x, x), original_prices))

  result = dict(
    map(lambda x, y, z: (f"{x} and {y}", f"Match: {math.isclose(y, z)}"), 
        original_prices, original_discounts, discounted_prices)
        )

  print(result)
  return result

@app.get("/health-check")
def health_check():
  return {
    "msg": "App is healthy"
    }

@app.get("/")
async def home():
  return {
    'msg': "This is the home page."
    }

@app.post("/compare")
async def compare(): 
  return compare_prices()