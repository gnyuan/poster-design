/*
 * @Author: ShawnPhang
 * @Date: 2021-08-19 18:30:38
 * @Description: Vite配置文件
 * @LastEditors: ShawnPhang <site: book.palxp.com>
 * @LastEditTime: 2023-08-01 10:46:59
 */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import viteCompression from 'vite-plugin-compression'
import ElementPlus from 'unplugin-element-plus/vite'

const resolve = (...data: string[]) => path.resolve(__dirname, ...data)

// https://vitejs.dev/config/
export default defineConfig({
  // base: '/web',
  plugins: [
    vue(),
    viteCompression({
      verbose: true,
      disable: false,
      threshold: 10240,
      algorithm: 'gzip',
      ext: '.gz',
    }),
    ElementPlus({
      // options
    }),
  ],
  build: {
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
  },
  resolve: {
    alias: {
      '@': resolve('src'),
      '~data': resolve('src/assets/data'),
    },
  },
  css: {
    preprocessorOptions: {
      less: {
        modifyVars: {
          color: `true; @import "./src/assets/styles/color.less";`,
        },
      },
    },
  },
  define: {
    'process.env': process.env,
  },
  server: {
    port: 9001,
    https: false,
    cors: true,
    hmr: { overlay: false },
    proxy: {
      '/screenshots': {
        target: 'http://10.18.12.113:9002',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/screenshots/, ''),
      },
      '/api': {
        target: 'http://10.18.12.113:9000/api/',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/ai/remove': {
        target: 'http://10.18.12.113:9003/api/remove',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/ai\/remove/, ''),
      },
      '/static': {
        target: 'http://10.18.12.113:9004/',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/static/, ''),
      },
    },
    headers: {
      'Referrer-Policy': 'no-referrer-when-downgrade', // Change this as needed
    },
  },
})
