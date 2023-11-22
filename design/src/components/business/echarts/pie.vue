<template>
  <div
    ref="pieDom"
    style="height: 100%; width: 100%"
    :height="height"
    :width="width"
  />
</template>

<script lang="ts" setup>
import { onMounted, ref, Ref, watch, nextTick, defineExpose } from 'vue'
import { debounce } from 'throttle-debounce'
import { EChartsOption } from 'echarts'
import { useECharts } from '@/components/business/echarts'

const props = defineProps({
  width: { type: Number, default: 300 },
  height: { type: Number, default: 300 },
  opts: {
    type: Object as () => EChartsOption,
    default: {
      animation: false,
      tooltip: {
        trigger: 'item',
      },
      legend: {
        top: '5%',
        left: 'center',
        show: true,
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
    } as EChartsOption,
  },
})

const pieDom = ref<HTMLElement>()
const { setOptions, resize } = useECharts(pieDom as Ref<HTMLDivElement>, 'dark')

watch(
  () => [props.width, props.height, props.opts],
  () => {
    render()
  },
)

const render = debounce(300, false, async () => {
  console.log('要进行渲染了！！因为height width 或者opts变动')
  console.log(props.opts)
  setOptions(props.opts)
  resize()
})

onMounted(() => {
  render()
})

defineExpose({ pieDom })
</script>
