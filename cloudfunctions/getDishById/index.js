const cloud = require('wx-server-sdk');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });
const db = cloud.database();

exports.main = async (event) => {
  const { id } = event;

  try {
    const result = await db.collection('dishes').doc(id).get();
    return { success: true, data: result.data };
  } catch (err) {
    return { success: false, error: '菜品不存在' };
  }
};
