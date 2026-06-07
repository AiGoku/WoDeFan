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
    try {
      const categories = await api.getCategories();
      const seasonMap = { 0: 'winter', 1: 'winter', 2: 'spring', 3: 'spring', 4: 'spring', 5: 'summer', 6: 'summer', 7: 'summer', 8: 'autumn', 9: 'autumn', 10: 'autumn', 11: 'winter' };
      const currentSeason = seasonMap[new Date().getMonth()];

      this.setData({
        categories: [{ key: '', name: '全部' }, ...categories],
      });

      const recRes = await api.getDishes({ season: currentSeason, limit: 6 });
      this.setData({
        recommended: recRes.items.map(d => ({ ...d, image_url: api.resolveImageUrl(d.image_url) })),
      });

      this.loadDishesByCategory('');
    } catch (e) {
      console.error('加载失败', e);
      this.setData({ loading: false });
    }
  },

  async loadDishesByCategory(category) {
    this.setData({ loading: true, dishes: [] });
    try {
      const params = category ? { category, limit: 10 } : { limit: 10 };
      const res = await api.getDishes(params);
      const dishes = res.items.map(d => ({
        id: d.id,
        name: d.name,
        price: d.price,
        image_url: api.resolveImageUrl(d.image_url),
        description: d.description,
      }));
      this.setData({ dishes, loading: false, hasMore: res.has_more });
    } catch (e) {
      console.error('加载菜品失败', e);
      this.setData({ loading: false });
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
    if (!dish || !dish.id) return;
    app.addToCart(dish);
    this.setData({ cartCount: app.globalData.cart.length });
  },

  goToCart() {
    wx.switchTab({ url: '/pages/cart/cart' });
  },

  onShareAppMessage() {
    return { title: '今晚吃啥？来看看我的菜单', path: '/pages/index/index' };
  },
});
