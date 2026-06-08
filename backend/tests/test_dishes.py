import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_list_dishes(client: AsyncClient):
    """测试获取菜品列表"""
    response = await client.get("/api/dishes/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert "has_more" in data
    assert len(data["items"]) > 0

async def test_list_dishes_by_category(client: AsyncClient):
    """测试按分类筛选菜品"""
    response = await client.get("/api/dishes/?category=hot_dish")
    assert response.status_code == 200
    data = response.json()
    for dish in data["items"]:
        assert dish["category"] == "hot_dish"

async def test_list_dishes_by_season(client: AsyncClient):
    """测试按季节筛选菜品"""
    response = await client.get("/api/dishes/?season=summer")
    assert response.status_code == 200
    data = response.json()
    for dish in data["items"]:
        assert dish["season_tag"] == "summer"

async def test_list_dishes_by_keyword(client: AsyncClient):
    """测试关键词搜索菜品"""
    response = await client.get("/api/dishes/?keyword=番茄")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0
    assert "番茄" in data["items"][0]["name"]

async def test_list_dishes_pagination(client: AsyncClient):
    """测试分页功能"""
    response = await client.get("/api/dishes/?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 2
    assert data["limit"] == 2
    assert data["offset"] == 0

async def test_list_dishes_empty_offset(client: AsyncClient):
    """测试偏移量超出范围"""
    response = await client.get("/api/dishes/?limit=2&offset=100")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0
    assert data["has_more"] == False

async def test_get_categories(client: AsyncClient):
    """测试获取分类列表"""
    response = await client.get("/api/dishes/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6
    categories = [cat["key"] for cat in data]
    assert "cold_dish" in categories
    assert "hot_dish" in categories
    assert "soup" in categories
    assert "staple" in categories
    assert "dessert" in categories
    assert "drink" in categories

async def test_get_dish(client: AsyncClient):
    """测试获取单个菜品"""
    response = await client.get("/api/dishes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "category" in data
    assert "price" in data

async def test_get_dish_not_found(client: AsyncClient):
    """测试获取不存在的菜品"""
    response = await client.get("/api/dishes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "菜品不存在"

async def test_list_dishes_invalid_limit_zero(client: AsyncClient):
    """测试limit=0的边界情况"""
    response = await client.get("/api/dishes/?limit=0")
    assert response.status_code == 422  # Validation Error

async def test_list_dishes_invalid_limit_over_100(client: AsyncClient):
    """测试limit超过100的边界情况"""
    response = await client.get("/api/dishes/?limit=101")
    assert response.status_code == 422  # Validation Error
