<template>
  <div class="w-40">
    <div v-if="type === 'number-input'">
      <el-input-number
        v-model="inputValue"
        :min="min"
        :max="max"
        @change="handleNumberInput"
      />
    </div>
    <div v-if="type === 'switch'">
      <el-switch v-model="inputValue" @change="handleSwitch" />
    </div>
    <div v-if="type === 'input'">
      <el-input v-model="inputValue" @change="handleInput" />
    </div>
    <div v-if="type === 'font-family-selector'">
      <font-family-selector
        v-model="inputValue"
        @change="handleFontFaimlySelector"
      />
    </div>
    <div v-if="type === 'color-picker'">
      <el-color-picker
        v-model="inputValue"
        :predefine="predefine"
        @change="handleColorPicker"
      />
    </div>
    <div v-if="type === 'color-picker2'">
      <template v-for="(item, index) in inputValue" :key="index">
        <el-color-picker
          v-model="inputValue[index]"
          :predefine="predefine"
          @change="handleColorPicker2(index)"
        />
      </template>
    </div>
    <div v-if="type === 'text-align-selector'">
      <icon-item-select
        :data="textAlignSlector"
        @finish="handleTextAlignSelector"
      />
    </div>
    <div v-if="type === 'select'">
      <el-select
        v-model="inputValue"
        class="m-2"
        placeholder="请选择"
        size="large"
        @change="handleSelect"
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
        @change="handleSlider"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, toRefs } from 'vue'
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
  value: {
    type: null,
  },
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

const { value } = toRefs(props)
const inputValue = ref(getValueByPath(props.init_echartopts, props.field))
// 对于选项，如果数据库没有，也就是从对象经过路径解码出来的没有，则用默认的props.value
if (inputValue.value === undefined) {
  inputValue.value = value.value
}

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

async function handleNumberInput() {
  if (props.field === 'cache.chart.series.label.fontSize') {
    for (
      let i = 0;
      i < dActiveElement.value.echartopts.series[0].data.length;
      i++
    ) {
      await emit(
        'update-options',
        `series.0.data.${i}.label.fontSize`,
        inputValue.value,
      )
      await nextTick()
    }
  } else {
    console.log('other', props.field)
  }
  await emit('update-options', props.field, inputValue.value)
  await nextTick()
}

let is_first_enter_percent = true
async function handleSwitch() {
  if (props.field === 'cache.chart.backgroundColor.show') {
    if (inputValue.value) {
      const bgColor =
        dActiveElement.value.echartopts.cache.chart.backgroundColor.color
      await emit('update-options', 'backgroundColor', bgColor)
    } else {
      // 不展示则保存画布颜色，并把画布置为#00000000
      await emit(
        'update-options',
        'cache.chart.backgroundColor.color',
        dActiveElement.value.echartopts.backgroundColor || '#FFFFFFFF',
      )
      await emit('update-options', 'backgroundColor', '#00000000')
    }
  } else if (props.field === 'cache.chart.series.label.show') {
    for (
      let i = 0;
      i < dActiveElement.value.echartopts.series[0].data.length;
      i++
    ) {
      await emit(
        'update-options',
        `series.0.data.${i}.label.show`,
        inputValue.value,
      )
    }
  } else if (props.field === 'cache.sundry.dataFormat.percent') {
    console.log(is_first_enter_percent, inputValue.value)
    if (!is_first_enter_percent && inputValue.value === false) {
      for (
        let i = 0;
        i < dActiveElement.value.echartopts.series[0].data.length;
        i++
      ) {
        await emit(
          'update-options',
          `series.0.data.${i}.value`,
          String(
            parseFloat(dActiveElement.value.echartopts.series[0].data[i].value),
          ),
        )
      }
    }
    if (inputValue.value === true) {
      for (
        let i = 0;
        i < dActiveElement.value.echartopts.series[0].data.length;
        i++
      ) {
        await emit(
          'update-options',
          `series.0.data.${i}.value`,
          String(
            parseFloat(
              dActiveElement.value.echartopts.series[0].data[i].value,
            ) * 100,
          ),
        )
      }
    }
    if (is_first_enter_percent) {
      is_first_enter_percent = false
    }
  } else if (props.field === 'cache.chart.series.clockwise') {
    await emit('update-options', `series.0.clockwise`, inputValue.value)
  } else if (props.field === 'cache.chart.series.labelLine.show') {
    console.log('cache.chart.series.labelLine.show')
  } else if (props.field === 'cache.chart.series.bar.label.show') {
    for (let i = 0; i < dActiveElement.value.echartopts.series.length; i++) {
      if (dActiveElement.value.echartopts.series[i].type === 'bar')
        await emit('update-options', `series.${i}.label.show`, inputValue.value)
    }
  } else if (props.field === 'cache.chart.series.line.label.show') {
    for (let i = 0; i < dActiveElement.value.echartopts.series.length; i++) {
      if (dActiveElement.value.echartopts.series[i].type === 'line')
        await emit('update-options', `series.${i}.label.show`, inputValue.value)
    }
  } else {
    console.log('pass')
  }
  await emit('update-options', props.field, inputValue.value)
}

