// src/socket.ts
import { io } from "socket.io-client";

const SOCKET_URL = "http://127.0.0.1:5000/"; // 根据你的服务器地址修改
const socket = io(SOCKET_URL);

export default socket;
