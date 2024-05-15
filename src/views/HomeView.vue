<template>
  <div class="home">
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
      <el-tab-pane
        v-for="item in typeList"
        :key="item"
        :label="item"
        :name="item"
      ></el-tab-pane>
    </el-tabs>
    <workSpaceIndex></workSpaceIndex>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import type { TabsPaneContext } from 'element-plus'
import workSpaceIndex from './workSpace/index.vue'
import { getNewsList } from '@/api/home'

const typeList = ref<String[]>([])

const fetchUser = async () => {
  try {
    const list = await getNewsList()
    typeList.value = list
  } catch (error) {
    console.error('Failed to fetch user details', error)
  }
}

const activeName = ref('')

const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(activeName.value)
}

onMounted(fetchUser)
</script>

<style lang="less" scoped>
.home {
  padding: 10px;
  height: 100%;
  width: 100%;
}

.demo-tabs {
  width: 100%;
  height: 60px;
}
</style>
