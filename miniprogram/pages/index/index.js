const app = getApp();
const api = require('../../utils/api');

Page({
  data: {
    categories: [],
    recommended: [],
    activeCategory: '',
    dishes: [],
    loading: true,
    cartCount: 0,
  },

  onLoad() {
    this.loadData();
  },

  onShow() {
    const cart = app.loadCart();
    this.setData({ cartCount: cart.length });
  },

  async loadData() {
    this.setData({ loading: true });
    try {
      const categories = await api.getCategories();

      const seasonMap = { 0: 'winter', 1: 'winter', 2: 'spring', 3: 'spring', 4: 'spring', 5: 'summer', 6: 'summer', 7: 'summer', 8: 'autumn', 9: 'autumn', 10: 'autumn', 11: 'winter' };
      const currentSeason = seasonMap[new Date().getMonth()];

      this.setData({
        categories: [{ key: '', name: '全部' }, ...categories],
        loading: false,
      });

      // 分批加载菜品，避免一次性加载过多导致超时
      this.loadDishesByCategory('', currentSeason);
    } catch (e) {
      console.error('加载失败', e);
      this.setData({ loading: false });
      wx.showToast({ title: '加载失败', icon: 'none' });
    }
  },

  async loadDishesByCategory(category, currentSeason) {
    try {
      const params = category ? { category } : {};
      const allDishes = await api.getAllDishes(params);

      const dishes = allDishes.map(d => ({
        ...d,
        image_url: api.resolveImageUrl(d.image_url),
      }));

      const recommended = currentSeason ? dishes.filter(d => d.season_tag === currentSeason) : [];

      this.setData({ dishes, recommended });
    } catch (e) {
      console.error('加载菜品失败', e);
    }
  },

  onCategoryTap(e) {
    const key = e.currentTarget.dataset.key;
    this.setData({ activeCategory: key });
    this.loadDishesByCategory(key);
  },

  onDishTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({ url: `/pages/detail/detail?id=${id}` });
  },

  onAddToCart(e) {
    const dish = e.currentTarget.dataset.dish;
    if (!dish || !dish.id) {
      wx.showToast({ title: '数据异常', icon: 'none' });
      return;
    }
    app.addToCart(dish);
    this.setData({ cartCount: app.globalData.cart.length });
  },

  goToCart() {
    wx.switchTab({ url: '/pages/cart/cart' });
  },

  // 转发分享
  onShareAppMessage() {
    return {
      title: '今晚吃啥？来看看我的菜单',
      path: '/pages/index/index',
    };
  },
});
