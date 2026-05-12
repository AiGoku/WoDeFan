/**
 * 图片上传工具页
 * 使用方式：
 * 1. 在微信开发者工具的云开发控制台 → 云存储 → 手动上传图片到 dishes/ 目录
 * 2. 文件名格式: {filename}.jpg (如 pat_huanggua.jpg)
 * 3. 回到此页面，点击"更新数据库"自动关联图片到菜品
 *
 * 或者使用"选择图片上传"功能，从本地选择图片逐个上传
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
      this.setData({ uploading: true, total: tempFiles.length, progress: 0, status: 'uploading...' });

      const fileMap = {};
      for (let i = 0; i < tempFiles.length; i++) {
        const tempPath = tempFiles[i];
        const fs = wx.getFileSystemManager();
        const imageData = fs.readFileSync(tempPath, 'base64');
        const namePart = tempPath.split('/').pop().split('.')[0];

        this.setData({ status: `upload ${i + 1}/${tempFiles.length}: ${namePart}`, progress: i + 1 });

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
        status: `done, ${Object.keys(fileMap).length} uploaded`,
      });
      wx.showToast({ title: 'upload ok', icon: 'success' });
    } catch (e) {
      this.setData({ uploading: false, status: 'fail: ' + e.message });
    }
  },

  // 从云存储自动关联
  async onAutoLink() {
    this.setData({ status: 'listing files...' });
    try {
      const result = await wx.cloud.callFunction({
        name: 'uploadImages',
        data: { mode: 'listFiles' },
      });

      if (!result.result.success) {
        this.setData({ status: 'list fail: ' + result.result.error });
        return;
      }

      const files = result.result.files;
      this.setData({ status: `found ${files.length} files, updating db...` });

      const fileMap = {};
      for (const f of files) {
        const name = f.cloudPath.split('/').pop().replace('.jpg', '').replace('.png', '');
        fileMap[name] = f.fileID;
      }

      const updateResult = await wx.cloud.callFunction({
        name: 'uploadImages',
        data: { mode: 'updateDB', fileMap },
      });

      if (updateResult.result.success) {
        this.setData({ status: `done! ${updateResult.result.updated}/${updateResult.result.total} updated` });
        wx.showToast({ title: 'ok', icon: 'success' });
      } else {
        this.setData({ status: 'update fail: ' + updateResult.result.error });
      }
    } catch (e) {
      this.setData({ status: 'fail: ' + e.message });
    }
  },

  // 手动更新数据库
  async onUpdateDB() {
    const { fileMap, fileCount } = this.data;
    if (fileCount === 0) {
      wx.showToast({ title: 'upload first', icon: 'none' });
      return;
    }

    this.setData({ status: 'updating db...' });
    try {
      const result = await wx.cloud.callFunction({
        name: 'uploadImages',
        data: { mode: 'updateDB', fileMap },
      });

      if (result.result.success) {
        this.setData({ status: `done! ${result.result.updated}/${result.result.total} updated` });
        wx.showToast({ title: 'ok', icon: 'success' });
      } else {
        this.setData({ status: 'fail: ' + result.result.error });
      }
    } catch (e) {
      this.setData({ status: 'fail: ' + e.message });
    }
  },
});
