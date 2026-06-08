// 模拟wx
global.wx = require('../../__mocks__/wx');

// 模拟getApp
global.getApp = jest.fn(() => ({
  globalData: {
    baseUrl: 'https://food.aigoku.com/api'
  }
}));

const api = require('../api');

describe('api.js', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('resolveImageUrl', () => {
    test('should return empty string for empty input', () => {
      expect(api.resolveImageUrl('')).toBe('');
    });

    test('should return empty string for null input', () => {
      expect(api.resolveImageUrl(null)).toBe('');
    });

    test('should return empty string for undefined input', () => {
      expect(api.resolveImageUrl(undefined)).toBe('');
    });

    test('should return http URL unchanged', () => {
      const url = 'http://example.com/img.jpg';
      expect(api.resolveImageUrl(url)).toBe(url);
    });

    test('should return https URL unchanged', () => {
      const url = 'https://example.com/img.jpg';
      expect(api.resolveImageUrl(url)).toBe(url);
    });

    test('should convert relative path to full URL', () => {
      const path = '/static/images/dish.jpg';
      const result = api.resolveImageUrl(path);
      expect(result).toBe('https://food.aigoku.com/static/images/dish.jpg');
    });
  });

  describe('getDishes', () => {
    test('should call request with correct URL', async () => {
      wx.request.mockImplementation(({ success }) => {
        success({
          statusCode: 200,
          data: { items: [], total: 0 }
        });
      });

      await api.getDishes();
      expect(wx.request).toHaveBeenCalledWith(
        expect.objectContaining({
          url: 'https://food.aigoku.com/api/dishes/'
        })
      );
    });

    test('should build query string with params', async () => {
      wx.request.mockImplementation(({ success }) => {
        success({
          statusCode: 200,
          data: { items: [], total: 0 }
        });
      });

      await api.getDishes({ category: 'hot_dish', limit: 10 });
      expect(wx.request).toHaveBeenCalledWith(
        expect.objectContaining({
          url: 'https://food.aigoku.com/api/dishes/?category=hot_dish&limit=10'
        })
      );
    });

    test('should filter out null and empty params', async () => {
      wx.request.mockImplementation(({ success }) => {
        success({
          statusCode: 200,
          data: { items: [], total: 0 }
        });
      });

      await api.getDishes({ category: null, keyword: '', limit: 10 });
      expect(wx.request).toHaveBeenCalledWith(
        expect.objectContaining({
          url: 'https://food.aigoku.com/api/dishes/?limit=10'
        })
      );
    });
  });

  describe('request', () => {
    test('should resolve on success (2xx)', async () => {
      const mockData = { id: 1, name: '番茄炒蛋' };
      wx.request.mockImplementation(({ success }) => {
        success({
          statusCode: 200,
          data: mockData
        });
      });

      const result = await api.getDishById(1);
      expect(result).toEqual(mockData);
    });

    test('should reject on error (4xx)', async () => {
      wx.request.mockImplementation(({ success }) => {
        success({
          statusCode: 404,
          data: { detail: '菜品不存在' }
        });
      });

      await expect(api.getDishById(999)).rejects.toThrow('菜品不存在');
    });

    test('should reject on network failure', async () => {
      wx.request.mockImplementation(({ fail }) => {
        fail({ errMsg: 'request:fail' });
      });

      await expect(api.getDishById(1)).rejects.toEqual({ errMsg: 'request:fail' });
    });
  });
});
