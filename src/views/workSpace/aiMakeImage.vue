<template>
  <el-button plain @click="aiDialog = true">使用Ai创造图片</el-button>

  <el-dialog
    v-model="aiDialog"
    title="生成Ai图片"
    width="800"
    :before-close="handleClose"
  >
    <div class="text-contant">
      <div class="raw-contant">
        <div>描述：</div>
        <el-input
          v-model="AiDes"
          style="width: 600px"
          placeholder="请输入图片描述"
          :rows="4"
          type="textarea"
          clearable
        ></el-input>
      </div>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="aiDialog = false">取消</el-button>
        <el-button type="primary" @click="createTask">提交生成任务</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { ElMessageBox, ElMessage } from "element-plus";
import { createAiImage } from "@/api/home";
// 定义接收的 props
const props = defineProps<{
  projectName: string;
}>();

const aiDialog = ref(false);

const AiDes = ref<string>("");

const createTask = async () => {
  aiDialog.value = false;
  await createAiImage({
    text: AiDes.value,
    projectName: props.projectName,
  });
  ElMessage({
    message: "提高生成图片人物成功",
    type: "success",
  });
};

const handleClose = (done: () => void) => {
  ElMessageBox.confirm("是否开始生成?")
    .then(() => {})
    .catch(() => {
      // catch error
    });
};
</script>

<style lang="less" scoped>
.raw-contant {
  display: flex;
  align-items: center;
}
</style>
