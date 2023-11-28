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
import { EChartsOption } from 'echarts'
import { merge } from 'lodash-es'
import api from '@/api'
import PieChart from '@/components/business/echarts/pie.ts'

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
    name: '饼图',
    type: NAME,
    uuid: -1,
    width: 300,
    height: 300,
    left: 0,
    top: 0,
    legendshow: true, // 是否展示图例
    series_radius: 40, // 环宽度
    zoom: 1,
    transform: '',
    radius: 0,
    opacity: 1,
    parent: '-1',
    setting: [],
    opts: {},
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
    ...mapGetters(['dActiveElement', 'dZoom']),
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
      // console.log(mypie.data)
      // console.log(mypie.option)
      const data = mypie.data.data
      const option = mypie.option.option
      const default_option = {
        backgroundColor: '#FFFFFF',
        title: [{ top: '3%' }, { top: '96%', right: '5%', left: null }],
        grid: {
          top: '20%',
          bottom: '15%',
          left: '10%',
          right: '12%',
          containLabel: true,
        },
        legend: {
          bottom: '14.4%',
          left: 'center',
          itemGap: 15,
          textStyle: {
            rich: {
              a: {
                fontSize: 24,
                align: 'left',
                width: 100,
                fontFamily: 'HarmonyOS_Sans_SC_Regular',
              },
              b: {
                fontSize: 24,
                align: 'right',
                fontFamily: 'HarmonyOS_Sans_SC_Regular',
              },
            },
          },
          icon: 'roundRect',
          orient: 'horizontal',
          top: '90%',
        },

        series: [
          {
            name: '访问来源',
            animation: false,
            type: 'pie',
            clockwise: true,
            radius: ['25%', '70%'],
            center: ['50%', '50%'],
            startAngle: 90,
            labelLine: {
              show: true,
              length: 15,
              length2: 10,
              smooth: 0.5,
            },
            itemStyle: {
              borderRadius: 3,
              borderColor: '#ffffff',
              borderWidth: 2,
            },
            animationEasing: 'sinusoidalOut',
            animationDuration: 2000,
            animationDelay: 0,
          },
        ],
      }
      const mergedOptions = merge({}, option, default_option) // 设置echart option
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

      console.log('!!!!!!!!', mergedOptions)

      this.echartOptions = mergedOptions
    } catch (error) {
      console.error('获取数据时出错：', error)
      // 处理错误情况
      console.log('error!')
    }
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
          console.log('can??')
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

          console.log(this.echartOptions)
          console.log('this.echartOptions 已经改变了啊！')
        }
      }
      console.log('must end')
    },
  },
}
</script>
