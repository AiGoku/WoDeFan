const cloud = require('wx-server-sdk');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });
const db = cloud.database();

exports.main = async (event) => {
  const { share_code, dish_id } = event;
  const openid = cloud.getWXContext().OPENID;

  if (!openid) {
    return { success: false, error: '无法获取用户信息' };
  }

  try {
    const orderResult = await db
      .collection('orders')
      .where({ share_code })
      .get();

    if (orderResult.data.length === 0) {
      return { success: false, error: '点菜单不存在' };
    }

    const order = orderResult.data[0];

    if (order.status !== 'active') {
      return { success: false, error: '该点菜单已关闭' };
    }

    let dish;
    try {
      const dishResult = await db.collection('dishes').doc(dish_id).get();
      dish = dishResult.data;
    } catch (e) {
      return { success: false, error: '菜品不存在' };
    }

    const newItem = {
      dish_id: dish._id,
      dish_name: dish.name,
      dish_price: dish.price,
      dish_image: dish.image_url || '',
      added_by_openid: openid,
    };

    await db
      .collection('orders')
      .doc(order._id)
      .update({
        data: {
          items: db.command.push(newItem),
          total_price: db.command.inc(dish.price),
          updated_at: db.serverDate(),
        },
      });

    const updatedResult = await db.collection('orders').doc(order._id).get();
    return { success: true, data: updatedResult.data };
  } catch (err) {
    return { success: false, error: err.message };
  }
};
