<template>
  <div>
    <div
      :id="params.uuid"
      ref="widget"
      :class="['w-qrcode', { 'layer-lock': params.lock }]"
      :style="{
        position: 'absolute',
        left: params.left - parent.left + 'px',
        top: params.top - parent.top + 'px',
        width: params.width + 'px',
        height: params.height + 'px',
        opacity: params.opacity,
      }"
    >
      <!-- <QRCode
        ref="qrcode"
        v-bind="qrCodeOptions"
        :width="width"
        :height="width"
        class="target"
        :image="params.url"
        :value="params.value"
      /> -->
      <div ref="chartRef1" style="height: 100%; width: 100%" />

      <div>aaaa</div>
    </div>
    <div :width="width" :height="width"></div>
  </div>
</template>

<script lang="ts" setup>
const NAME = 'w-qrcode'

import { Ref, ref, onMounted } from 'vue'
import { mapGetters, mapActions } from 'vuex'
import QRCode from '@/components/business/qrcode'

import { EChartsOption } from 'echarts'
import { useECharts } from '@/components/business/echarts'

const chartRef1 = ref<HTMLDivElement | null>(null)
const { setOptions } = useECharts(chartRef1 as Ref<HTMLDivElement>, 'dark')
console.log(111)

const option1: EChartsOption = {
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  },
  yAxis: {
    type: 'value',
  },
  series: [
    {
      data: [159, 230, 224, 218, 135, 147, 260],
      type: 'line',
    },
  ],
}
onMounted(() => {
  setOptions(option1)
})

const parent = { left: 100, top: 100 }
const width = 100
const qrCodeOptions = {
  qrOptions: { typeNumber: 0, mode: 'Byte', errorCorrectionLevel: 'H' },
  // dotsOptions: { color: '#999999' },
  dotsOptions: {
    type: 'classy',
    value: 'nihao',
    color: '#35495E',
    gradient: {
      type: 'linear',
      rotation: 270,
      colorStops: [
        { offset: 0, color: '#35495E' },
        { offset: 1, color: '#35495E' },
      ],
    },
  },
}
const params = {
  name: '二维码',
  type: NAME,
  lock: 4,
  uuid: 'aaabb',
  width: 300,
  height: 300,
  left: 200,
  top: 300,
  zoom: 1,
  transform: '',
  radius: 0,
  opacity: 1,
  parent: '-1',
  url: '',
  dotType: 'classy',
  dotColorType: 'single',
  dotRotation: 270,
  dotColor: '#35495E',
  dotColor2: '#35495E',
  value: 'ccccc',
  setting: [],
  record: {
    width: 0,
    height: 0,
    minWidth: 10,
    minHeight: 10,
    dir: 'all',
  },
}
</script>
