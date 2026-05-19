const app = getApp();
const api = require('../../utils/api');

Page({
  data: {
    items: [],
    totalPrice: 0,
    isFromShare: false,
    shareCode: '',
    shareItems: [],
    shareTotalPrice: 0,
  },

  onLoad(options) {
    if (options.share_code) {
      this.setData({ isFromShare: true, shareCode: options.share_code });
      this.loadShareOrder(options.share_code);
    }
  },

  onShow() {
    const cart = app.loadCart();
    const totalPrice = cart.reduce((sum, item) => sum + item.price, 0);
    this.setData({ items: cart, totalPrice });
  },

  async loadShareOrder(shareCode) {
    try {
      const order = await api.getOrderByShareCode(shareCode);
      this.setData({
        shareItems: order.items,
        shareTotalPrice: order.total_price,
      });
    } catch (e) {
      wx.showToast({ title: '加载失败', icon: 'none' });
    }
  },

  onRemoveItem(e) {
    const id = e.currentTarget.dataset.id;
    app.removeFromCart(id);
    const cart = app.globalData.cart;
    const totalPrice = cart.reduce((sum, item) => sum + item.price, 0);
    this.setData({ items: cart, totalPrice });
  },

  onClearCart() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空菜单吗？',
      success: (res) => {
        if (res.confirm) {
          app.clearCart();
          this.setData({ items: [], totalPrice: 0 });
        }
      },
    });
  },

  // 创建点菜单并分享
  async onCreateAndShare() {
    const { items } = this.data;
    if (items.length === 0) {
      wx.showToast({ title: '请先选菜', icon: 'none' });
      return;
    }

    try {
      wx.showLoading({ title: '生成中...' });
      const openid = app.globalData.openid;
      const dishIds = items.map(item => item.id);
      const order = await api.createOrder(openid, dishIds);
      wx.hideLoading();

      // 保存shareCode供分享使用
      this.setData({ shareCode: order.share_code });
      wx.showToast({ title: '已生成，快分享吧' });
    } catch (e) {
      wx.hideLoading();
      wx.showToast({ title: '生成失败', icon: 'none' });
    }
  },

  goToIndex() {
    wx.switchTab({ url: '/pages/index/index' });
  },

  onShareAppMessage() {
    const { shareCode, items } = this.data;
    if (shareCode) {
      return {
        title: `我选了${items.length}道菜，来看看你想吃什么`,
        path: `/pages/share/share?share_code=${shareCode}`,
      };
    }
    return {
      title: '今晚吃啥？来看看我的菜单',
      path: '/pages/index/index',
    };
  },

  // 在分享页面追加菜品
  async onAddToShareOrder(e) {
    const dishId = e.currentTarget.dataset.id;
    const { shareCode } = this.data;
    try {
      await api.addDishToOrder(shareCode, app.globalData.openid, dishId);
      this.loadShareOrder(shareCode);
      wx.showToast({ title: '已加入' });
    } catch (e) {
      wx.showToast({ title: '操作失败', icon: 'none' });
    }
  },
});