async function handleInput() {
  if (props.field === 'cache.chart.series.label.formatter') {
    for (
      let i = 0;
      i < dActiveElement.value.echartopts.series[0].data.length;
      i++
    ) {
      await emit(
        'update-options',
        `series.0.data.${i}.label.formatter`,
        inputValue.value,
      )
      await nextTick()
    }
  }
  await emit('update-options', props.field, inputValue.value)
}

async function handleFontFaimlySelector() {
  if (props.field === 'cache.chart.series.label.fontFamily') {
    for (
      let i = 0;
      i < dActiveElement.value.echartopts.series[0].data.length;
      i++
    ) {
      await emit(
        'update-options',
        `series.0.data.${i}.label.fontFamily`,
        inputValue.value,
      )
      await nextTick()
    }
  }
  await emit('update-options', props.field, inputValue.value)
}

async function handleColorPicker() {
  if (props.field === 'cache.chart.backgroundColor.color') {
    await emit('update-options', 'backgroundColor', inputValue.value)
  } else if (props.field === 'cache.chart.series.itemStyle.borderColor') {
    await emit(
      'update-options',
      'series.0.itemStyle.borderColor',
      inputValue.value,
    )
    await nextTick()
  } else {
    console.log('no opitons')
  }
  await emit('update-options', props.field, inputValue.value)
}

async function handleColorPicker2(index) {
  if (props.field === 'cache.chart.legend.color') {
    // 扇形颜色
    await emit('update-options', `color.${index}`, inputValue.value[index])
    await nextTick()
    await emit(
      'update-options',
      `series.${index}.color`,
      inputValue.value[index],
    )
    await nextTick()
  } else {
    console.log('pass!')
  }
  await emit('update-options', props.field, inputValue.value)
}

async function handleSelect() {
  if (props.field === 'cache.chart.legend.location') {
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
  } else if (props.field === 'cache.sundry.dataFormat.dataDecimal') {
    if (inputValue.value === 'default' || inputValue.value === 'two') {
      for (
        let i = 0;
        i < dActiveElement.value.echartopts.series[0].data.length;
        i++
      ) {
        await emit(
          'update-options',
          `series.0.data.${i}.value`,
          String(
            parseFloat(
              dActiveElement.value.echartopts.series[0].data[i].value,
            ).toFixed(2),
          ),
        )
      }
    } else if (inputValue.value === 'one') {
      for (
        let i = 0;
        i < dActiveElement.value.echartopts.series[0].data.length;
        i++
      ) {
        await emit(
          'update-options',
          `series.0.data.${i}.value`,
          String(
            parseFloat(
              dActiveElement.value.echartopts.series[0].data[i].value,
            ).toFixed(1),
          ),
        )
      }
    } else if (inputValue.value === 'ZahlenQ') {
      for (
        let i = 0;
        i < dActiveElement.value.echartopts.series[0].data.length;
        i++
      ) {
        await emit(
          'update-options',
          `series.0.data.${i}.value`,
          String(
            Math.abs(
              parseFloat(
                dActiveElement.value.echartopts.series[0].data[i].value,
              ),
            ),
          ),
        )
      }
    } else {
      console.log('no this option', inputValue.value)
    }
    await nextTick()
  } else if (props.field === 'cache.chart.legend.icon') {
    await emit('update-options', `legend.icon`, inputValue.value)
    await nextTick()
  } else {
    console.log('other')
  }
  await emit('update-options', props.field, inputValue.value)
}

async function handleSlider() {
  if (props.field === 'cache.chart.series.startAngle') {
    await emit('update-options', `series.0.startAngle`, inputValue.value)
    await nextTick()
  } else if (props.field === 'cache.chart.series.radius.0') {
    await emit('update-options', `series.0.radius.0`, `${inputValue.value}%`)
    await nextTick()
  } else if (props.field === 'cache.chart.series.itemStyle.borderWidth') {
    await emit(
      'update-options',
      'series.0.itemStyle.borderWidth',
      inputValue.value,
    )
    await nextTick()
  } else if (props.field === 'cache.chart.series.itemStyle.borderRadius') {
    await emit(
      'update-options',
      'series.0.itemStyle.borderRadius',
      inputValue.value,
    )
    await nextTick()
  } else {
    console.log('no this option', inputValue.value)
  }
  await emit('update-options', props.field, inputValue.value)
}

function handleTextAlignSelector(item) {
  emit('update-options', props.field, item.value)
}
</script>
