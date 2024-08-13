# 项目介绍 / Project Introduction

本前端项目用于配合 AI 生成图片排版视频操作界面。  
This frontend project is used for the AI-assisted image generation and video layout operation interface.

## 项目设置 / Project Setup

```bash
npm install
```

````

### 编译并热加载用于开发 / Compiles and Hot-Reloads for Development

```bash
npm run serve
```

### 编译并压缩用于生产 / Compiles and Minifies for Production

```bash
npm run build
```

### dist 文件夹 / dist Folder

打包后把 dist 文件放到 Python 项目的 web 文件夹下面。
After packaging, place the dist folder into the web folder of the Python project.

如有修改后台启动的端口，请保持 IP 和端口号一致。
If the backend startup port is modified, please ensure that the IP and port number are consistent.

```javascript
VUE_APP_API_URL=http://127.0.0.1:5000
```

### socket.ts 文件 / socket.ts File

```javascript
import { io } from "socket.io-client";

const SOCKET_URL = "http://127.0.0.1:5000/"; // 根据你的服务器地址修改
const socket = io(SOCKET_URL); // Modify according to your server address

export default socket;
```
````
