/*
 * @Author: ShawnPhang
 * @Date: 2021-08-27 14:42:15
 * @Description: AI相关接口
 * @LastEditors: ShawnPhang <https://m.palxp.cn>
 * @LastEditTime: 2023-10-13 00:07:19
 */
import fetch from '@/utils/axios'
import _config from '@/config'

// 上传接口
export const upload = (file: File, cb: Function) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('model', 'u2net')
  formData.append('a', 'false')
  formData.append('af', '240')
  formData.append('ab', '10')
  formData.append('ae', '10')
  formData.append('om', 'false')
  formData.append('ppm', 'false')
  const extra = {
    responseType: 'blob',
    onUploadProgress: (progress: any) => {
      cb(Math.floor((progress.loaded / progress.total) * 100), 0)
    },
    onDownloadProgress: (progress: any) => {
      cb(100, Math.floor((progress.loaded / progress.total) * 100))
    },
  }
  return fetch(_config.UPLOAD_URL, formData, 'post', {}, extra)
}
