<template>
  <div class="home" v-loading="loading">
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
      <el-tab-pane
        v-for="item in typeList"
        :key="item"
        :label="item"
        :name="item"
      ></el-tab-pane>
    </el-tabs>
    <workSpaceIndex ref="workSpaceIndexRef"></workSpaceIndex>
    <div class="del-contant">
      <el-button type="primary" @click="addProject" :icon="FolderAdd" />
      <el-button
        type="primary"
        :loading="deleteloading"
        @click="delProject"
        :icon="Delete"
      />
    </div>
    <el-drawer
      v-model="newProjectDrawer"
      title="创建新的项目"
      :direction="'rtl'"
      :size="'40%'"
    >
      <div
        class="input-contant"
        :style="{
          display: 'flex',
          alignItems: 'center',
        }"
      >
        <div>项目名称：</div>
        <el-input
          v-model="newProjectName"
          style="width: 240px"
          placeholder="Please input"
        ></el-input>
      </div>
      <template #footer>
        <div style="flex: auto">
          <el-button :loading="addLoading" type="primary" @click="createNewProject"
            >创建</el-button
          >
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script lang="ts" setup>
import { ref, Ref, onMounted } from "vue";
import type { TabsPaneContext } from "element-plus";
import workSpaceIndex, { WorkspaceIndexInterface } from "./workSpace/index.vue";
import { getNewsList, deleteProject, createProject } from "@/api/home";
import { Delete, FolderAdd } from "@element-plus/icons-vue";
import { ElMessageBox, ElMessage } from "element-plus";

const typeList = ref<String[]>([]);

const newProjectName = ref<string>("");

const newProjectDrawer = ref<Boolean>(false);

const deleteloading = ref<Boolean>(false);

const addLoading = ref<Boolean>(false);

const loading = ref<Boolean>(false);

const workSpaceIndexRef = ref<WorkspaceIndexInterface | null>(null);

const fetchProjectList = async () => {
  loading.value = true;
  try {
    const list = await getNewsList();
    typeList.value = list;
    if (workSpaceIndexRef.value) {
      workSpaceIndexRef.value.init(String(list[0]));
      activeName.value = String(list[0]);
    }
  } catch (error) {
    console.error("Failed to fetch user details", error);
  } finally {
    loading.value = false;
  }
};

const activeName = ref("");

const handleClick = (tab: TabsPaneContext, event: Event) => {
  if (workSpaceIndexRef.value) {
    workSpaceIndexRef.value.init(String(tab.paneName));
  }
};
// 删除项目
const delProject = () => {
  ElMessageBox.confirm("确定要删除这个项目吗？这个操作无法撤销。", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
    icon: Delete,
  })
    .then(async () => {
      // 这里放置删除逻辑
      console.log("项目已删除");
      deleteloading.value = true;
      try {
        await deleteProject({
          project_name: activeName.value,
        });

        window.location.reload();
        // 可选：显示操作成功的消息
        ElMessage({
          type: "success",
          message: "删除成功!",
        });
      } catch {
      } finally {
        deleteloading.value = false;
      }
    })
    .catch(() => {
      // 用户取消操作
      ElMessage({
        type: "info",
        message: "已取消删除",
      });
    });
};

// 添加项目
const addProject = () => {
  newProjectDrawer.value = true;
};

// 创建新的项目
const createNewProject = async () => {
  addLoading.value = true;
  try {
    await createProject({
      project_name: newProjectName.value,
    });
    ElMessage({
      type: "success",
      message: "创建成功!",
    });

    window.location.reload();
  } catch {
  } finally {
    addLoading.value = false;
  }
};

onMounted(fetchProjectList);
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

.del-contant {
  position: absolute;
  right: 10px;
  top: 8px;
}
</style>
