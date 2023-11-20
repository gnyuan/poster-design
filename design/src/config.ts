// const prefix = import.meta.env
const prefix = process.env

const isDev = prefix.NODE_ENV === 'development'
import { version } from '../package.json'

export default {
  isDev,
  BASE_URL: isDev ? '/' : './',
  VERSION: version,
  APP_NAME: '长图设计',
  COPYRIGHT: 'YuanGengnan',
  API_URL: '/api',
  SCREEN_URL: '/screenshots',
  // ICONFONT_URL: '//at.alicdn.com/t/font_3223711_74mlzj4jdue.css',
  ICONFONT_URL: '//at.alicdn.com/t/font_2717063_ypy8vprc3b.css?display=swap',
  ICONFONT_EXTRA: '//at.alicdn.com/t/c/font_3228074_zubqmza1sdk.css',
  ICONFONT2: '//at.alicdn.com/t/c/font_4337374_r28wvteb6d.css',
  supportSubFont: true, // 是否开启服务端字体压缩
  UPLOAD_URL: '/ai/remove',
}
