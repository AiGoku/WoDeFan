/**
 * E2E测试脚本 - 基本流程
 * 使用miniprogram-automator SDK
 *
 * 运行前提：
 * 1. 微信开发者工具已启动
 * 2. 后端服务运行在 http://localhost:8000
 * 3. 已安装miniprogram-automator: npm install miniprogram-automator --save-dev
 */

const automator = require('miniprogram-automator');

describe('我的饭小程序 - 基本流程测试', () => {
  let miniProgram;
  let page;

  beforeAll(async () => {
    // 连接到微信开发者工具
    miniProgram = await automator.connect({
      projectPath: './miniprogram'
    });
  }, 30000);

  afterAll(async () => {
    if (miniProgram) {
      await miniProgram.close();
    }
  });

  describe('场景1: 浏览菜品并查看详情', () => {
    test('首页加载正常', async () => {
      page = await miniProgram.reLaunch('/pages/index/index');
      await page.waitFor('.dish-list', { timeout: 5000 });

      // 验证页面标题
      const title = await page.$('.page-title');
      expect(await title.text()).toContain('点菜');

      // 验证菜品列表
      const dishes = await page.$$('.dish-card');
      expect(dishes.length).toBeGreaterThan(0);
    });

    test('分类筛选功能', async () => {
      // 点击热菜分类
      const categoryBtn = await page.$('[data-category="hot_dish"]');
      await categoryBtn.click();

      // 等待列表更新
      await page.waitFor(500);

      // 验证只显示热菜
      const dishes = await page.$$('.dish-card');
      for (const dish of dishes) {
        const category = await dish.dataset('category');
        expect(category).toBe('hot_dish');
      }
    });

    test('菜品详情页', async () => {
      // 点击第一个菜品
      const firstDish = await page.$('.dish-card');
      await firstDish.click();

      // 等待详情页加载
      await page.waitFor('.detail-page', { timeout: 3000 });

      // 验证详情信息
      const name = await page.$('.dish-name');
      expect(await name.text()).toBeTruthy();

      const price = await page.$('.dish-price');
      expect(await price.text()).toContain('¥');

      const description = await page.$('.dish-description');
      expect(await description.text()).toBeTruthy();

      // 返回首页
      await page.navigateBack();
    });
  });

  describe('场景2: 添加菜品到购物车', () => {
    test('从首页添加菜品', async () => {
      // 确保在首页
      page = await miniProgram.reLaunch('/pages/index/index');
      await page.waitFor('.dish-list');

      // 点击添加按钮
      const addBtn = await page.$('.add-btn');
      await addBtn.click();

      // 验证Toast提示
      const toast = await page.waitFor('.wx-toast', { timeout: 2000 });
      expect(await toast.text()).toContain('已加入');

      // 验证购物车数量
      const cartBadge = await page.$('.cart-badge');
      expect(await cartBadge.text()).toBe('1');
    });

    test('重复添加提示', async () => {
      // 再次点击同一个添加按钮
      const addBtn = await page.$('.add-btn');
      await addBtn.click();

      // 验证Toast提示
      const toast = await page.waitFor('.wx-toast', { timeout: 2000 });
      expect(await toast.text()).toContain('已在菜单中');
    });
  });

  describe('场景3: 查看和管理购物车', () => {
    test('购物车页面显示', async () => {
      // 切换到购物车Tab
      await miniProgram.switchTab('/pages/cart/cart');
      page = await miniProgram.currentPage();

      // 验证购物车列表
      const cartItems = await page.$$('.cart-item');
      expect(cartItems.length).toBeGreaterThan(0);

      // 验证总价显示
      const totalPrice = await page.$('.total-price');
      expect(await totalPrice.text()).toContain('¥');
    });

    test('删除菜品', async () => {
      // 点击删除按钮
      const deleteBtn = await page.$('.delete-btn');
      await deleteBtn.click();

      // 确认删除
      const confirmBtn = await page.waitFor('.confirm-btn', { timeout: 2000 });
      await confirmBtn.click();

      // 验证菜品被移除
      await page.waitFor(500);
      const cartItems = await page.$$('.cart-item');
      expect(cartItems.length).toBe(0);
    });

    test('清空购物车', async () => {
      // 先添加菜品
      await miniProgram.switchTab('/pages/index/index');
      page = await miniProgram.currentPage();
      const addBtn = await page.$('.add-btn');
      await addBtn.click();

      // 回到购物车
      await miniProgram.switchTab('/pages/cart/cart');
      page = await miniProgram.currentPage();

      // 点击清空按钮
      const clearBtn = await page.$('.clear-btn');
      await clearBtn.click();

      // 确认清空
      const confirmBtn = await page.waitFor('.confirm-btn', { timeout: 2000 });
      await confirmBtn.click();

      // 验证购物车被清空
      await page.waitFor(500);
      const emptyTip = await page.$('.empty-tip');
      expect(await emptyTip.text()).toContain('菜单是空的');
    });
  });

  describe('场景4: 创建订单并分享', () => {
    test('创建订单', async () => {
      // 先添加菜品
      await miniProgram.switchTab('/pages/index/index');
      page = await miniProgram.currentPage();
      const addBtn = await page.$('.add-btn');
      await addBtn.click();

      // 回到购物车
      await miniProgram.switchTab('/pages/cart/cart');
      page = await miniProgram.currentPage();

      // 点击分享按钮
      const shareBtn = await page.$('.share-btn');
      await shareBtn.click();

      // 等待订单创建
      const loading = await page.waitFor('.wx-loading', { timeout: 2000 });
      expect(await loading.text()).toContain('创建中');

      // 等待分享面板
      await page.waitFor('.share-panel', { timeout: 5000 });

      // 验证分享内容
      const shareTitle = await page.$('.share-title');
      expect(await shareTitle.text()).toContain('一起点菜吧');
    });
  });

  describe('场景5: 打开分享链接', () => {
    test('通过分享码打开订单', async () => {
      // 模拟打开分享链接
      page = await miniProgram.reLaunch('/pages/share/share?share_code=test1234');

      // 等待页面加载
      await page.waitFor('.share-page', { timeout: 5000 });

      // 验证显示朋友的菜单
      const title = await page.$('.page-title');
      expect(await title.text()).toContain('朋友的菜单');

      // 验证菜品列表
      const dishes = await page.$$('.dish-item');
      expect(dishes.length).toBeGreaterThan(0);
    });

    test('协作加菜功能', async () => {
      // 点击加菜按钮
      const addDishBtn = await page.$('.add-dish-btn');
      await addDishBtn.click();

      // 等待菜品选择面板
      await page.waitFor('.dish-panel', { timeout: 3000 });

      // 选择一个菜品
      const dishItem = await page.$('.dish-option');
      await dishItem.click();

      // 验证菜品被添加
      await page.waitFor(1000);
      const dishes = await page.$$('.dish-item');
      expect(dishes.length).toBeGreaterThan(1);
    });
  });

  describe('场景6: 边界情况', () => {
    test('空购物车分享提示', async () => {
      // 清空购物车
      await miniProgram.switchTab('/pages/cart/cart');
      page = await miniProgram.currentPage();
      const clearBtn = await page.$('.clear-btn');
      if (clearBtn) {
        await clearBtn.click();
        const confirmBtn = await page.waitFor('.confirm-btn', { timeout: 2000 });
        await confirmBtn.click();
      }

      // 尝试分享
      const shareBtn = await page.$('.share-btn');
      await shareBtn.click();

      // 验证提示
      const toast = await page.waitFor('.wx-toast', { timeout: 2000 });
      expect(await toast.text()).toContain('菜单是空的');
    });

    test('无效分享码', async () => {
      // 打开无效分享链接
      page = await miniProgram.reLaunch('/pages/share/share?share_code=invalid123');

      // 等待错误提示
      const errorTip = await page.waitFor('.error-tip', { timeout: 5000 });
      expect(await errorTip.text()).toContain('点菜单不存在');
    });
  });
});
