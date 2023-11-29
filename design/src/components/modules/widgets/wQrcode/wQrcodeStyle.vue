<!--
 * @Author: ShawnPhang
 * @Date: 2021-08-09 11:41:53
 * @Description: 
 * @LastEditors: ShawnPhang <site: book.palxp.com>
 * @LastEditTime: 2023-06-29 17:53:23
-->
<template>
  <div id="w-qrcode-style">
    <el-collapse v-if="!dMoving" v-model="activeNames">
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
        </div>
      </el-collapse-item>
      <el-collapse-item title="样式设计" name="样式设计">
        <div style="flex-wrap: nowrap" class="line-layout">
          <el-select v-model="dActiveElement.dotColorType">
            <el-option
              v-for="ctype in localization.dotColorTypes"
              :key="ctype.key"
              :label="ctype.value"
              :value="ctype.key"
            />
          </el-select>
          <el-select v-model="dActiveElement.dotType" class="selector">
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
            v-model="dActiveElement.dotColor"
            @finish="(value) => finish('dotColor', value)"
          />
          <color-select
            v-show="dActiveElement.dotColorType !== 'single'"
            v-model="dActiveElement.dotColor2"
            @finish="(value) => finish('dotColor2', value)"
          />
        </div>
        <number-slider
          v-show="dActiveElement.dotColorType !== 'single'"
          v-model="dActiveElement.dotRotation"
          style="margin-top: 8px"
          label="渐变角度"
          :step="1"
          :minValue="0"
          :maxValue="360"
          @finish="(value) => finish('dotRotation', value)"
        />
      </el-collapse-item>
      <el-collapse-item title="内容设置" name="内容设置">
        <text-input-area
          v-model="dActiveElement.value"
          :max="40"
          label=""
          @finish="(value) => finish('value', value)"
        />
        <br />
        <div class="slide-wrap logo__layout">
          <img
            v-show="dActiveElement.url"
            :src="dActiveElement.url"
            class="logo"
          />
          <uploader class="options__upload" @done="uploadImgDone">
            <el-button size="small" plain>{{
              dActiveElement.url ? '替换图片' : '上传 Logo'
            }}</el-button>
          </uploader>
          <el-button
            v-show="dActiveElement.url"
            size="small"
            link
            @click="finish('url', '')"
            >删除</el-button
          >
        </div>
        <br />
        <div class="slide-wrap">
          <number-slider
            v-model="dActiveElement.opacity"
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

<script>
// 二维码组件样式
const NAME = 'w-qrcode-style'
import { mapGetters, mapActions } from 'vuex'
import { ElSelect, ElOption } from 'element-plus'
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

export default {
  name: NAME,
  components: {
    ElSelect,
    ElOption,
    numberInput,
    numberSlider,
    iconItemSelect,
    textInputArea,
    colorSelect,
    uploader,
  },
  data() {
    return {
      activeNames: ['位置尺寸', '样式设计', '内容设置'],
      ingoreKeys: [
        'left',
        'top',
        'name',
        'width',
        'height',
        'radiusTopLeft',
        'radiusTopRight',
        'radiusBottomLeft',
        'radiusBottomRight',
      ],
      layerIconList,
      alignIconList,
      localization,
    }
  },
  computed: {
    ...mapGetters(['dActiveElement', 'dMoving']),
    dActiveElement() {
      return this.$store.getters.dActiveElement
    },
  },
  //
  methods: {
    ...mapActions(['updateWidgetData', 'updateAlign', 'updateLayerIndex']),
    finish(key, value) {
      if (!this.ingoreKeys.includes(key)) {
        this.updateWidgetData({
          uuid: this.dActiveElement.uuid,
          key: key,
          value: value,
          pushHistory: true,
        })
      } else {
        console.log(
          `The property '${key}' is in the ingoreKeys list and won't be updated.`,
        )
      }
    },
    layerAction(item) {
      this.updateLayerIndex({
        uuid: this.dActiveElement.uuid,
        value: item.value,
      })
    },
    async alignAction(item) {
      this.updateAlign({
        align: item.value,
        uuid: this.dActiveElement.uuid,
      })
      await this.$nextTick()
      this.$store.commit('updateRect')
    },
    async uploadImgDone(img) {
      this.$store.commit('setShowMoveable', false)
      await api.material.addMyPhoto(img)
      // this.dActiveElement.width = img.width
      // this.dActiveElement.height = img.height * (this.innerElement.width / img.width)
      this.dActiveElement.url = img.url
      this.$store.commit('setShowMoveable', true)
    },
  },
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
