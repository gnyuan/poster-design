<template>
  <div id="w-image-style">
    <el-collapse v-model="activeNames">
      <el-collapse-item title="位置尺寸" name="1">
        <div class="line-layout">
          <number-input
            v-model="innerElement.left"
            label="X"
            @finish="(value) => finish('left', value)"
          />
          <number-input
            v-model="innerElement.top"
            label="Y"
            @finish="(value) => finish('top', value)"
          />
          <number-input
            v-model="innerElement.width"
            style="margin-top: 0.5rem"
            label="宽"
            @finish="(value) => finish('width', value)"
          />
          <number-input
            v-model="innerElement.height"
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
      <el-collapse-item title="样式设计" name="2">
        <div style="flex-wrap: nowrap" class="line-layout">
          <el-switch
            v-model="innerElement.legendshow"
            active-text="展示标题"
            inactive-text="隐藏标题"
            @finish="(value) => finish('legendshow', value)"
          />
        </div>
        <br />
        <div class="slide-wrap">
          <number-slider
            v-model="innerElement.series_radius"
            label="环宽"
            :step="2"
            :maxValue="80"
            @finish="(value) => finish('series_radius', value)"
          />
        </div>
        <br />
        <div class="slide-wrap">
          <number-slider
            v-model="innerElement.opacity"
            label="不透明"
            :step="0.01"
            :maxValue="1"
            @finish="(value) => finish('opacity', value)"
          />
        </div>
      </el-collapse-item>
      <el-collapse-item title="数据" name="3">
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
      <el-collapse-item title="颜色" name="4">
        <template v-for="column in columns" :key="column.key">
          <color-select
            v-model="column.color"
            @finish="(value) => finish('dotColor', value)"
          />
        </template>
      </el-collapse-item>

      <el-collapse-item title="echart配置" name="5">
        <text-input-area
          v-model="innerElement.otheropts"
          :max="40"
          label=""
          @finish="(value) => finish('otheropts', value)"
        />
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

import { ElSwitch, ElInput, ElSlider, ElCollapse } from 'element-plus'
import numberInput from '../../settings/numberInput.vue'
import iconItemSelect from '../../settings/iconItemSelect.vue'
import numberSlider from '../../settings/numberSlider.vue'
import textInputArea from '../../settings/textInputArea.vue'
import colorSelect from '../../settings/colorSelect.vue'

import layerIconList from '@/assets/data/LayerIconList'
import alignIconList from '@/assets/data/AlignListData'

defineOptions({
  name: 'w-image-style',
  inheritAttrs: false,
})

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
  console.log(columns.value)
  console.log(data.value)
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

const activeNames = ref(['1', '2', '3', '4'])
const innerElement = ref({})
const tag = ref(false)
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
const dMoving = computed(() => store.getters.dMoving)

function change() {
  tag.value = true
  innerElement.value = JSON.parse(JSON.stringify(dActiveElement.value))
}

function changeValue() {
  if (tag.value) {
    tag.value = false
    return
  }
  if (dMoving.value) {
    return
  }
  for (let key in innerElement.value) {
    if (ingoreKeys.indexOf(key) !== -1) {
      dActiveElement.value[key] = innerElement.value[key]
    } else if (
      key !== 'setting' &&
      key !== 'record' &&
      innerElement.value[key] !== dActiveElement.value[key]
    ) {
      store.dispatch('updateWidgetData', {
        uuid: dActiveElement.value.uuid,
        key: key,
        value: innerElement.value[key],
      })
    }
  }
}

function finish(key, value) {
  store.dispatch('updateWidgetData', {
    uuid: dActiveElement.value.uuid,
    key: key,
    value: value,
    pushHistory: true,
  })
}
function layerAction(item) {
  console.log(item)
  store.dispatch('updateLayerIndex', {
    uuid: dActiveElement.value.uuid,
    value: item.value,
  })
}
async function alignAction(item) {
  store.dispatch('updateAlign', {
    align: item.value,
    uuid: dActiveElement.value.uuid,
  })
  await nextTick()
  store.commit('updateRect')
}

watch(
  dActiveElement,
  (newValue, oldValue) => {
    change()
    if (newValue.uuid === -1) {
      console.log(4444)
      innerElement.value.cropEdit = false
      store.dispatch('updateWidgetData', {
        uuid: lastUuid.value,
        key: 'cropEdit',
        value: false,
      })
    } else {
      lastUuid.value = newValue.uuid
    }
  },
  { deep: true },
)

watch(
  innerElement,
  (newValue, oldValue) => {
    changeValue()
  },
  { deep: true },
)
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
