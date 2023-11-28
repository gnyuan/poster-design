<template>
  <el-select v-model="selectedFont" @change="handleFontChange">
    <el-option
      v-for="font in fontOptions"
      :key="font.name"
      :label="font.label"
      :value="font.name"
    ></el-option>
  </el-select>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import { debounce } from 'lodash-es'
import { ElSelect, ElOption } from 'element-plus'

export default {
  components: {
    ElSelect,
    ElOption,
  },
  props: {
    modelValue: {
      default: undefined,
    },
  },
  emits: ['update:modelValue', 'change'],
  setup(props, { emit }) {
    const selectedFont = ref(props.modelValue)
    const fontOptions = [
      { name: 'Arial', label: 'Arial' },
      { name: 'Helvetica', label: 'Helvetica' },
      // Add more font options here
    ]

    const handleFontChange = debounce(() => {
      emit('update:modelValue', selectedFont.value)
      emit('change', selectedFont.value)
    }, 300)

    onMounted(() => {
      selectedFont.value = props.modelValue
    })

    return {
      selectedFont,
      fontOptions,
      handleFontChange,
    }
  },
}
</script>
