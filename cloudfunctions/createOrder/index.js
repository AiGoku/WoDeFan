const cloud = require('wx-server-sdk');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });
const db = cloud.database();

function generateShareCode() {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let code = '';
  for (let i = 0; i < 8; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return code;
}

exports.main = async (event) => {
  const { dish_ids } = event;
  const openid = cloud.getWXContext().OPENID;

  if (!openid) {
    return { success: false, error: '无法获取用户信息' };
  }
  if (!dish_ids || dish_ids.length === 0) {
    return { success: false, error: '请选择至少一道菜' };
  }

  try {
    const shareCode = generateShareCode();

    const dishResults = await db
      .collection('dishes')
      .where({
        _id: db.command.in(dish_ids),
      })
      .get();

    const dishes = dishResults.data;

    const items = dishes.map((dish) => ({
      dish_id: dish._id,
      dish_name: dish.name,
      dish_price: dish.price,
      dish_image: dish.image_url || '',
      added_by_openid: openid,
    }));

    const totalPrice = items.reduce((sum, item) => sum + item.dish_price, 0);

    const orderResult = await db.collection('orders').add({
      data: {
        share_code: shareCode,
        creator_openid: openid,
        status: 'active',
        items,
        total_price: totalPrice,
        created_at: db.serverDate(),
        updated_at: db.serverDate(),
      },
    });

    return {
      success: true,
      data: {
        _id: orderResult._id,
        share_code: shareCode,
        creator_openid: openid,
        status: 'active',
        items,
        total_price: totalPrice,
      },
    };
  } catch (err) {
    return { success: false, error: err.message };
  }
};
