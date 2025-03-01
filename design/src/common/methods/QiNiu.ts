/*
 * @Author: ShawnPhang
 * @Date: 2021-08-29 20:35:31
 * @Description: 七牛上传方法
 * @LastEditors: ShawnPhang <https://m.palxp.cn>
 * @LastEditTime: 2023-10-05 16:11:55
 */
import dayjs from 'dayjs'
import api from '@/api/album'

interface Options {
  bucket: string
  prePath?: string
  fullPath?: string
}

export default {
  upload2: async (file: File, options: Options, cb?: Function) => {
    const win: any = window
    let name = ''
    const suffix = file.type.split('/')[1] || 'png' // 文件后缀
    if (!options.fullPath) {
      // const DT: any = await exifGetTime(file) // 照片时间
      const DT: any = new Date()
      const YM = `${dayjs(DT).format('YYYY')}/${dayjs(DT).format('MM')}/` // 文件时间分类
      const keyName = YM + new Date(DT).getTime()
      const prePath = options.prePath ? options.prePath + '/' : ''
      name = `${prePath}${keyName}` + `.${suffix}` // 文件名
    } else name = options.fullPath + `.${suffix}` // 文件名
    const token = await api.getToken({ bucket: options.bucket, name })
    const exOption = {
      useCdnDomain: true, // 使用cdn加速
    }
    const observable = win.qiniu.upload(file, name, token, {}, exOption)
    return new Promise((resolve: Function, reject: Function) => {
      observable.subscribe({
        next: (result: any) => {
          cb && cb(result) // result.total.percent -> 展示进度
        },
        error: (e: any) => {
          reject(e)
        },
        complete: (result: any) => {
          resolve(result)
          // cb && cb(result) // result.total.percent -> 展示进度
        },
      })
    })
  },
  upload: async (file: File, options: Options, cb?: Function) => {
    let name = ''
    const suffix = file.type.split('/')[1] || 'png' // 文件后缀
    if (!options.fullPath) {
      // const DT: any = await exifGetTime(file) // 照片时间
      const DT: any = new Date()
      const YM = `${dayjs(DT).format('YYYY')}/${dayjs(DT).format('MM')}/` // 文件时间分类
      const keyName = YM + new Date(DT).getTime()
      const prePath = options.prePath ? options.prePath + '/' : ''
      name = `${prePath}${keyName}` + `.${suffix}` // 文件名
    } else name = options.fullPath + `.${suffix}` // 文件名
    const user = await api.getToken({ type: 'post', username: 'superadmin', password: '123456' })
    const token = user.token
    const headers = {
      accept: 'application/json',
      Authorization: token,
    }
    const formData = new FormData()
    formData.append('file', file) // 用你的文件替代 'file'

    const observable = api.upload(formData, { ...headers })

    // 创建一个 Promise 包装对象
    return new Promise((resolve, reject) => {
      const cb = (result: any) => {
        // 处理进度回调
        if (result && result.total && result.total.percent) {
          // 展示进度
          console.log(`上传进度: ${result.total.percent}%`)
        }
      }

      // 直接返回 observable 对象
      resolve(observable)
    })
  },
}

// function exifGetTime(img: any) {
//   const win = window as any
//   return new Promise((resolve) => {
//     const file = img.originFileObj || img
//     win.EXIF.getData(file, function() {
//       const DT = win.EXIF.getAllTags(this).DateTimeOriginal || win.EXIF.getAllTags(this).DateTime
//       if (DT) {
//         if (DT.split(' ').length > 1) {
//           const date = DT.split(' ')[0].replace(/:/g, '/')
//           const time = DT.split(' ')[1]
//           resolve(dayjs(`${date} ${time}`).isValid() ? `${date} ${time}` : date)
//         } else {
//           resolve(DT)
//         }
//       } else {
//         resolve(new Date())
//       }
//     })
//   })
// }
