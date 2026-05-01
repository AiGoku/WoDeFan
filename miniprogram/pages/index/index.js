const app = getApp();
const api = require('../../utils/api');

Page({
  data: {
    categories: [],
    recommended: [],
    activeCategory: '',
    dishes: [],
    loading: true,
  },

  onLoad() {
    this.loadData();
  },

  onShow() {
    app.loadCart();
  },

  async loadData() {
    this.setData({ loading: true });
    try {
      const [categories, allDishes] = await Promise.all([
        api.getCategories(),
        api.getDishes(),
      ]);

      const recommended = allDishes.filter(d => d.season_tag === 'spring');

      this.setData({
        categories: [{ key: '', name: '全部' }, ...categories],
        recommended,
        dishes: allDishes,
        loading: false,
      });
    } catch (e) {
      console.error('加载失败', e);
      this.setData({ loading: false });
      wx.showToast({ title: '加载失败', icon: 'none' });
    }
  },

  onCategoryTap(e) {
    const key = e.currentTarget.dataset.key;
    this.setData({ activeCategory: key });
    if (key) {
      api.getDishes({ category: key }).then(dishes => {
        this.setData({ dishes });
      });
    } else {
      api.getDishes().then(dishes => {
        this.setData({ dishes });
      });
    }
  },

  onDishTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({ url: `/pages/detail/detail?id=${id}` });
  },

  onAddToCart(e) {
    const dish = e.currentTarget.dataset.dish;
    app.addToCart(dish);
  },

  // 转发分享
  onShareAppMessage() {
    return {
      title: '今晚吃啥？来看看我的菜单',
      path: '/pages/index/index',
    };
  },
});
