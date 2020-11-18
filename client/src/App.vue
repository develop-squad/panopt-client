<template>
  <div id="q-app">
    <router-view />
  </div>
</template>
<script>
import { T } from "./store/module/types";

export default {
  name: "App",
  created() {
    this.setDeviceId();
  },
  methods: {
    setDeviceId() {
      const deviceId = String(Math.random());
      this.$store.dispatch(T.INIT_PROGRAM, deviceId);
      console.log("Device ID = "+  deviceId);
    },
  },
};
</script>
