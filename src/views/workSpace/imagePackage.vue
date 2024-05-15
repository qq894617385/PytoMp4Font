<template>
  <div class="imagePackage">
    <div class="image-item" v-for="item in images" @click="changeImages(item)">
      <div class="icon-contant" v-if="item == currentData.bgi">
        <el-icon color="#fff"><Select /></el-icon>
      </div>
      <el-image
        style="width: 100%; height: 100%;"
        :src="getSetImage(item)"
        :zoom-rate="1.2"
        :max-scale="7"
        :min-scale="0.2"
        fit="contain"
      />
    </div>
    <div class="image-item">
      <el-upload
        class="avatar-uploader"
        :action="action"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload"
      >
        <img v-if="imageUrl" :src="imageUrl" class="avatar" />
        <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
      </el-upload>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineEmits } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getImagePackage, textItem } from '@/api/workspace'
import type { UploadProps } from 'element-plus'
import type { Ref } from 'vue'
// 定义接收的 props
const props = defineProps<{
  projectName: string
  index: number
  currentData: textItem
}>()

const emit = defineEmits<{
  (event: 'changeImages', message: string): void
}>()

const baseUrl = process.env.VUE_APP_API_URL

const action = baseUrl + '/upload_image/' + props.projectName

const imageUrl = ref('')

const images: Ref<string[]> = ref([])

const handleAvatarSuccess: UploadProps['onSuccess'] = (
  response,
  uploadFile,
) => {
  imageUrl.value = URL.createObjectURL(uploadFile.raw!)
}

const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
  if (rawFile.type !== 'image/jpeg') {
    ElMessage.error('Avatar picture must be JPG format!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  }
  return true
}

const getSetImage = (url: string) => {
  const baseUrl = process.env.VUE_APP_API_URL
  const dict = props.projectName
  return `${baseUrl}/images/${dict}/images/${url}`
}

const fetchImagesPackage = async (projectName: string) => {
  try {
    const dataImages = await getImagePackage({
      projectName,
    })
    images.value = dataImages.images
  } catch (error) {
    console.error('Failed to fetch user details', error)
  }
}

// 选中图片
const changeImages = (useUrl: string) => {
  emit('changeImages', useUrl)
}

onMounted(() => {
  // 获取图片
  fetchImagesPackage(props.projectName)
})
</script>

<style lang="less" scoped>
.imagePackage {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-auto-rows: 150px;
  gap: 10px;
}

.avatar {
  width: 100%;
  height: 100%;
  display: block;
}

.image-item {
  position: relative;
  border: 1px solid #dcdfe6;
  border-radius: 5px;
  cursor: pointer;
  overflow: hidden;
}
::v-deep .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 100%;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.avatar-uploader {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  text-align: center;
}

.icon-contant {
  position: absolute;
  right: 0;
  top: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 22px;
  height: 22px;
  background-color: skyblue;
  z-index: 99;
  border-bottom-left-radius: 5px;
}
</style>
