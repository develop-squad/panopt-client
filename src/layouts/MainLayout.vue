<template>
  <div class="layout">
    <router-view class="router-view" />
    <ControlPannel class="control-panel"></ControlPannel>
  </div>
</template>

<script>
import ControlPannel from "./ControlPannel";

export default {
  name: "MainLayout",
  components: { ControlPannel },
  data() {
    return {};
  },
};
</script>

<style lang="scss" scoped>
.layout {
  display: flex;
  width: 100vw;
  height: 100vh;

  & .router-view {
    width: 75%;
    height: 100%;
    background-color: grey;
  }
}
</style>
