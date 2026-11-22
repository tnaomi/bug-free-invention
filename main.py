
from contextlib import asynccontextmanager
import math
import uuid
import redis.asyncio as redis
from fastapi import FastAPI
from pydantic import UUID4, BaseModel, Field
from dotenv import dotenv_values

from .constants import APP_HEALTH_CHECK, DISCOUNT_RATE_API_TITLE, HOME_CONTENT, CALC_DIS_API_TITLE, ITEM_NAME_API_TITLE, OG_DISCOUNT_API_TITLE, OG_PRICE_API_DESC, OG_PRICE_API_TITLE, APP_TITLE

config = dotenv_values(".env")

@asynccontextmanager
async def lifespan(app: FastAPI):
  """ Creates a global Redis client from a connnection pool and ties it to Fastapi's startup and teardown handling """
  global r 

  connection_url: str = config.get("REDIS_CONN_URL", "redis://127.0.0.1") # type: ignore # defaults to local host
  pool= redis.ConnectionPool.from_url(connection_url)
  r= redis.Redis(decode_responses= True).from_pool(pool)

  yield
  await r.aclose()

app = FastAPI(title=APP_TITLE, lifespan=lifespan)

class PriceCheck(BaseModel):
  id: UUID4 = Field(
    default= uuid.uuid4(), exclude= True 
    )
  item_name: str | None = Field(
    default= None, title= ITEM_NAME_API_TITLE, max_length= 50
    )
  original_price: float = Field(
    gt= 0, title= OG_PRICE_API_TITLE, description= OG_PRICE_API_DESC
    )
  original_discount: float = Field(
    ge=0, title= OG_DISCOUNT_API_TITLE
    )
  calculated_discount: float | None = Field(
    gt=0, title= CALC_DIS_API_TITLE, default= None
    )
  discount: float = Field(
    gt= 0, title= DISCOUNT_RATE_API_TITLE
    )

@app.get("/health-check")
def health_check():
  return {
    "msg": APP_HEALTH_CHECK["success"]
    }

@app.get("/")
async def home():
  return {
    "msg": HOME_CONTENT
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