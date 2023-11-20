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
      ref="qrcode"
      v-bind="echartOptions"
      :width="width"
      :height="height"
      class="target"
    />
  </div>
</template>

<script>
// 图片组件
const NAME = 'w-piechart'

import { mapGetters, mapActions } from 'vuex'
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
      echartOptions: {
        xAxis: {
          type: 'category',
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            data: [1990, 230, 224, 218, 135, 147, 260],
            type: 'line',
          },
        ],
      },
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
      this.pieOptions = {
        qrOptions: { typeNumber: 0, mode: 'Byte', errorCorrectionLevel: 'H' },
        // dotsOptions: { color: '#999999' },
        dotsOptions: {
          type: this.params.dotType,
          color: this.params.dotColor,
          gradient: {
            type: 'linear',
            rotation: this.params.dotRotation,
            colorStops: [
              { offset: 0, color: this.params.dotColor },
              {
                offset: 1,
                color:
                  this.params.dotColorType === 'single'
                    ? this.params.dotColor
                    : this.params.dotColor2,
              },
            ],
          },
        },
      }
    },
  },
}
</script>
