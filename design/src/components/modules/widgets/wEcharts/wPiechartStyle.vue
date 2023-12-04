<template>
  <div id="w-piechart-style">
    <el-collapse v-model="activeNames">
      <el-collapse-item title="位置尺寸" name="位置尺寸">
        <div class="line-layout">
          <number-input
            v-model="dActiveElement.left"
            label="X"
            @finish="(value) => finish('left', value)"
          />
          <number-input
            v-model="dActiveElement.top"
            label="Y"
            @finish="(value) => finish('top', value)"
          />
          <number-input
            v-model="dActiveElement.width"
            style="margin-top: 0.5rem"
            label="宽"
            @finish="(value) => finish('width', value)"
          />
          <number-input
            v-model="dActiveElement.height"
            style="margin-top: 0.5rem"
            label="高"
            @finish="(value) => finish('height', value)"
          />
          <br />
        </div>
        <el-input :value="dActiveElement.uuid">
          <template #prepend>UUID</template>
        </el-input>
      </el-collapse-item>
      <template
        v-for="(section, sectionindex) in optionList"
        :key="sectionindex"
      >
        <el-collapse-item :title="section.name" :name="section.name">
          <div
            v-for="(item, index) in section.items"
            :key="index"
            class="setting-option flex items-center justify-between"
          >
            <div class="flex items-center">{{ item.title }}</div>
            <div class="flex items-center">
              <echart-option-widget
                :key="index"
                :title="item.title"
                :field="item.field"
                :type="item.type"
                :props="item.props"
                :options="item.options || []"
                :value="item.value"
                :emit="item.emit || []"
                :emitPrefix="item.emitPrefix"
                :init_echartopts="dActiveElement.echartopts"
                @update-options="updateEchartsOptions"
              />
            </div>
          </div>
        </el-collapse-item>
      </template>
      <el-collapse-item title="数据" name="数据">
        <table>
          <thead>
            <tr>
              <th
                v-for="column in columns"
                :key="column.key"
                @click="addColumn(column)"
              >
                <el-input v-model="column.title"></el-input>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(row, index) in data"
              :key="index"
              @click="addRow(index)"
            >
              <td v-for="column in columns" :key="column.key">
                <el-input v-model="row[column.key]"></el-input>
              </td>
            </tr>
          </tbody>
        </table>
      </el-collapse-item>
      <br />
      <icon-item-select
        class="style-item"
        label=""
        :data="layerIconList"
        @finish="layerAction"
      />
      <icon-item-select :data="alignIconList" @finish="alignAction" />
      <br />
    </el-collapse>
  </div>
</template>

<script lang="ts" setup>
import { computed, nextTick, watch, ref } from 'vue'
import { useStore } from 'vuex'

import { ElSwitch, ElInput, ElCollapse } from 'element-plus'
import numberInput from '../../settings/numberInput.vue'
import iconItemSelect from '../../settings/iconItemSelect.vue'

import echartOptionWidget from '../../settings/echart/echartOptionWidget.vue'

import layerIconList from '@/assets/data/LayerIconList'
import alignIconList from '@/assets/data/AlignListData'

import { echarts_comp } from './echartsettings'

defineOptions({
  name: 'w-piechart-style',
  inheritAttrs: false,
})

const chart_type_id = 'group_line_bar' // doughnut_pie   group_line_bar
const optionList = ref(
  Object.entries(echarts_comp[chart_type_id][0].props.forms)
    .filter(([key, value]) => key !== 'name' && key !== 'group') // 过滤掉键为'name'的项
    .map(([key, value]) => value),
) // 映射为包含键值对的对象

function updateEchartsOptions(option_path, option_value) {
  store.dispatch('updateWidgetData', {
    uuid: dActiveElement.value.uuid,
    key: 'opts',
    value: { k: option_path, v: option_value },
    pushHistory: true,
  })
}

const columns = ref([
  { key: 'c1', title: '系列1', color: '#7a5050ff' },
  { key: 'c2', title: '系列2', color: '#9c1313ff' },
])
const data = ref([
  { c1: 10, c2: 5 },
  { c1: 13, c2: 6 },
  { c1: 14, c2: 7 },
])

const addRow = (index) => {
  if (index === data.value.length - 1) {
    const newRow = {} // Create a new row
    columns.value.forEach((column) => {
      newRow[column.key] = ''
    })
    data.value.push(newRow)
  }
}

const addColumn = (clickedColumn) => {
  const lastColumn = columns.value[columns.value.length - 1]
  if (clickedColumn === lastColumn) {
    const newIndex = columns.value.length + 1
    const newKey = `c${newIndex}`
    const newTitle = `系列${newIndex}`
    columns.value.push({ key: newKey, title: newTitle })

    data.value.forEach((row) => {
      row[newKey] = ''
    })
  }
}

const activeNames = ref([
  '位置尺寸',
  '文本设置',
  '动画设置',
  '图表设置',
  '数据格式',
  '更多设置',
])
// const activeNames = ref(['动画设置'])
const lastUuid = ref(-1)
const ingoreKeys = [
  'left',
  'top',
  'name',
  'width',
  'height',
  'radiusTopLeft',
  'radiusTopRight',
  'radiusBottomLeft',
  'radiusBottomRight',
]
const store = useStore()
const dActiveElement = computed(() => store.getters.dActiveElement)
// const dMoving = computed(() => store.getters.dMoving)

function finish(key, value) {
  if (!ingoreKeys.includes(key)) {
    store.dispatch('updateWidgetData', {
      uuid: dActiveElement.value.uuid,
      key: key,
      value: value,
      pushHistory: true,
    })
  } else {
    console.log(
      `The property '${key}' is in the ingoreKeys list and won't be updated.`,
    )
  }
}
async function layerAction(item) {
  store.dispatch('updateLayerIndex', {
    uuid: dActiveElement.value.uuid,
    value: item.value,
  })
  // TODO updateRect 需要在窗口大小变动的时候执行
}
async function alignAction(item) {
  store.dispatch('updateAlign', {
    align: item.value,
    uuid: dActiveElement.value.uuid,
  })
  await nextTick()
  store.commit('updateRect')
}
</script>

<style lang="less" scoped>
.slide-wrap {
  width: 100%;
  padding: 16px;
  background: #f3f5f7;
  border-radius: 6px;
}
#w-image-style {
  height: 100%;
  width: 100%;
}
.line-layout {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
  width: 100%;
}
.style-item {
  margin-bottom: 10px;
}
.setting-list {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
  width: 100%;
}
.options {
  // margin-bottom: 0.7rem;
  &__upload {
    width: auto;
    // margin-left: 10px;
    display: inline-block;
  }
}

.selector {
  width: 340px;
  transform: scale(0.94);
}
.logo__layout {
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.logo {
  height: 40px;
}
</style>
