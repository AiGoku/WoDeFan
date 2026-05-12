function callFunction(name, data = {}) {
  return new Promise((resolve, reject) => {
    wx.cloud.callFunction({
      name,
      data,
      success(res) {
        const result = res.result;
        if (result.success) {
          resolve(result.data);
        } else {
          reject(new Error(result.error || '请求失败'));
        }
      },
      fail(err) {
        reject(err);
      },
    });
  });
}

function getCategories() {
  return callFunction('getCategories');
}

function getDishes(params = {}) {
  return callFunction('getDishes', params);
}

function getDishById(id) {
  return callFunction('getDishById', { id });
}

function createOrder(openid, dishIds) {
  return callFunction('createOrder', { dish_ids: dishIds });
}

function getOrderByShareCode(shareCode) {
  return callFunction('getOrder', { share_code: shareCode });
}

function addDishToOrder(shareCode, openid, dishId) {
  return callFunction('addDishToOrder', {
    share_code: shareCode,
    dish_id: dishId,
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
