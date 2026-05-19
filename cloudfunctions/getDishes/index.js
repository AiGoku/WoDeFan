const cloud = require('wx-server-sdk');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });
const db = cloud.database();
const _ = db.command;

// 列表页只需要这些字段，详情字段在 getDishById 中返回
const LIST_FIELDS = {
  _id: true,
  name: true,
  category: true,
  price: true,
  image_url: true,
  description: true,
  season_tag: true,
};

exports.main = async (event) => {
  const { category, season, keyword } = event;

  try {
    let query = {};

    if (category) {
      query.category = category;
    }
    if (season) {
      query.season_tag = season;
    }
    if (keyword) {
      query.name = db.RegExp({
        regexp: keyword,
        options: 'i',
      });
    }

    const collection = db.collection('dishes');
    const countResult = await collection.where(query).count();
    const total = countResult.total;

    const batchSize = 20;
    const batchTimes = Math.ceil(total / batchSize);
    const tasks = [];

    for (let i = 0; i < batchTimes; i++) {
      tasks.push(
        collection
          .where(query)
          .field(LIST_FIELDS)
          .skip(i * batchSize)
          .limit(batchSize)
          .orderBy('_id', 'desc')
          .get()
      );
    }

    const results = await Promise.all(tasks);
    const dishes = results.reduce((acc, cur) => acc.concat(cur.data), []);

    return { success: true, data: dishes };
  } catch (err) {
    return { success: false, error: err.message };
  }
};
