const cloud = require('wx-server-sdk');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

exports.main = async () => {
  return {
    success: true,
    data: [
      { key: 'cold_dish', name: '凉菜' },
      { key: 'hot_dish', name: '热菜' },
      { key: 'soup', name: '汤羹' },
      { key: 'staple', name: '主食' },
      { key: 'dessert', name: '甜品小吃' },
      { key: 'drink', name: '饮品' },
    ],
  };
};
