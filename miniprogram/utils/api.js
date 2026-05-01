const app = getApp();

const BASE_URL = ''; // 部署时填写后端地址，如 http://your-server:8000

function request(url, options = {}) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${BASE_URL}${url}`,
      method: options.method || 'GET',
      data: options.data || {},
      header: { 'Content-Type': 'application/json' },
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject(new Error(res.data?.detail || '请求失败'));
        }
      },
      fail(err) {
        reject(err);
      },
    });
  });
}

// 菜品相关
function getCategories() {
  return request('/api/dishes/categories');
}

function getDishes(params = {}) {
  const query = Object.entries(params)
    .filter(([_, v]) => v)
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&');
  return request(`/api/dishes/${query ? '?' + query : ''}`);
}

function getDishById(id) {
  return request(`/api/dishes/${id}`);
}

// 订单相关
function createOrder(openid, dishIds) {
  return request('/api/orders/', {
    method: 'POST',
    data: { creator_openid: openid, dish_ids: dishIds },
  });
}

function getOrderByShareCode(shareCode) {
  return request(`/api/orders/${shareCode}`);
}

function addDishToOrder(shareCode, openid, dishId) {
  return request(`/api/orders/${shareCode}/add`, {
    method: 'POST',
    data: { openid, dish_id: dishId },
  });
}

module.exports = {
  getCategories,
  getDishes,
  getDishById,
  createOrder,
  getOrderByShareCode,
  addDishToOrder,
};
