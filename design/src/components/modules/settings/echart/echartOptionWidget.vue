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
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, onBeforeMount, reactive } from 'vue'
import { ElInputNumber, ElSwitch, ElInput } from 'element-plus'

const props = defineProps({
  field: String,
  type: String,
  // default: null,
  init_value: null,
  props: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['update-options'])

const inputValue = ref(props.init_value)
// const inputValue = ref(props.default || 0)
// console.log('my default', props.default, inputValue.value)

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
