// 微信API模拟
const storage = {};

const wx = {
  request: jest.fn(({ success, fail }) => {
    // 默认返回成功
    if (success) {
      success({
        statusCode: 200,
        data: { message: 'success' }
      });
    }
  }),

  getStorageSync: jest.fn((key) => {
    return storage[key] || '';
  }),

  setStorageSync: jest.fn((key, value) => {
    storage[key] = value;
  }),

  showToast: jest.fn(({ title, icon }) => {
    // 模拟显示提示
  }),

  navigateTo: jest.fn(({ url }) => {
    // 模拟页面跳转
  }),

  switchTab: jest.fn(({ url }) => {
    // 模拟Tab切换
  }),

  showShareMenu: jest.fn(({ withShareTicket }) => {
    // 模拟显示分享菜单
  }),

  // 清除所有模拟数据
  __resetMocks: () => {
    storage = {};
    jest.clearAllMocks();
  }
};

module.exports = wx;
