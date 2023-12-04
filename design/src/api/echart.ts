import fetch from '@/utils/axios'

// 获取echart组件初始配置及初始数据
export const getEchart = (params: Type.Object = {}) =>
  fetch('design/echart_option', params, 'get')
