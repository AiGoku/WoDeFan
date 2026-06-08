import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_create_order(client: AsyncClient):
    """测试创建点菜单"""
    response = await client.post("/api/orders/", json={
        "creator_openid": "test_user_1",
        "dish_ids": [1, 2]
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "share_code" in data
    assert len(data["share_code"]) == 8
    assert data["creator_openid"] == "test_user_1"
    assert data["status"] == "active"
    assert len(data["items"]) == 2
    assert data["total_price"] > 0

async def test_create_order_empty_dishes(client: AsyncClient):
    """测试创建空点菜单"""
    response = await client.post("/api/orders/", json={
        "creator_openid": "test_user_2",
        "dish_ids": []
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0
    assert data["total_price"] == 0

async def test_create_order_invalid_dishes(client: AsyncClient):
    """测试创建点菜单时包含无效菜品ID"""
    response = await client.post("/api/orders/", json={
        "creator_openid": "test_user_3",
        "dish_ids": [1, 999]  # 999不存在
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1  # 只有有效的菜品被添加

async def test_get_order(client: AsyncClient):
    """测试获取点菜单"""
    # 先创建一个点菜单
    create_response = await client.post("/api/orders/", json={
        "creator_openid": "test_user_4",
        "dish_ids": [1]
    })
    share_code = create_response.json()["share_code"]

    # 获取点菜单
    response = await client.get(f"/api/orders/{share_code}")
    assert response.status_code == 200
    data = response.json()
    assert data["share_code"] == share_code
    assert len(data["items"]) == 1

async def test_get_order_not_found(client: AsyncClient):
    """测试获取不存在的点菜单"""
    response = await client.get("/api/orders/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "点菜单不存在"

async def test_add_dish_to_order(client: AsyncClient):
    """测试向点菜单添加菜品"""
    # 先创建一个点菜单
    create_response = await client.post("/api/orders/", json={
        "creator_openid": "test_user_5",
        "dish_ids": [1]
    })
    share_code = create_response.json()["share_code"]

    # 添加菜品
    response = await client.post(f"/api/orders/{share_code}/add", json={
        "dish_id": 2,
        "openid": "test_user_6"
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2

async def test_add_dish_to_order_not_found(client: AsyncClient):
    """测试向不存在的点菜单添加菜品"""
    response = await client.post("/api/orders/nonexistent/add", json={
        "dish_id": 1,
        "openid": "test_user_7"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "点菜单不存在"

async def test_add_dish_to_order_invalid_dish(client: AsyncClient):
    """测试向点菜单添加不存在的菜品"""
    # 先创建一个点菜单
    create_response = await client.post("/api/orders/", json={
        "creator_openid": "test_user_8",
        "dish_ids": [1]
    })
    share_code = create_response.json()["share_code"]

    # 添加不存在的菜品
    response = await client.post(f"/api/orders/{share_code}/add", json={
        "dish_id": 999,
        "openid": "test_user_9"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "菜品不存在"

async def test_remove_item_from_order(client: AsyncClient):
    """测试从点菜单移除菜品"""
    # 先创建一个点菜单
    create_response = await client.post("/api/orders/", json={
        "creator_openid": "test_user_10",
        "dish_ids": [1, 2]
    })
    data = create_response.json()
    share_code = data["share_code"]
    item_id = data["items"][0]["id"]

    # 移除菜品
    response = await client.delete(f"/api/orders/{share_code}/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "已移除"

    # 验证菜品已被移除
    get_response = await client.get(f"/api/orders/{share_code}")
    assert len(get_response.json()["items"]) == 1

async def test_remove_item_from_order_not_found(client: AsyncClient):
    """测试从不存在的点菜单移除菜品"""
    response = await client.delete("/api/orders/nonexistent/items/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "点菜单不存在"

async def test_generate_share_code():
    """测试分享码生成"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from api.orders import generate_share_code
    codes = set()
    for _ in range(1000):
        code = generate_share_code()
        assert len(code) == 8
        assert all(c in '0123456789abcdef' for c in code)
        codes.add(code)
    # 检查唯一性（1000次生成应该都是唯一的）
    assert len(codes) == 1000
