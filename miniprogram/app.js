App({
  globalData: {
    baseUrl: 'http://192.168.0.109:8000/api',
    openid: '',
    cart: [],
  },

  onLaunch() {
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
    if (!cart.find(item => item.id === dish.id)) {
      cart.push({ id: dish.id, name: dish.name, price: dish.price, image_url: dish.image_url });
      this.saveCart(cart);
      wx.showToast({ title: '已加入', icon: 'success' });
    } else {
      wx.showToast({ title: '已在菜单中', icon: 'none' });
    }
  },

  removeFromCart(dishId) {
    this.saveCart(this.globalData.cart.filter(item => item.id !== dishId));
  },

  clearCart() {
    this.saveCart([]);
  },
});
