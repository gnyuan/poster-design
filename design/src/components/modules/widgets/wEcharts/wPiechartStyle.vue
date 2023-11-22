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
        </div>
      </el-collapse-item>
      <el-collapse-item title="样式设计" name="2">
        <div style="flex-wrap: nowrap" class="line-layout">
          <el-switch
            v-model="innerElement.legendshow"
            active-text="展示标题"
            inactive-text="隐藏标题"
            @finish="(value) => finish('legendshow', value)"
          >
          </el-switch>
        </div>

        <div style="flex-wrap: nowrap" class="line-layout">
          <el-select v-model="innerElement.dotColorType">
            <el-option
              v-for="ctype in localization.dotColorTypes"
              :key="ctype.key"
              :label="ctype.value"
              :value="ctype.key"
            />
          </el-select>
          <el-select v-model="innerElement.dotType" class="selector">
            <el-option
              v-for="dtype in localization.dotTypes"
              :key="dtype.key"
              :label="dtype.value"
              :value="dtype.key"
            />
          </el-select>
        </div>
        <div style="flex-wrap: nowrap; margin-top: 1rem" class="line-layout">
          <color-select
            v-model="innerElement.dotColor"
            @finish="(value) => finish('dotColor', value)"
          />
          <color-select
            v-show="innerElement.dotColorType !== 'single'"
            v-model="innerElement.dotColor2"
            @finish="(value) => finish('dotColor2', value)"
          />
        </div>
        <number-slider
          v-show="innerElement.dotColorType !== 'single'"
          v-model="innerElement.dotRotation"
          style="margin-top: 8px"
          label="渐变角度"
          :step="1"
          :minValue="0"
          :maxValue="360"
          @finish="(value) => finish('dotRotation', value)"
        />
      </el-collapse-item>
      <el-collapse-item title="内容设置" name="3">
        <text-input-area
          v-model="innerElement.value"
          :max="40"
          label=""
          @finish="(value) => finish('value', value)"
        />
        <br />
        <div class="slide-wrap logo__layout">
          <img v-show="innerElement.url" :src="innerElement.url" class="logo" />
          <uploader class="options__upload" @done="uploadImgDone">
            <el-button size="small" plain>{{
              innerElement.url ? '替换图片' : '上传 Logo'
            }}</el-button>
          </uploader>
          <el-button
            v-show="innerElement.url"
            size="small"
            link
            @click="finish('url', '')"
            >删除</el-button
          >
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
import { computed, nextTick, watch, watchEffect, ref } from 'vue'
import { useStore } from 'vuex'

import { ElSelect, ElOption, ElSwitch } from 'element-plus'
import numberInput from '../../settings/numberInput.vue'
import iconItemSelect from '../../settings/iconItemSelect.vue'
import numberSlider from '../../settings/numberSlider.vue'
import textInputArea from '../../settings/textInputArea.vue'
import colorSelect from '../../settings/colorSelect.vue'

import api from '@/api'
import localization from '@/assets/data/QrCodeLocalization'
import uploader from '@/components/common/Uploader/index.vue'
import layerIconList from '@/assets/data/LayerIconList'
import alignIconList from '@/assets/data/AlignListData'

defineOptions({
  name: 'w-image-style',
  inheritAttrs: false,
})

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
    console.log(key, innerElement.value[key])
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
      console.log(key, innerElement.value[key], dActiveElement.value.uuid)
    }
  }
}

function finish(key, value) {
  console('laotie', key, value)
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
async function uploadImgDone(img) {
  store.commit('setShowMoveable', false)
  await api.material.addMyPhoto(img)
  innerElement.value.url = img.url
  store.commit('setShowMoveable', true)
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

// change()
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
