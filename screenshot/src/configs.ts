/*
 * @Author: ShawnPhang
 * @Date: 2022-02-01 13:41:59
 * @Description: 配置文件
 * @LastEditors: ShawnPhang <https://m.palxp.cn>
 * @LastEditTime: 2023-09-15 10:40:41
 */
const isDev = process.env.NODE_ENV === "development";

exports.servicePort = 9002;

/**
 * 配置服务器端的chrome浏览器位置
 */
(exports.executablePath = "/opt/google/chrome-unstable/chrome"),
  /**
   * 前端绘制页地址
   */
  (exports.drawLink = isDev
    ? "http://10.18.12.113:9001/draw"
    : "https://design.palxp.cn/draw");

/**
 * 截图并发数上限
 */
exports.maxNum = 2;

/**
 * 截图队列的阈值，超出时请求将会被熔断
 */
exports.upperLimit = 20;

/**
 * 多久释放浏览器驻留内存，单位：秒（多标签页版生效）
 */
exports.releaseTime = 300;

/**
 * 图片缓存目录位置，根据实际情况调整
 */
exports.filePath = isDev ? process.cwd() + `/static/` : "/cache/";
// exports.filePath = process.cwd() + `/static/`
