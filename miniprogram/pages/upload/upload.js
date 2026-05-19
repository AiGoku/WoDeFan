/**
 * 图片上传工具页
 */
Page({
  data: {
    fileMap: {},
    fileCount: 0,
    status: '',
    uploading: false,
    progress: 0,
    total: 0,
  },

  // 从本地选择图片上传到云存储
  async onChooseAndUpload() {
    try {
      const res = await new Promise((resolve, reject) => {
        wx.chooseImage({
          count: 9,
          sizeType: ['compressed'],
          sourceType: ['album'],
          success: resolve,
          fail: reject,
        });
      });

      const tempFiles = res.tempFilePaths;
      this.setData({ uploading: true, total: tempFiles.length, progress: 0, status: '上传中...' });

      const fileMap = {};
      for (let i = 0; i < tempFiles.length; i++) {
        const tempPath = tempFiles[i];
        const fs = wx.getFileSystemManager();
        const imageData = fs.readFileSync(tempPath, 'base64');
        const namePart = tempPath.split('/').pop().split('.')[0];

        this.setData({ status: `上传 ${i + 1}/${tempFiles.length}: ${namePart}`, progress: i + 1 });

        const result = await wx.cloud.callFunction({
          name: 'uploadImages',
          data: { mode: 'upload', filename: namePart, imageData },
        });

        if (result.result.success) {
          fileMap[namePart] = result.result.fileID;
        }
      }

      this.setData({
        fileMap,
        fileCount: Object.keys(fileMap).length,
        uploading: false,
        status: `上传完成, ${Object.keys(fileMap).length} 张`,
      });
      wx.showToast({ title: '上传完成', icon: 'success' });
    } catch (e) {
      this.setData({ uploading: false, status: '上传失败: ' + e.message });
    }
  },

  // 自动关联：全部在云函数中完成（有管理员权限，可访问控制台上传的文件）
  async onAutoLink() {
    this.setData({ status: '正在关联云存储图片...', uploading: true });
    try {
      const result = await wx.cloud.callFunction({
        name: 'uploadImages',
        data: { mode: 'autoLink' },
      });

      const res = result.result;
      console.log('autoLink result:', JSON.stringify(res));

      if (!res.success) {
        this.setData({ status: '关联失败: ' + res.error, uploading: false });
        return;
      }

      const msg = `完成! ${res.updated}/${res.total} 菜品已关联图片`;
      this.setData({
        status: msg,
        uploading: false,
        fileCount: res.updated,
      });
      wx.showToast({ title: `${res.updated} 张已关联`, icon: 'success' });
    } catch (e) {
      console.error('autoLink error:', e);
      this.setData({ status: '关联失败: ' + e.message, uploading: false });
    }
  },

  // 手动更新数据库
  async onUpdateDB() {
    const { fileMap, fileCount } = this.data;
    if (fileCount === 0) {
      wx.showToast({ title: '请先上传图片', icon: 'none' });
      return;
    }

    this.setData({ status: '更新数据库...' });
    try {
      const result = await wx.cloud.callFunction({
        name: 'uploadImages',
        data: { mode: 'updateDB', fileMap },
      });

      if (result.result.success) {
        this.setData({ status: `完成! ${result.result.updated}/${result.result.total} 已更新` });
        wx.showToast({ title: '更新成功', icon: 'success' });
      } else {
        this.setData({ status: '更新失败: ' + result.result.error });
      }
    } catch (e) {
      this.setData({ status: '更新失败: ' + e.message });
    }
  },
});
