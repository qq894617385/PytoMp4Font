# 项目介绍

本前端项目用于配合 ai 生成图片排版视频操作界面

## Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### dist

打包后吧 dist 文件到，放到 python 项目的 web 文件夹下面

如有修改后台启动的端口，请把 ip 端口号保持一致

```javascript
VUE_APP_API_URL=http://127.0.0.1:5000

```

socket.ts

```javascript
import { io } from "socket.io-client";

const SOCKET_URL = "http://127.0.0.1:5000/"; // 根据你的服务器地址修改
const socket = io(SOCKET_URL);

export default socket;
```
