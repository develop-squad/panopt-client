<template>
  <div class="control-panel">
    <div class="toggle-view">Toggle View</div>
    <div class="process-view">Process View</div>
    <div class="status-view">Status View</div>
  </div>
</template>

<script>
import { T } from "../store/module/types";
import { mapGetters } from "vuex";

export default {
  mounted() {},
  computed: {
    ...mapGetters({
      deviceId: "getDeviceId",
    }),
  },
  watch: {
    deviceId(newDeviceId) {
      console.log(newDeviceId);
    },
  },
  mounted() {
    // this.getEvent();
  },
  methods: {
    getEvent() {
      setTimeout(() => {
        if (this.deviceId) {
          this.$store.dispatch(T.GET_EVENT, {
            deviceId: this.deviceId,
            cSuc: (data) => {
              console.log(data);
            },
          });
        }
        this.getEvent();
      }, 1000);
    },
  },
};
</script>

<style lang="scss" scoped>
.control-panel {
  width: 25%;
  height: 100%;

  & > div {
    padding: 10px;
    width: 100%;
  }
}
.toggle-view {
  height: 20%;
}

.process-view {
  height: 55%;
}

.status-view {
  height: 25%;
}

.toggle-view,
.process-view {
  border-bottom: 1px solid grey;
}
</style>