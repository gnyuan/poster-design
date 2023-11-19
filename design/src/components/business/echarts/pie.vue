<template>
  <div
    ref="pieDom"
    style="height: 100%; width: 100%"
    :height="300"
    :width="400"
  />
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, Ref, watch, nextTick } from 'vue'
import { debounce } from 'throttle-debounce'
import { EChartsOption } from 'echarts'
import { useECharts } from '@/components/business/echarts'

export default defineComponent({
  props: {
    width: {
      default: 300,
    },
    height: {
      default: 300,
    },
    echartOptions: {
      default: () =>
        ({
          xAxis: {
            type: 'category',
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          },
          yAxis: {
            type: 'value',
          },
          series: [
            {
              data: [150, 230, 224, 218, 135, 147, 260],
              type: 'line',
            },
          ],
        } as EChartsOption),
      type: Object as () => EChartsOption,
    },
  },
  setup(props) {
    watch(
      () => [props.width, props.height, props.echartOptions],
      () => {
        render()
      },
    )

    const render = debounce(300, false, async () => {
      setOptions(props.echartOptions)
    })

    const pieDom = ref<HTMLElement>()
    const { setOptions } = useECharts(pieDom as Ref<HTMLDivElement>, 'dark')
    onMounted(() => {
      render()
    })

    return {
      pieDom,
    }
  },
})
</script>
