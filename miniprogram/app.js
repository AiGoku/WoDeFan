App({
  globalData: {
    openid: '',
    cart: [],
  },

  onLaunch() {
    if (!wx.cloud) {
      console.error('请使用 2.2.3 或以上的基础库以使用云能力');
      return;
    }
    wx.cloud.init({
      env: 'cloud1-d8gdz5z0d911e1fb5',
      traceUser: true,
    });
    this.getOpenid();
  },

  getOpenid() {
    let openid = wx.getStorageSync('openid');
    if (!openid) {
      openid = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);
      wx.setStorageSync('openid', openid);
    }
    this.globalData.openid = openid;
  },

  loadCart() {
    const cart = wx.getStorageSync('current_cart') || [];
    this.globalData.cart = cart;
    return cart;
  },

  saveCart(cart) {
    this.globalData.cart = cart;
    wx.setStorageSync('current_cart', cart);
  },

  addToCart(dish) {
    const cart = this.globalData.cart;
    const exists = cart.find(item => item._id === dish._id);
    if (!exists) {
      cart.push({
        _id: dish._id,
        name: dish.name,
        price: dish.price,
        image_url: dish.image_url,
      });
      this.saveCart(cart);
      wx.showToast({ title: '已加入', icon: 'success' });
    } else {
      wx.showToast({ title: '已在菜单中', icon: 'none' });
    }
  },

  removeFromCart(dishId) {
    const cart = this.globalData.cart.filter(item => item._id !== dishId);
    this.saveCart(cart);
  },

  clearCart() {
    this.saveCart([]);
  },
});
