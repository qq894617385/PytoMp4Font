<template>
  <div class="workspace">
    <draggable v-model="textArr" group="name" item-key="index">
      <template #item="{ element, index }">
        <div class="line-contant" :key="'line' + index">
          <div class="title-contant">
            <div>元素{{ index + 1 }}：</div>
            <div style="flex: 1"></div>
            <el-icon style="cursor: pointer" color="#409eff" @click="deleteRow(index)">
              <Delete />
            </el-icon>
          </div>
          <div class="row-contant">
            <div class="text-contant">
              <el-input
                class="input-room"
                v-model="element.text"
                :rows="6"
                type="textarea"
                placeholder="Please input"
              />
            </div>
            <div class="image-contant" @click="showImagePackage(index, element)">
              <div
                class="black-bg"
                style="width: 130px; height: 130px"
                v-if="element.bgi === ''"
              ></div>
              <el-image
                v-else
                style="width: 130px; height: 130px"
                :src="getSetImage(element?.bgi || '')"
                :zoom-rate="1.2"
                :max-scale="7"
                :min-scale="0.2"
                fit="cover"
              />
            </div>
          </div>
        </div>
      </template>
    </draggable>
    <div class="add-contant" @click="addRow">
      <el-icon><Plus /></el-icon>
    </div>
    <el-drawer v-model="drawer" title="图片库" :direction="'rtl'" :size="'40%'">
      <imagePackage
        v-if="drawer"
        :index="currentIndex"
        :currentData="currentData"
        :projectName="projectName"
        @change-images="changeIndexImages"
      />
    </el-drawer>
  </div>
  <outputDialog
    v-if="dialogShow"
    :projectName="projectName"
    @close="closeOutView"
  ></outputDialog>
  <div class="bottom-contant">
    <el-button type="primary" @click="openOutView">输出视频预览</el-button>
    <div style="flex: 1"></div>
    <el-button type="primary" @click="save">保存</el-button>
    <el-button type="primary" @click="saveAndCreate">保存并生成</el-button>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from "vue";
import type { TabsPaneContext } from "element-plus";
import {
  getProjectDetail,
  ProjectDetail,
  textItem,
  savePorject,
  makeMovie,
} from "@/api/workspace";
import type { Ref } from "vue";
import { ElMessage } from "element-plus";
import imagePackage from "./imagePackage.vue";
import draggable from "vuedraggable";
import { defineExpose } from "vue";
import outputDialog from "@/views/output/index.vue";

const projectDetail = reactive({
  detail: null as ProjectDetail | null,
  error: null as Error | null,
});

const textArr: Ref<ProjectDetail["textArr"]> = ref([]);

const drawer = ref(false);

const currentIndex = ref(-1);

const images: Ref<string[]> = ref([]);

const projectName: Ref<string> = ref("");

const currentData: Ref<textItem> = ref({});

const dialogShow = ref<Boolean>(false);

// 打开预览视频
const openOutView = () => {
  dialogShow.value = true;
};

// 关闭预览视频
const closeOutView = () => {
  dialogShow.value = false;
};

const showImagePackage = (index: number, item: textItem) => {
  drawer.value = true;
  currentIndex.value = index;
  currentData.value = item;
};

const getSetImage = (url: string) => {
  const dict = projectDetail.detail?.dict;
  const baseUrl = process.env.VUE_APP_API_URL;
  return `${baseUrl}/images/${dict}/images/${url}`;
};

// 改变当前选中的图片背景
const changeIndexImages = (url: string) => {
  textArr.value[currentIndex.value].bgi = url;
};

const init = async (name: string) => {
  projectName.value = name;
  try {
    const detail = await getProjectDetail({
      projectName: projectName.value,
    });
    projectDetail.detail = detail;
    textArr.value = detail.textArr;
    images.value = detail.images;
  } catch (error) {
    console.error("Failed to fetch user details", error);
  }
};

const activeName = ref("");

const save = async () => {
  try {
    projectDetail.detail!.textArr = textArr.value;
    const detail = await savePorject({
      projectName: projectName.value,
      ProjectDetail: projectDetail.detail!,
    });
    ElMessage({
      message: "保存成功",
      type: "success",
    });
  } catch (error) {
    console.error("保存失败", error);
  }
};

const openImagePackage = (tab: TabsPaneContext, event: Event) => {
  console.log(activeName.value);
};

// 添加图片
const addRow = () => {
  textArr.value.push({
    bgi: "",
    text: "",
  });
};

const saveAndCreate = async () => {
  await save();
  try {
    await makeMovie({
      projectName: projectName.value,
    });
    ElMessage({
      message: "开始创建",
      type: "success",
    });
  } catch (error) {
    console.error("保存失败", error);
  }
};

// 删除该行
const deleteRow = (index: number) => {
  textArr.value.splice(index, 1);
};

defineExpose({ init });

export interface WorkspaceIndexInterface {
  init: (projectName: string) => void;
}
</script>

<style lang="less" scoped>
.bottom-contant {
  position: absolute;
  left: 0;
  bottom: 0;
  background: #fff;
}

.workspace {
  position: relative;
  width: 100%;
  height: calc(100% - 60px);
  overflow-y: auto;
}

.line-contant {
  margin-bottom: 16px;
  width: 100%;
  background: #ececec;
  border-radius: 10px;
  padding: 20px;
  box-sizing: border-box;
  .row-contant {
    margin-top: 16px;
    display: flex;
    align-items: center;
    width: 100%;
    .text-contant {
      flex: 1;
      .input-room {
        width: 100%;
      }
    }
  }
  .image-contant {
    margin-left: 32px;
    border-radius: 6px;
    overflow: hidden;
  }
}

.bottom-contant {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  padding: 10px 16px;
}

.add-contant {
  display: flex;
  padding: 16px;
  justify-content: center;
  align-items: center;
  border-radius: 5px;
  border: 1px skyblue dashed;
  cursor: pointer;
  margin-bottom: 60px;
}
.black-bg {
  background-color: #000;
  border-radius: 6px;
}

.title-contant {
  display: flex;
  font-weight: 600;
  color: #333;
}
</style>
