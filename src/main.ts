import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 创建 Vue 应用实例
const app = createApp(App)

// 使用 Vuex、Vue Router 和 Element Plus
app.use(store).use(router).use(ElementPlus)

// 全局注册 Element Plus 的所有图标
Object.entries(ElementPlusIconsVue).forEach(([iconName, iconComponent]) => {
    app.component(iconName, iconComponent)
})

// 挂载 Vue 应用实例到 DOM
app.mount('#app')
