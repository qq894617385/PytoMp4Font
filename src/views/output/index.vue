<template>
  <el-dialog v-model="dialogVisible" title="观看视频" width="600px">
    <video controls width="100%" height="600px">
      <source :src="videoUrl" type="video/mp4" />
      Your browser does not support the video tag.
    </video>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="close">取消</el-button>
        <el-button type="primary" @click="close"> 确定 </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, defineEmits } from "vue";
import { ElButton, ElDialog } from "element-plus";

// 定义接收的 props
const props = defineProps<{
  projectName: string;
}>();

const emit = defineEmits<{
  (event: "close"): void;
}>();

const dialogVisible = ref(true);
const baseUrl = process.env.VUE_APP_API_URL;
const action = baseUrl + "/video/" + props.projectName;
const videoUrl = ref(action);

const close = () => {
  emit("close");
};
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
