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
      :width="width"
      :height="height"
      class="target"
    />
  </div>
</template>

<script lang="ts">
// 图片组件
const NAME = 'w-piechart'

import { mapGetters, mapActions } from 'vuex'
import { EChartsOption } from 'echarts'
import PieChart from '@/components/business/echarts/pie.ts'

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
    legendshow: true,
    zoom: 1,
    transform: '',
    radius: 0,
    opacity: 1,
    parent: '-1',
    setting: [],
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
  methods: {
    ...mapActions(['updateWidgetData']),
    updateRecord() {
      if (this.dActiveElement.uuid === this.params.uuid) {
        let record = this.dActiveElement.record
        record.width = this.$refs.widget.offsetWidth
        record.height = this.$refs.widget.offsetHeight
      }
      // this.updateZoom()
    },
    changeValues() {
      console.log(5656)
      console.log(this.params)
      this.echartOptions = {
        animation: false,
        tooltip: {
          trigger: 'item',
        },
        legend: {
          top: '5%',
          left: 'center',
          show: this.params.legendshow,
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2,
            },
            label: {
              show: false,
              position: 'center',
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 40,
                fontWeight: 'bold',
              },
            },
            labelLine: {
              show: false,
            },
            data: [
              { value: 1048, name: 'Search Engine' },
              { value: 735, name: 'Direct' },
              { value: 580, name: 'Email' },
              { value: 484, name: 'Union Ads' },
              { value: 300, name: 'Video Ads' },
            ],
          },
        ],
      } as EChartsOption
    },
  },
}
</script>
