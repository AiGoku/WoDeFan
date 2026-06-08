// 模拟wx
global.wx = require('../__mocks__/wx');

// 保存App配置
let appConfig = null;

// 模拟App函数
global.App = jest.fn((config) => {
  appConfig = config;
  // 不调用onLaunch，因为需要手动测试
});

// 模拟getApp
global.getApp = jest.fn(() => null);

// 加载app.js
require('../app');

// 获取App配置
const app = appConfig;

describe('app.js', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    app.globalData.cart = [];
  });

  describe('onLaunch', () => {
    test('should generate openid if not exists', () => {
      wx.getStorageSync.mockReturnValue('');
      app.onLaunch();
      expect(app.globalData.openid).toMatch(/^user_\d+_[a-z0-9]{6}$/);
      expect(wx.setStorageSync).toHaveBeenCalledWith('openid', expect.any(String));
    });

    test('should use existing openid', () => {
      const existingOpenid = 'user_123_abc';
      wx.getStorageSync.mockReturnValue(existingOpenid);
      app.onLaunch();
      expect(app.globalData.openid).toBe(existingOpenid);
    });
  });

  describe('loadCart', () => {
    test('should load cart from storage', () => {
      const mockCart = [{ id: 1, name: '番茄炒蛋', price: 18 }];
      wx.getStorageSync.mockReturnValue(mockCart);

      const result = app.loadCart();
      expect(result).toEqual(mockCart);
      expect(app.globalData.cart).toEqual(mockCart);
    });

    test('should return empty array if no cart in storage', () => {
      wx.getStorageSync.mockReturnValue('');

      const result = app.loadCart();
      expect(result).toEqual([]);
      expect(app.globalData.cart).toEqual([]);
    });
  });

  describe('saveCart', () => {
    test('should save cart to storage and globalData', () => {
      const newCart = [{ id: 1, name: '番茄炒蛋', price: 18 }];

      app.saveCart(newCart);
      expect(app.globalData.cart).toEqual(newCart);
      expect(wx.setStorageSync).toHaveBeenCalledWith('current_cart', newCart);
    });
  });

  describe('addToCart', () => {
    test('should add dish when not in cart', () => {
      const dish = { id: 1, name: '番茄炒蛋', price: 18, image_url: '/img.jpg' };

      app.addToCart(dish);
      expect(app.globalData.cart).toContainEqual(dish);
      expect(wx.showToast).toHaveBeenCalledWith({ title: '已加入', icon: 'success' });
    });

    test('should not add duplicate dish', () => {
      const dish = { id: 1, name: '番茄炒蛋', price: 18, image_url: '/img.jpg' };
      app.globalData.cart = [dish];

      app.addToCart(dish);
      expect(app.globalData.cart).toHaveLength(1);
      expect(wx.showToast).toHaveBeenCalledWith({ title: '已在菜单中', icon: 'none' });
    });
  });

  describe('removeFromCart', () => {
    test('should remove dish by id', () => {
      app.globalData.cart = [
        { id: 1, name: '番茄炒蛋', price: 18 },
        { id: 2, name: '凉拌黄瓜', price: 12 }
      ];

      app.removeFromCart(1);
      expect(app.globalData.cart).toEqual([{ id: 2, name: '凉拌黄瓜', price: 12 }]);
    });

    test('should do nothing if dish not in cart', () => {
      app.globalData.cart = [
        { id: 1, name: '番茄炒蛋', price: 18 }
      ];

      app.removeFromCart(999);
      expect(app.globalData.cart).toHaveLength(1);
    });
  });

  describe('clearCart', () => {
    test('should clear all items from cart', () => {
      app.globalData.cart = [
        { id: 1, name: '番茄炒蛋', price: 18 },
        { id: 2, name: '凉拌黄瓜', price: 12 }
      ];

      app.clearCart();
      expect(app.globalData.cart).toEqual([]);
      expect(wx.setStorageSync).toHaveBeenCalledWith('current_cart', []);
    });
  });
});
