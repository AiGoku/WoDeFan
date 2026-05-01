from fastapi import APIRouter, Depends, Query
import aiosqlite
from models.database import get_db
from models.schemas import DishOut

router = APIRouter(prefix="/dishes", tags=["菜品"])


@router.get("/", response_model=list[DishOut])
async def list_dishes(
    category: str = Query(None, description="分类筛选"),
    season: str = Query(None, description="当季推荐"),
    keyword: str = Query(None, description="搜索关键词"),
    db: aiosqlite.Connection = Depends(get_db),
):
    query = "SELECT * FROM dishes WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)
    if season:
        query += " AND season_tag = ?"
        params.append(season)
    if keyword:
        query += " AND name LIKE ?"
        params.append(f"%{keyword}%")

    query += " ORDER BY id DESC"
    cursor = await db.execute(query, params)
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


@router.get("/categories")
async def get_categories():
    return [
        {"key": "cold_dish", "name": "凉菜"},
        {"key": "hot_dish", "name": "热菜"},
        {"key": "soup", "name": "汤羹"},
        {"key": "staple", "name": "主食"},
        {"key": "dessert", "name": "甜品小吃"},
        {"key": "drink", "name": "饮品"},
    ]


@router.get("/{dish_id}", response_model=DishOut)
async def get_dish(dish_id: int, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM dishes WHERE id = ?", (dish_id,))
    row = await cursor.fetchone()
    if not row:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="菜品不存在")
    return dict(row)
