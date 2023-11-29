<template>
  <div class="wrap">
    <search-header type="none" @change="searchChange" />
    <div style="height: 0.5rem" />
    <classHeader
      v-show="!state.currentCategory"
      :types="state.types"
      @select="selectTypes"
    >
      <template v-slot="{ index }">
        <photo-list
          :isShort="true"
          :listData="state.showList[index]"
          @load="getDataList"
          @drag="dragStart($event, state.showList[index])"
          @select="selectImg($event, state.showList[index])"
        />
      </template>
    </classHeader>
    <div v-if="state.currentCategory">
      <classHeader :is-back="true" @back="back">{{
        state.currentCategory.name
      }}</classHeader>
      <br /><br /><br />
      <div style="margin: 0 1rem; height: 100vh">
        <photo-list
          :isDone="state.loadDone"
          :listData="state.recommendImgList"
          @load="getDataList"
          @drag="dragStart"
          @select="selectImg"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
// 图片列表
const NAME = 'chart-list-wrap'
import { reactive, computed, onMounted } from 'vue'
import wImage from '../../widgets/wImage/wImage.vue'
import api from '@/api'
import { useStore } from 'vuex'
import setImageData from '@/common/methods/DesignFeatures/setImage'

defineOptions({
  name: NAME,
  inheritAttrs: false,
})

// defineProps(['active'])

const store = useStore()
const state = reactive({
  recommendImgList: [],
  loadDone: false,
  page: 0,
  currentCategory: null,
  types: [],
  showList: [],
})

//   state
const dPage = computed(() => store.getters.dPage)
let loading = false

onMounted(async () => {
  if (state.types.length <= 0) {
    const types = await api.material.getKinds({ type: 10 })
    state.types = types
    for (const iterator of types) {
      const { list } = await api.material.getChartList({
        labelName: iterator.name,
        pageSize: 2,
      })
      state.showList.push(list)
    }
  }
})

const selectImg = async (index, list) => {
  const item = list ? list[index] : state.recommendImgList[index]
  store.commit('setShowMoveable', false) // 清理掉上一次的选择
  let setting = JSON.parse(JSON.stringify(wImage.setting))
  const img = await setImageData(item) // await getImage(item.url)
  setting.width = img.width
  setting.height = img.height // parseInt(100 / item.value.ratio, 10)
  setting.imgUrl = item.url
  const { width: pW, height: pH } = dPage
  setting.left = pW / 2 - img.width / 2
  setting.top = pH / 2 - img.height / 2
  store.dispatch('addWidget', setting)
}

const getDataList = async () => {
  if (state.loadDone || loading) {
    return
  }
  loading = true
  state.page += 1
  let { list = [], total } = await api.material.getChartList({
    labelName: state.currentCategory.name,
    page: state.page,
    pageSize: 30,
  })
  list.length <= 0
    ? (state.loadDone = true)
    : (state.recommendImgList = state.recommendImgList.concat(list))
  setTimeout(() => {
    loading = false
  }, 100)
}

const dragStart = (index, list) => {
  const item = list ? list[index] : state.recommendImgList[index]
  store.commit('selectItem', { data: { value: item }, type: 'image' })
}

const searchChange = (e) => {
  console.log(e)
}

const selectTypes = (item) => {
  state.currentCategory = item
  getDataList()
}
const back = () => {
  state.currentCategory = null
  state.page = 0
  state.loadDone = false
  state.recommendImgList = []
}
</script>

<style lang="less" scoped>
.wrap {
  width: 100%;
  height: 100%;
}
</style>
