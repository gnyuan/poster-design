<template>
  <div
    ref="pieDom"
    style="height: 100%; width: 100%"
    :height="height"
    :width="width"
  />
</template>

<script lang="ts" setup>
import { onMounted, ref, Ref, watch, nextTick } from 'vue'
import { debounce } from 'throttle-debounce'
import { EChartsOption } from 'echarts'
import { useECharts } from '@/components/business/echarts'

const props = defineProps({
  width: { type: Number, default: 300 },
  height: { type: Number, default: 300 },
  opts: { type: Object as () => EChartsOption, default: {} },
})

const pieDom = ref<HTMLElement>()
const { setOptions, resize } = useECharts(pieDom as Ref<HTMLDivElement>, 'dark')

watch(
  () => [props.width, props.height],
  () => {
    render()
  },
)
watch(
  () => props.opts,
  (newVal, oldVal) => {
    render()
  },
  { deep: true },
)

const render = debounce(300, false, async () => {
  console.log('要进行渲染了！！因为height width 或者opts变动', props.opts)
  setOptions(props.opts)
  await nextTick()
  await resize()
})

onMounted(() => {
  render()
})
</script>
