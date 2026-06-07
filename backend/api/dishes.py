from fastapi import APIRouter, Depends, Query
import aiosqlite
from models.database import get_db
from models.schemas import DishOut, PaginatedDishes

router = APIRouter(prefix="/dishes", tags=["菜品"])


@router.get("/", response_model=PaginatedDishes)
async def list_dishes(
    category: str = Query(None, description="分类筛选"),
    season: str = Query(None, description="当季推荐"),
    keyword: str = Query(None, description="搜索关键词"),
    limit: int = Query(10, description="每页数量", ge=1, le=100),
    offset: int = Query(0, description="偏移量", ge=0),
    db: aiosqlite.Connection = Depends(get_db),
):
    # 构建筛选条件
    where = "WHERE 1=1"
    params = []

    if category:
        where += " AND category = ?"
        params.append(category)
    if season:
        where += " AND season_tag = ?"
        params.append(season)
    if keyword:
        where += " AND name LIKE ?"
        params.append(f"%{keyword}%")

    # 查询总数
    count_cursor = await db.execute(f"SELECT COUNT(*) FROM dishes {where}", params)
    total = (await count_cursor.fetchone())[0]

    # 查询当前页数据
    data_cursor = await db.execute(
        f"SELECT * FROM dishes {where} ORDER BY id DESC LIMIT ? OFFSET ?",
        params + [limit, offset],
    )
    rows = await data_cursor.fetchall()

    return PaginatedDishes(
        items=[dict(row) for row in rows],
        total=total,
        limit=limit,
        offset=offset,
        has_more=offset + limit < total,
    )


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
