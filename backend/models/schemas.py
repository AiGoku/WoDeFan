from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DishOut(BaseModel):
    id: int
    name: str
    category: str
    price: float
    image_url: str
    description: str
    season_tag: str


class PaginatedDishes(BaseModel):
    items: list[DishOut]
    total: int
    limit: int
    offset: int
    has_more: bool


class OrderItemIn(BaseModel):
    dish_id: int
    added_by_openid: str


class OrderItemOut(BaseModel):
    id: int
    dish_id: int
    dish_name: str
    dish_price: float
    dish_image: str
    added_by_openid: str


class OrderCreateIn(BaseModel):
    creator_openid: str
    dish_ids: list[int]


class OrderAddDishIn(BaseModel):
    openid: str
    dish_id: int


class OrderOut(BaseModel):
    id: int
    share_code: str
    creator_openid: str
    status: str
    items: list[OrderItemOut]
    total_price: float
    created_at: str
