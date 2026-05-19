const cloud = require('wx-server-sdk');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });
const db = cloud.database();

const nameToFileMap = {
  '拍黄瓜': 'pat_huanggua', '凉拌木耳': 'liangban_muer', '皮蛋豆腐': 'pidan_doufu',
  '口水鸡': 'koushui_ji', '蒜泥白肉': 'suanni_bairou', '凉拌三丝': 'liangban_sanwen',
  '五花肉冻': 'wuhua_routun', '糖醋莲藕': 'tangcu_lianou',
  '番茄炒蛋': 'fanqie_chaodan', '宫保鸡丁': 'gongbao_jiding', '鱼香肉丝': 'yuxiang_rousi',
  '红烧肉': 'hongshao_rou', '麻婆豆腐': 'mapo_doufu', '清蒸鲈鱼': 'qingzheng_luyu',
  '糖醋排骨': 'tangcu_paigu', '水煮牛肉': 'shuizhu_niurou', '干煸四季豆': 'ganbian_sijidou',
  '回锅肉': 'huiguo_rou', '清炒西兰花': 'qingchao_xilan', '鸡蛋羹': 'jidan_geng',
  '红烧冬瓜': 'hongshaorou_donggua', '炒牛肉': 'chaoniurou',
  '紫菜蛋花汤': 'zicai_danhuatang', '番茄蛋汤': 'fanqie_dantang', '冬瓜排骨汤': 'donggu_paigutang',
  '酸辣汤': 'suanla_tang', '玉米浓汤': 'yumi_nongtang', '萝卜排骨汤': 'luobo_tang',
  '冬瓜虾仁汤': 'zidou_danhuatang', '三鲜汤': 'sanxian_tang',
  '蛋炒饭': 'dan_chaofan', '阳春面': 'yangchun_mian', '炸酱面': 'zhajiang_mian',
  '扬州炒饭': 'yangzhou_chaofan', '饺子（猪肉白菜）': 'jiaozi', '炒米粉': 'chao_mifen',
  '豆浆油条': 'doujiang_youtiao', '馄饨': 'huntun', '白米饭': 'mifan', '炒面': 'chao_mian',
  '红糖糍粑': 'hongtang_ciba', '芒果布丁': 'mangguo_buding', '双皮奶': 'shuangpi_nai',
  '蛋挞': 'danta', '芝麻球': 'zhima_qiu', '汤圆': 'tangyuan', '月饼': 'yuebing', '冰淇淋': 'bingqilin',
  '柠檬水': 'ningmeng_shui', '酸梅汤': 'suanmei_tang', '豆浆': 'doujiang', '奶茶': 'naicha',
  '西瓜汁': 'xigua_zhi', '橙汁': 'chengzhi', '菠萝蜜汁': 'boluomei', '绿茶': 'lucha',
};

async function getAllDishes() {
  const countResult = await db.collection('dishes').count();
  const total = countResult.total;
  const allDishes = [];
  for (let i = 0; i < total; i += 20) {
    const res = await db.collection('dishes').skip(i).limit(20).get();
    allDishes.push(...res.data);
  }
  return allDishes;
}

// fileID 前缀（从云存储中实际文件的 fileID 获取）
const FILE_ID_PREFIX = 'cloud://cloud1-d8gdz5z0d911e1fb5.636c-cloud1-d8gdz5z0d911e1fb5-1429233331/';

exports.main = async (event) => {
  try {
    const { mode } = event;

    // 模式1: 单张上传
    if (mode === 'upload') {
      const { filename, imageData } = event;
      const cloudPath = `dishes/${filename}.jpg`;
      const result = await cloud.uploadFile({
        cloudPath,
        fileContent: Buffer.from(imageData, 'base64'),
      });
      return { success: true, fileID: result.fileID, filename };
    }

    // 模式2: 自动关联（全在云函数完成，有管理员权限）
    if (mode === 'autoLink') {
      const allDishes = await getAllDishes();

      // 构建 fileID 列表
      const dishFilePairs = [];
      for (const [name, filename] of Object.entries(nameToFileMap)) {
        dishFilePairs.push({ name, filename });
      }
      const fileList = dishFilePairs.map(p => `${FILE_ID_PREFIX}dishes/${p.filename}.jpg`);

      // 分批调用 getTempFileURL（每次最多 50 个）
      const allResults = [];
      for (let i = 0; i < fileList.length; i += 50) {
        const batch = fileList.slice(i, i + 50);
        const batchResult = await cloud.getTempFileURL({ fileList: batch });
        allResults.push(...(batchResult.fileList || []));
      }

      // 构建 name→dish 映射
      const dishByName = {};
      for (const dish of allDishes) {
        dishByName[dish.name] = dish;
      }

      // 匹配并并行更新数据库
      const updateTasks = [];
      const notFound = [];
      const details = [];

      for (let i = 0; i < allResults.length; i++) {
        const item = allResults[i];
        const pair = dishFilePairs[i];
        if (!pair) continue;

        if (item.status === 0 && item.tempFileURL) {
          const dish = dishByName[pair.name];
          if (dish) {
            updateTasks.push(
              db.collection('dishes').doc(dish._id).update({
                data: { image_url: item.tempFileURL }
              }).then(() => {
                details.push(`${pair.name} → ${pair.filename}.jpg`);
              })
            );
          }
        } else {
          notFound.push(pair.filename);
        }
      }

      // 每 10 个一批并行执行
      for (let i = 0; i < updateTasks.length; i += 10) {
        await Promise.all(updateTasks.slice(i, i + 10));
      }

      return {
        success: true,
        total: allDishes.length,
        updated: details.length,
        details,
        notFound,
      };
    }

    // 模式3: 手动更新数据库
    if (mode === 'updateDB') {
      const { fileMap } = event;
      if (!fileMap) return { success: false, error: 'fileMap required' };

      const allDishes = await getAllDishes();
      let updated = 0;
      for (const dish of allDishes) {
        const filename = nameToFileMap[dish.name];
        if (filename && fileMap[filename]) {
          await db.collection('dishes').doc(dish._id).update({
            data: { image_url: fileMap[filename] }
          });
          updated++;
        }
      }
      return { success: true, total: allDishes.length, updated };
    }

    return { success: false, error: 'unknown mode' };
  } catch (err) {
    return { success: false, error: err.message };
  }
};
