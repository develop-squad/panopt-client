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
    this.runProcessMonitorPy();
  },
  methods: {
    setDeviceId() {
      const deviceId = String(Math.random());
      // this.$store.dispatch(T.INIT_PROGRAM, deviceId);
      console.log("Device ID = " + deviceId);
    },
    runProcessMonitorPy() {
      const { PythonShell } = require("python-shell");

      let options = {
        scriptPath: "./src/python/",
        args: [1, 2],
      };
      setTimeout(() => {
        PythonShell.run("process-monitor.py", options, (err, data) => {
          const time = new Date();
          if (err) {
            console.log("ERR");
            console.log(err);
            throw err;
          }

          this.$store.dispatch(T.UPDATE_PROCESS_LIST, {
            list: JSON.parse(data[0].replace(/\'/gi, '"')),
            time,
          });

          // if (data != null) console.log(data.length);
        });
        this.runProcessMonitorPy();
      }, 1000);
    },
  },
};
</script>
