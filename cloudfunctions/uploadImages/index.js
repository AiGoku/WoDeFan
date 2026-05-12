const cloud = require('wx-server-sdk');

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });
const db = cloud.database();

// 菜品名 → 文件名映射
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

exports.main = async (event) => {
  try {
    const { mode } = event;

    // 模式1: 单张上传图片到云存储
    if (mode === 'upload') {
      const { filename, imageData } = event;
      const cloudPath = `dishes/${filename}.jpg`;

      const result = await cloud.uploadFile({
        cloudPath,
        fileContent: Buffer.from(imageData, 'base64'),
      });

      return { success: true, fileID: result.fileID, filename };
    }

    // 模式2: 列出云存储 dishes/ 目录下的所有文件
    if (mode === 'listFiles') {
      const fileList = [];
      let marker = undefined;

      do {
        const result = await cloud.cloudPathList({
          cloudPath: ['dishes/'],
          maxResults: 100,
          marker,
        });
        fileList.push(...result.fileList);
        marker = result.marker;
      } while (marker);

      return { success: true, files: fileList, count: fileList.length };
    }

    // 模式3: 用 fileID 映射批量更新数据库
    if (mode === 'updateDB') {
      const { fileMap } = event;
      if (!fileMap) return { success: false, error: 'fileMap required' };

      const countResult = await db.collection('dishes').count();
      const total = countResult.total;
      let allDishes = [];

      for (let i = 0; i < total; i += 20) {
        const res = await db.collection('dishes').skip(i).limit(20).get();
        allDishes = allDishes.concat(res.data);
      }

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

    return { success: false, error: 'unknown mode, use "upload" or "updateDB"' };
  } catch (err) {
    return { success: false, error: err.message };
  }
};
