const app = getApp();
const api = require('../../utils/api');

Page({
  data: {
    dish: null,
    inCart: false,
  },

  onLoad(options) {
    if (options.id) {
      this.loadDish(options.id);
    }
  },

  async loadDish(id) {
    try {
      const dish = await api.getDishById(id);
      dish.image_url = api.resolveImageUrl(dish.image_url);
      const inCart = app.globalData.cart.some(item => item.id === dish.id);
      this.setData({ dish, inCart });
    } catch (e) {
      wx.showToast({ title: '加载失败', icon: 'none' });
    }
  },

  onAddToCart() {
    const { dish, inCart } = this.data;
    if (inCart) {
      app.removeFromCart(dish.id);
      this.setData({ inCart: false });
      wx.showToast({ title: '已移除', icon: 'none' });
    } else {
      app.addToCart(dish);
      this.setData({ inCart: true });
    }
  },

  onShareAppMessage() {
    const { dish } = this.data;
    return {
      title: `推荐一道菜：${dish.name}`,
      path: `/pages/detail/detail?id=${dish.id}`,
    };
  },
});
