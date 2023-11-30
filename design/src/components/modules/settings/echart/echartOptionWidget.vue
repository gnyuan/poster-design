<template>
  <div class="w-40">
    <div v-if="type === 'number-input'">
      <el-input-number
        v-model="inputValue"
        :min="min"
        :max="max"
        @change="handleChange"
      />
    </div>
    <div v-if="type === 'switch'">
      <el-switch v-model="inputValue" @change="handleChange" />
    </div>
    <div v-if="type === 'input'">
      <el-input v-model="inputValue" @change="handleChange" />
    </div>
    <div v-if="type === 'font-family-selector'">
      <font-family-selector v-model="inputValue" @change="handleChange" />
    </div>
    <div v-if="type === 'color-picker'">
      <el-color-picker
        v-model="inputValue"
        :predefine="predefine"
        @change="handleChange"
      />
    </div>
    <div v-if="type === 'text-align-selector'">
      <icon-item-select :data="textAlignSlector" @finish="handleTextAlign" />
    </div>
    <div v-if="type === 'select'">
      <el-select
        v-model="inputValue"
        class="m-2"
        placeholder="请选择"
        size="large"
        @change="handleChange"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
    </div>
    <div v-if="type === 'slider'">
      <el-slider
        v-model="inputValue"
        :min="min"
        :max="max"
        input-size="small"
        :show-input="true"
        :show-tooltip="false"
        :show-input-controls="false"
        @change="handleChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, computed, nextTick } from 'vue'
import { useStore } from 'vuex'

import fontFamilySelector from './fontFamilySelector.vue'
import iconItemSelect from '../iconItemSelect.vue'
const store = useStore() //  用于保存信息
const dActiveElement = computed(() => store.getters.dActiveElement) // 用户获取信息

const props = defineProps({
  title: String,
  field: String,
  type: String,
  props: {
    type: Object,
    default: () => ({}),
  },
  value: String,
  options: Array,
  emit: Array,
  emitPrefix: String,
  init_echartopts: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['update-options'])

function getValueByPath(obj, path) {
  const keys = path.split('.')
  let value = obj
  for (const key of keys) {
    if (value && typeof value === 'object' && key in value) {
      value = value[key]
    } else {
      value = undefined
      break
    }
  }
  return value
}

const inputValue = ref(getValueByPath(props.init_echartopts, props.field))
console.log(666, typeof inputValue.value, inputValue.value)

const min = ref(props.props?.min || 0)
const max = ref(props.props?.max || 100)
const textAlignSlector = [
  {
    key: 'align',
    icon: 'icon-align-left',
    tip: '左对齐',
    value: 'left',
  },
  {
    key: 'align',
    icon: 'icon-align-center-horiz',
    tip: '水平居中对齐',
    value: 'center',
  },
  {
    key: 'align',
    icon: 'icon-align-right',
    tip: '右对齐',
    value: 'right',
  },
]

// 取色器预设颜色
const predefine = [
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
  '#FFFFFF',
]

// 选项
const options = ref(props.options || [])

console.log('!!!!!!!!!', props.type, props.title, min.value, max.value, props)

// 对于选项，如果这里设置有初始值
if (props.value !== undefined) {
  inputValue.value = props.value
}
async function handleChange() {
  console.log(props.type, props.field, inputValue.value)
  // 处理是否展示画布
  if (
    props.type === 'switch' &&
    props.field === 'cache.chart.backgroundColor.show'
  ) {
    if (inputValue.value) {
      const bgColor =
        dActiveElement.value.echartopts.cache.chart.backgroundColor.color
      emit('update-options', 'backgroundColor', bgColor)
    } else {
      // 不展示则保存画布颜色，并把画布置为#00000000
      console.log('morga ', dActiveElement.value)
      emit(
        'update-options',
        'cache.chart.backgroundColor.color',
        dActiveElement.value.echartopts.backgroundColor || '#FFFFFFFF',
      )
      await nextTick()
      emit('update-options', 'backgroundColor', '#00000000')
    }
    return
  }
  // 处理选择画布颜色
  if (
    props.type === 'color-picker' &&
    props.field === 'cache.chart.backgroundColor.color'
  ) {
    console.log(inputValue.value, '666666')
    emit(
      'update-options',
      'cache.chart.backgroundColor.color',
      inputValue.value,
    )
    await nextTick()
    emit('update-options', 'backgroundColor', inputValue.value)
    return
  }

  // 处理图例位置
  if (
    props.type === 'select' &&
    props.field === 'cache.chart.legend.location'
  ) {
    console.log('hello', props.value, inputValue.value)
    // 设置所有图例位置属性为 null
    emit('update-options', 'legend.show', null)
    await nextTick()
    emit('update-options', 'legend.orient', null)
    await nextTick()
    emit('update-options', 'legend.left', null)
    await nextTick()
    emit('update-options', 'legend.top', null)
    await nextTick()
    emit('update-options', 'legend.right', null)
    await nextTick()
    emit('update-options', 'legend.bottom', null)
    await nextTick()
    emit('update-options', 'legend.show', true)
    await nextTick()

    switch (inputValue.value) {
      case 'top-left':
        emit('update-options', 'legend.orient', 'horizontal')
        await nextTick()
        emit('update-options', 'legend.left', 10)
        await nextTick()
        emit('update-options', 'legend.top', 10)
        await nextTick()
        break

      case 'top-center':
        emit('update-options', 'legend.orient', 'horizontal')
        await nextTick()
        emit('update-options', 'legend.left', 'center')
        await nextTick()
        emit('update-options', 'legend.top', 10)
        await nextTick()
        break

      case 'top-right':
        emit('update-options', 'legend.orient', 'horizontal')
        await nextTick()
        emit('update-options', 'legend.right', 10)
        await nextTick()
        emit('update-options', 'legend.top', 10)
        await nextTick()
        break

      case 'bottom-left':
        emit('update-options', 'legend.orient', 'horizontal')
        await nextTick()
        emit('update-options', 'legend.left', 10)
        await nextTick()
        emit('update-options', 'legend.bottom', 70)
        await nextTick()
        break

      case 'bottom-center':
        emit('update-options', 'legend.orient', 'horizontal')
        await nextTick()
        emit('update-options', 'legend.left', 'center')
        await nextTick()
        emit('update-options', 'legend.bottom', 70)
        await nextTick()
        break

      case 'bottom-right':
        emit('update-options', 'legend.orient', 'horizontal')
        await nextTick()
        emit('update-options', 'legend.right', 10)
        await nextTick()
        emit('update-options', 'legend.bottom', 70)
        await nextTick()
        break

      default:
        console.log('no legend position choice.')
        break
    }
    return
  }
  console.log('impossible!!!!!')

  emit('update-options', props.field, inputValue.value)
}

function handleTextAlign(item) {
  console.log(props.field, inputValue.value)
  emit('update-options', props.field, item.value)
}

// Update the min, max, step values on component initialization
onBeforeMount(() => {
  min.value = props.props?.min || 0
  max.value = props.props?.max || Infinity
})
</script>
