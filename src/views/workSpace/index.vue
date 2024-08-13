<template>
  <div class="workspace">
    <div class="top-contant">
      <span>背景音乐：</span>
      <!-- 获取bgm -->
      <el-select v-model="value" placeholder="Select" style="width: 240px">
        <el-option v-for="item in bgmList" :key="item" :label="item" :value="item" />
      </el-select>
      <span>背景音乐：</span>
      <!-- 获取bgm -->
      <el-select v-model="value" placeholder="Select" style="width: 240px">
        <el-option v-for="item in aiMusicList" :key="item" :label="item" :value="item" />
      </el-select>
    </div>
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
            <div class="text-props">
              <div>
                <span class="span-text">颜色背景：</span>
                <el-color-picker v-model="element.bgc" size="small" />
              </div>
              <div>
                <span class="span-text">字体大小：</span>
                <el-input-number v-model="element.fontSize" :step="1" size="small" />
              </div>
              <div>
                <span class="span-text">颜色：</span>
                <el-color-picker v-model="element.color" size="small" />
              </div>
              <div>
                <span class="span-text">底边距：</span>
                <el-input-number v-model="element.marginBottom" :step="1" size="small" />
              </div>
            </div>
            <div class="text-contant">
              <el-input
                class="input-room"
                v-model="element.text"
                :rows="6"
                type="textarea"
                placeholder="Please input"
              />
            </div>
            <div class="video-contant">
              <video controls width="200px" height="200px">
                <source :src="getVideo(index)" type="video/mp4" />
                没有视频
              </video>
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
    <aiMakeImage :projectName="projectName" />
    <div style="flex: 1"></div>
    <span class="span-text">宽：</span>
    <el-input-number v-model="projectWidth" :step="1" />
    <span class="span-text">高：</span>
    <el-input-number v-model="projectHeight" :step="1" />
    <div style="flex: 1"></div>

    <el-button type="primary" @click="save">保存</el-button>
    <el-button type="warning" @click="hanldeEveryVideo">生成每段视频</el-button>
    <el-button type="warning" @click="combine">合并</el-button>
    <el-button type="danger" @click="saveAndCreate">一键生成</el-button>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed } from "vue";
import type { TabsPaneContext } from "element-plus";
import {
  getProjectDetail,
  ProjectDetail,
  textItem,
  savePorject,
  makeMovie,
  MakeEveryVideo,
  mergeVideo,
  getAllBGM,
  getAllvoicelist,
} from "@/api/workspace";
import type { Ref } from "vue";
import { ElMessage } from "element-plus";
import imagePackage from "./imagePackage.vue";
import draggable from "vuedraggable";
import { defineExpose } from "vue";
import outputDialog from "@/views/output/index.vue";
import aiMakeImage from "./aiMakeImage.vue";

const projectDetail = reactive({
  detail: {
    images: [],
    title: "",
    dict: "",
    project: {
      height: 0,
      width: 0,
    },
    bgm: "",
    voice: "",
    textArr: [],
  } as ProjectDetail | null,
  error: null as Error | null,
});

const projectWidth = computed({
  get() {
    return projectDetail.detail?.project.width || 0;
  },
  set(value) {
    if (projectDetail.detail) {
      projectDetail.detail.project.width = value;
    }
  },
});

const projectHeight = computed({
  get() {
    return projectDetail.detail?.project.height || 0;
  },
  set(value) {
    if (projectDetail.detail) {
      projectDetail.detail.project.height = value;
    }
  },
});

const textArr: Ref<ProjectDetail["textArr"]> = ref([]);

const drawer = ref(false);

const currentIndex = ref(-1);

const images: Ref<string[]> = ref([]);

const projectName: Ref<string> = ref("");

const currentData: Ref<textItem> = ref({});

const dialogShow = ref<Boolean>(false);

const value = ref("");

const bgmList = ref([]);

const aiMusicList = ref([]);

// 获取所有bgm
const getBGM = async () => {
  const bgm = await getAllBGM();
  bgmList.value = bgm.mp3List;
};

const getAiMusic = async () => {
  const aiMusic = await getAllvoicelist();
  aiMusicList.value = aiMusic.voice_list;
};
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

const getVideo = (url: string) => {
  const dict = projectDetail.detail?.dict;
  const baseUrl = process.env.VUE_APP_API_URL;
  return `${baseUrl}/videoSpan/${dict}/${url}`;
};

// 改变当前选中的图片背景
const changeIndexImages = (url: string) => {
  textArr.value[currentIndex.value].bgi = url;
};

const init = async (name: string) => {
  getBGM();
  getAiMusic();
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
    bgc: "#000",
    fontSize: 24,
    marginBottom: 60,
    color: "#fff",
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

const combine = async () => {
  try {
    await mergeVideo({
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

const hanldeEveryVideo = async () => {
  await save();
  try {
    await MakeEveryVideo({
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
  align-items: center;
  width: 100%;
  padding: 10px 16px;
  border-top: 2px solid #ececec;
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

.span-text {
  margin-left: 12px;
  color: #409eff;
}

.text-props {
  width: 250px;
}

.video-contant {
  margin-left: 30px;
}

.top-contant {
  background: #f0f0f0;
  height: 40px;
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
}
</style>
