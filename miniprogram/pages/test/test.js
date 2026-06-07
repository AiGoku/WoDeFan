Page({
  data: {
    result: '点击按钮测试',
  },

  async onTest() {
    this.setData({ result: '请求中...' });
    try {
      const res = await new Promise((resolve, reject) => {
        wx.request({
          url: 'http://192.168.0.109:8000/',
          success: resolve,
          fail: reject,
        });
      });
      this.setData({ result: JSON.stringify(res.data) });
    } catch (e) {
      this.setData({ result: '错误: ' + e.message });
    }
  },
});
