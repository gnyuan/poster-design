<!--
 * @Author: ShawnPhang
 * @Date: 2022-02-11 18:48:23
 * @Description: 组件列表
 * @LastEditors: ShawnPhang <https://m.palxp.cn>
 * @LastEditTime: 2023-10-13 18:48:25
-->
<template>
  <div class="wrap">
    <div class="header">组件</div>
    <div class="item" @click="addQrcode">
      <i class="icon sd-w-qrcode" />
      <div class="text">
        <span>二维码</span><span class="desc">在设计中使用风格化二维码</span>
      </div>
    </div>
    <div class="item" @click="addPieChart">
      <i class="icon sd-tubiao-bingtu" />
      <div class="text">
        <span>饼图</span><span class="desc">使用ECharts饼图</span>
      </div>
    </div>
    <div class="item" @click="addQrcode">
      <i class="icon sd-tubiao-zhuzhuangtu" />
      <div class="text">
        <span>柱状图</span><span class="desc">使用ECharts柱状图</span>
      </div>
    </div>
    <div class="item" @click="addQrcode">
      <i class="icon sd-tubiao-zhexiantu" />
      <div class="text">
        <span>折线图</span><span class="desc">使用ECharts折线图</span>
      </div>
    </div>
    <div class="header">其它</div>
    <div class="item" @click="openImageCutout">
      <i class="icon sd-AI_zhineng" />
      <div class="text">
        <span>智能抠图</span> <span class="desc">上传图像一键去除背景</span>
      </div>
    </div>
    <imageCutout ref="imageCutout" />
  </div>
</template>

<script>
// 图片列表
const NAME = 'tool-list-wrap'
// import api from '@/api'
import { mapActions, mapGetters } from 'vuex'
import wQrcode from '../../widgets/wQrcode/wQrcode.vue'
import imageCutout from '@/components/business/image-cutout'
import wPiechart from '../../widgets/wEcharts/wPiechart.vue'

export default {
  name: NAME,
  components: { imageCutout },
  data() {
    return {
      loadDone: false,
    }
  },
  computed: {
    ...mapGetters(['dPage']),
  },

  mounted() {
    // this.getDataList()
    setTimeout(() => {
      const { koutu } = this.$route.query
      koutu && this.openImageCutout()
    }, 300)
  },
  methods: {
    ...mapActions(['addWidget']),
    async getDataList() {
      if (this.loadDone || this.loading) {
        return
      }
      this.loading = true
      this.page += 1
    },
    addQrcode() {
      this.$store.commit('setShowMoveable', false) // 清理掉上一次的选择
      let setting = JSON.parse(JSON.stringify(wQrcode.setting))
      const { width: pW, height: pH } = this.dPage
      setting.left = pW / 2 - setting.width / 2
      setting.top = pH / 2 - setting.height / 2
      this.addWidget(setting)
      console.log(setting)
    },
    addPieChart() {
      this.$store.commit('setShowMoveable', false) // 清理掉上一次的选择
      console.log('add clicked!')
      let setting = JSON.parse(JSON.stringify(wPiechart.setting))
      const { width: pW, height: pH } = this.dPage
      setting.left = pW / 2 - setting.width / 2
      setting.top = pH / 2 - setting.height / 2
      this.addWidget(setting)
      console.log(setting)
    },
    openImageCutout() {
      this.$refs.imageCutout.open()
    },
  },
}
</script>

<style lang="less" scoped>
.wrap {
  width: 100%;
  height: 100%;
}
.header {
  padding: 17px 1rem;
  height: 56px;
  display: flex;
  position: relative;
  font-size: 16px;
  color: #333333;
  font-weight: bold;
  display: flex;
  align-items: center;
  user-select: none;
}
.item {
  opacity: 0.85;
  position: relative;
  border-radius: 4px;
  font-size: 15px;
  height: 72px;
  color: #33383e;
  display: flex;
  align-items: center;
  cursor: pointer;
  margin: 0 1rem 16px;
  user-select: none;
  background-color: #f6f7f9;
}
.item:hover {
  opacity: 1;
}
.icon {
  margin: 0 1rem;
  font-size: 32px;
}
.text {
  display: flex;
  flex-direction: column;
}
.desc {
  padding-top: 0.5rem;
  color: #7f8792;
  font-size: 12px;
}
</style>
