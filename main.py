
import math
import uuid

from fastapi import FastAPI
from pydantic import UUID4, BaseModel, Field

app = FastAPI(title="Testing Helper")

app = FastAPI(title="Testing Helper", lifespan=lifespan)

class PriceCheck(BaseModel):
  id: UUID4 = Field(
    default= uuid.uuid4(), exclude= True 
    )
  item_name: str | None = Field(
    default= None, title= "Item name (optional)", max_length= 50
    )
  original_price: float = Field(
    gt= 0, title= "Original Price", description= "The original price as listed on the website, before discounts."
    )
  original_discount: float = Field(
    ge=0, title= "The discount as listed on the website (the amount to be tested)."
    )
  calculated_discount: float | None = Field(
    gt=0, title= "The calculated discount (the amount to test).", default= None
    )
  discount: float = Field(
    gt= 0, title= "Listed discount (%)"
    )

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

@app.post("/compare/", response_model= PriceCheck)
async def process_comparison(data: PriceCheck):
  data_dict = data.model_dump(mode='json')
  original_discount: float = data_dict["discount"]
  original_price = data_dict["original_price"]

  calculated_discount = original_price - round(math.prod([original_discount / 100, original_price]), 3)

  data_dict.update([
    ("id", uuid.uuid4()),
    ("calculated_discount", calculated_discount), 
    ("match", math.isclose(original_discount, calculated_discount))
    ])
  return data_dict