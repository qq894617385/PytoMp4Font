<template>
  <router-view />
</template>

<script lang="ts">
import { defineComponent, reactive, onMounted, onUnmounted } from "vue";
import socket from "@/socket";
import { ElNotification } from "element-plus";
interface Message {
  id: number;
  text: string;
}

export default defineComponent({
  setup() {
    const state = reactive({
      message: "",
      messages: [] as Message[],
      nextMessageId: 0,
    });

    function sendMessage() {
      socket.emit("chat message", state.message);
      state.message = "";
    }

    function receiveMessage(jsondata: any) {
      ElNotification({
        title: jsondata.data,
        type: "success",
      });
    }

    onMounted(() => {
      socket.on("update", receiveMessage);
    });

    onUnmounted(() => {
      socket.off("chat message", receiveMessage);
    });

    return { ...state, sendMessage };
  },
});
</script>

<style>
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

#app {
  width: 100vw;
  height: 100vh;
}
</style>
