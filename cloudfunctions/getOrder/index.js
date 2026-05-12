const cloud = require('wx-server-sdk');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });
const db = cloud.database();

exports.main = async (event) => {
  const { share_code } = event;

  try {
    const result = await db
      .collection('orders')
      .where({ share_code })
      .get();

    if (result.data.length === 0) {
      return { success: false, error: '点菜单不存在' };
    }

    const order = result.data[0];
    return { success: true, data: order };
  } catch (err) {
    return { success: false, error: err.message };
  }
};
