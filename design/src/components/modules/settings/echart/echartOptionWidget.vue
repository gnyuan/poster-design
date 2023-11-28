<template>
  <div>
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
      <el-color-picker v-model="inputValue" @change="handleChange" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, onBeforeMount, reactive } from 'vue'
import { ElInputNumber, ElSwitch, ElInput, ElColorPicker } from 'element-plus'
import fontFamilySelector from './fontFamilySelector.vue'

const props = defineProps({
  field: String,
  type: String,
  init_echartopts: {
    type: Object,
    default: () => ({}),
  },
  props: {
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
  console.log('hhhh', obj, path, value)
  return value
}

const inputValue = ref(getValueByPath(props.init_echartopts, props.field))

const min = ref(props.props?.min || 0)
const max = ref(props.props?.max || Infinity)

function handleChange() {
  console.log('in handle change.', props.field, inputValue.value)
  emit('update-options', props.field, inputValue.value)
}

// Update the min, max, step values on component initialization
onBeforeMount(() => {
  console.log(1111)
  min.value = props.props?.min || 0
  max.value = props.props?.max || Infinity
})
</script>
