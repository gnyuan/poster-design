<template>
  <div
    :id="params.uuid"
    ref="widget"
    :class="['w-piechart', { 'layer-lock': params.lock }]"
    :style="{
      position: 'absolute',
      left: params.left - parent.left + 'px',
      top: params.top - parent.top + 'px',
      width: params.width + 'px',
      height: params.height + 'px',
      opacity: params.opacity,
    }"
  >
    <PieChart
      :opts="echartOptions"
      :width="width - 5"
      :height="height - 5"
      class="target"
    />
  </div>
</template>

<script lang="ts">
// 图片组件
const NAME = 'w-piechart'

import { mapGetters, mapActions } from 'vuex'
import { merge } from 'lodash-es'
import { EChartsOption } from 'echarts'

import api from '@/api'
import PieChart from '@/components/business/echarts/pie.ts'
import { echarts_comp } from './echartsettings'

const COLORS = [
  '#4E70F0',
  '#00C5D2',
  '#FFCE2B',
  '#FF812C',
  '#FF5A2E',
  '#1720D1',
  '#A64DFF',
  '#F95DBA',
  '#81D4FA',
  '#9FA8DA',
  '#CE93D8',
  '#F48FB1',
  '#FFAB91',
  '#FFCC80',
  '#FFE082',
  '#FFE082',
  '#A5D6A7',
  '#80CBC4',
  '#B0BEC5',
]

export default {
  name: NAME,
  components: { PieChart },
  setting: {
    name: '图表',
    type: NAME,
    uuid: -1,
    width: 300,
    height: 300,
    left: 0,
    top: 0,
    zoom: 1,
    transform: '',
    radius: 0,
    opacity: 1,
    parent: '-1',
    setting: [],
    opts: {}, // 当前的echart具体某项配置的key以及value
    echartopts: {}, // 当前的echart全部配置
    record: {
      width: 0,
      height: 0,
      minWidth: 10,
      minHeight: 10,
      dir: 'all',
    },
  },
  props: ['params', 'parent'],
  data() {
    return {
      echartOptions: {},
    }
  },
  computed: {
    ...mapGetters(['dActiveElement']),
    width() {
      return Number(this.params.width)
    },
    height() {
      return Number(this.params.height)
    },
  },
  watch: {
    params: {
      async handler(nval) {
        this.changeValues()
      },
      immediate: true,
      deep: true,
    },
  },
  updated() {
    this.updateRecord()
    this.$store.commit('updateRect')
  },

  async mounted() {
    this.updateRecord()
    await this.$nextTick()
    this.params.rotate &&
      (this.$refs.widget.style.transform += `rotate(${this.params.rotate})`)
  },

  async created() {
    try {
      const mypie = await api.echart.getEchart({ chartId: 'doughnut_pie' })
      const data = mypie.data.data
      const option = mypie.option.option
      const mergedOptions = merge(
        {},
        option,
        echarts_comp['doughnut_pie'].default,
      ) // 设置echart option
      mergedOptions.legend.data = data.slice(1).map((item) => item[0]) // 设置echart lengend
      mergedOptions.color = COLORS.slice(0, data.length - 1) // 设置color
      data.slice(1).forEach((item, index) => {
        const [name, value] = item
        mergedOptions.series[0].data = mergedOptions.series[0].data || []
        mergedOptions.series[0].data.push({
          value: value.toString(),
          name,
          label: {
            show: true,
            position: 'outside',
            color: 'inherit',
            formatter: `{b} {c}%`,
            fontSize: 26,
            fontFamily: 'HarmonyOS_Sans_SC_Regular',
          },
          labelLine: {
            show: true,
            length: 15,
            length2: 10,
          },
        })
      })

      this.echartOptions = JSON.parse(JSON.stringify(mergedOptions))
    } catch (error) {
      console.error('获取数据时出错：', error)
      // 处理错误情况
      console.log('error!')
    }
    this.updateWidgetData({
      uuid: this.dActiveElement.uuid,
      key: 'echartopts',
      value: this.echartOptions,
      pushHistory: true,
    })
  },

  methods: {
    ...mapActions(['updateWidgetData']),
    updateRecord() {
      if (this.dActiveElement.uuid === this.params.uuid) {
        let record = this.dActiveElement.record
        record.width = this.$refs.widget.offsetWidth
        record.height = this.$refs.widget.offsetHeight
      }
    },
    changeValues() {
      if (Object.keys(this.params.opts).length !== 0) {
        if (Object.keys(this.echartOptions).length !== 0) {
          let current = this.echartOptions
          const keys = this.params.opts.k.split('.')
          // 遍历属性路径数组，找到目标属性所在的位置
          for (let i = 0; i < keys.length - 1; i++) {
            const key = keys[i]
            current[key] = current[key] || {}
            current = current[key]
          }
          // 将最终属性设为 v
          current[keys[keys.length - 1]] = this.params.opts.v
          console.log(
            'this.echartOptions 已经改变了啊！',
            this.params.opts.k,
            this.params.opts.v,
            this.echartOptions,
          )
        }
      }
    },
  },
}
</script>
