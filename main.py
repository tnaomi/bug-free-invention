
from fastapi import FastAPI
from pydantic import UUID4, BaseModel, Field

app = FastAPI(title="Testing Helper")

app = FastAPI(title="Testing Helper", lifespan=lifespan)

class PriceCheck(BaseModel):
  id: UUID4 | None
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