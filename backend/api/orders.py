import uuid
from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
from models.database import get_db
from models.schemas import OrderCreateIn, OrderAddDishIn, OrderOut, OrderItemOut

router = APIRouter(prefix="/orders", tags=["点菜单"])


def generate_share_code() -> str:
    return uuid.uuid4().hex[:8]


@router.post("/", response_model=OrderOut)
async def create_order(data: OrderCreateIn, db: aiosqlite.Connection = Depends(get_db)):
    share_code = generate_share_code()

    cursor = await db.execute(
        "INSERT INTO orders (share_code, creator_openid) VALUES (?, ?)",
        (share_code, data.creator_openid),
    )
    order_id = cursor.lastrowid

    for dish_id in data.dish_ids:
        dish_cursor = await db.execute("SELECT * FROM dishes WHERE id = ?", (dish_id,))
        dish = await dish_cursor.fetchone()
        if not dish:
            continue
        await db.execute(
            "INSERT INTO order_items (order_id, dish_id, dish_name, dish_price, dish_image, added_by_openid) VALUES (?, ?, ?, ?, ?, ?)",
            (order_id, dish["id"], dish["name"], dish["price"], dish["image_url"], data.creator_openid),
        )

    await db.commit()
    return await _build_order_response(order_id, db)


@router.get("/{share_code}", response_model=OrderOut)
async def get_order(share_code: str, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT id FROM orders WHERE share_code = ?", (share_code,))
    order = await cursor.fetchone()
    if not order:
        raise HTTPException(status_code=404, detail="点菜单不存在")
    return await _build_order_response(order["id"], db)


@router.post("/{share_code}/add", response_model=OrderOut)
async def add_dish_to_order(
    share_code: str, data: OrderAddDishIn, db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute("SELECT * FROM orders WHERE share_code = ?", (share_code,))
    order = await cursor.fetchone()
    if not order:
        raise HTTPException(status_code=404, detail="点菜单不存在")
    if order["status"] != "active":
        raise HTTPException(status_code=400, detail="该点菜单已关闭")

    dish_cursor = await db.execute("SELECT * FROM dishes WHERE id = ?", (data.dish_id,))
    dish = await dish_cursor.fetchone()
    if not dish:
        raise HTTPException(status_code=404, detail="菜品不存在")

    await db.execute(
        "INSERT INTO order_items (order_id, dish_id, dish_name, dish_price, dish_image, added_by_openid) VALUES (?, ?, ?, ?, ?, ?)",
        (order["id"], dish["id"], dish["name"], dish["price"], dish["image_url"], data.openid),
    )
    await db.execute(
        "UPDATE orders SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (order["id"],)
    )
    await db.commit()
    return await _build_order_response(order["id"], db)


@router.delete("/{share_code}/items/{item_id}")
async def remove_item(
    share_code: str, item_id: int, db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute("SELECT id FROM orders WHERE share_code = ?", (share_code,))
    order = await cursor.fetchone()
    if not order:
        raise HTTPException(status_code=404, detail="点菜单不存在")

    await db.execute(
        "DELETE FROM order_items WHERE id = ? AND order_id = ?", (item_id, order["id"])
    )
    await db.commit()
    return {"message": "已移除"}


async def _build_order_response(order_id: int, db: aiosqlite.Connection) -> OrderOut:
    cursor = await db.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = await cursor.fetchone()

    items_cursor = await db.execute(
        "SELECT * FROM order_items WHERE order_id = ?", (order_id,)
    )
    items_rows = await items_cursor.fetchall()
    items = [OrderItemOut(**dict(row)) for row in items_rows]
    total = sum(item.dish_price for item in items)

    return OrderOut(
        id=order["id"],
        share_code=order["share_code"],
        creator_openid=order["creator_openid"],
        status=order["status"],
        items=items,
        total_price=total,
        created_at=str(order["created_at"]),
    )
