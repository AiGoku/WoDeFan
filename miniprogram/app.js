App({
  globalData: {
    baseUrl: '', // 后端API地址，部署时填写
    openid: '',
    cart: [], // 当前选菜列表
  },

  onLaunch() {
    this.getOpenid();
  },

  getOpenid() {
    // 通过云函数或后端接口获取openid
    // 这里先用本地生成的临时ID
    let openid = wx.getStorageSync('openid');
    if (!openid) {
      openid = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);
      wx.setStorageSync('openid', openid);
    }
    this.globalData.openid = openid;
  },

  // 从本地缓存恢复购物车
  loadCart() {
    const cart = wx.getStorageSync('current_cart') || [];
    this.globalData.cart = cart;
    return cart;
  },

  // 保存购物车到本地
  saveCart(cart) {
    this.globalData.cart = cart;
    wx.setStorageSync('current_cart', cart);
  },

  // 添加菜品到购物车
  addToCart(dish) {
    const cart = this.globalData.cart;
    const exists = cart.find(item => item.id === dish.id);
    if (!exists) {
      cart.push({
        id: dish.id,
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

  // 从购物车移除
  removeFromCart(dishId) {
    const cart = this.globalData.cart.filter(item => item.id !== dishId);
    this.saveCart(cart);
  },

  // 清空购物车
  clearCart() {
    this.saveCart([]);
  },
});
