const BASE_URL = 'http://127.0.0.1:8000/api';

function request(method, path, data) {
  return new Promise((resolve, reject) => {
    const app = getApp();
    const baseUrl = (app && app.globalData && app.globalData.baseUrl) || BASE_URL;

    wx.request({
      url: `${baseUrl}${path}`,
      method,
      data,
      header: { 'Content-Type': 'application/json' },
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject(new Error(res.data.detail || `请求失败(${res.statusCode})`));
        }
      },
      fail(err) {
        reject(err);
      },
    });
  });
}

/**
 * 将相对图片路径转为完整 URL
 * @param {string} path - 如 /static/images/fanqie_chaodan.jpg
 * @returns {string} 完整 URL
 */
function resolveImageUrl(path) {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  const app = getApp();
  const baseUrl = (app && app.globalData && app.globalData.baseUrl) || BASE_URL;
  // baseUrl 是 /api 结尾，取主机部分
  const host = baseUrl.replace(/\/api\/?$/, '');
  return `${host}${path}`;
}

function getCategories() {
  return request('GET', '/dishes/categories');
}

function getDishes(params = {}) {
  const qs = Object.entries(params)
    .filter(([, v]) => v != null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&');
  return request('GET', `/dishes/${qs ? '?' + qs : ''}`);
}

function getAllDishes(params = {}) {
  return getDishes({ ...params, limit: 100 });
}

function getDishById(id) {
  return request('GET', `/dishes/${id}`);
}

function createOrder(openid, dishIds) {
  return request('POST', '/orders/', { creator_openid: openid, dish_ids: dishIds });
}

function getOrderByShareCode(shareCode) {
  return request('GET', `/orders/${shareCode}`);
}

function addDishToOrder(shareCode, openid, dishId) {
  return request('POST', `/orders/${shareCode}/add`, { openid, dish_id: dishId });
}

module.exports = {
  getCategories,
  getDishes,
  getAllDishes,
  getDishById,
  createOrder,
  getOrderByShareCode,
  addDishToOrder,
  resolveImageUrl,
};
