const app = getApp();
const api = require('../../utils/api');

Page({
  data: {
    order: null,
    loading: true,
    showAddPanel: false,
    categories: [],
    dishes: [],
    activeCategory: '',
  },

  onLoad(options) {
    if (options.share_code) {
      this.loadOrder(options.share_code);
    }
  },

  async loadOrder(shareCode) {
    try {
      const order = await api.getOrderByShareCode(shareCode);
      this.setData({ order, loading: false });
    } catch (e) {
      this.setData({ loading: false });
      wx.showToast({ title: '菜单不存在或已失效', icon: 'none' });
    }
  },

  // 打开选菜面板
  async onOpenAddPanel() {
    if (this.data.categories.length === 0) {
      const [categories, dishes] = await Promise.all([
        api.getCategories(),
        api.getDishes(),
      ]);
      this.setData({ categories: [{ key: '', name: '全部' }, ...categories], dishes });
    }
    this.setData({ showAddPanel: true });
  },

  onClosePanel() {
    this.setData({ showAddPanel: false });
  },

  onCategoryTap(e) {
    const key = e.currentTarget.dataset.key;
    this.setData({ activeCategory: key });
    if (key) {
      api.getDishes({ category: key }).then(dishes => this.setData({ dishes }));
    } else {
      api.getDishes().then(dishes => this.setData({ dishes }));
    }
  },

  // 追加菜品到点菜单
  async onAddDish(e) {
    const dish = e.currentTarget.dataset.dish;
    const { order } = this.data;
    try {
      await api.addDishToOrder(order.share_code, app.globalData.openid, dish._id);
      wx.showToast({ title: '已加入' });
      this.loadOrder(order.share_code);
    } catch (e) {
      wx.showToast({ title: '操作失败', icon: 'none' });
    }
  },

  // 再次分享给其他人
  onShareAppMessage() {
    const { order } = this.data;
    return {
      title: `一起来点菜！已选${order.items.length}道`,
      path: `/pages/share/share?share_code=${order.share_code}`,
    };
  },
});
