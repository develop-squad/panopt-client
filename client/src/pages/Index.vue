<template>
  <div>
    <div id="map"></div>
  </div>
</template>


<script>
import { T } from "../store/module/types";
import { mapGetters } from "vuex";

export default {
  name: "PageIndex",
  data() {
    return {
      map: {},
      nowProcessList: [],
    };
  },
  computed: {
    ...mapGetters({
      processList: "getProcessList",
    }),
  },
  watch: {
    processList(newProcessList) {
      console.log(newProcessList);
      console.log(this.nowProcessList);
      // let refinedProcessList = this.nowProcessList;
      this.nowProcessList.forEach((process) => {
        if (newProcessList.find((el) => el.processId !== process.processId)) {
          // delete
          this.nowProcessList = this.nowProcessList.filter(
            (el) => el.processId !== process.processId
          );
        }
      });

      newProcessList.forEach((process) => {
        let thisProcess = this.nowProcessList.find(
          (el) => el.processId == process.processId
        );

        if (thisProcess) {
          if (thisProcess.remote_ip !== process.remote_ip) {
            // update
            this.getLocation(process, thisProcess);
          }
        } else {
          console.log("C");
          //  created
          this.getLocation(process, 0);
        }
      });
    },
  },
  mounted() {
    this.initMapbox();
    this.drawNetwork("test");
  },
  methods: {
    initMapbox() {
      let mapboxgl = require("mapbox-gl/dist/mapbox-gl.js");

      mapboxgl.accessToken =
        "pk.eyJ1IjoibW9vbmp1aGFuIiwiYSI6ImNrZXV4Y3g0dzIxeDAyeHF2NXpqZmJ0d3YifQ.mQU_y-ckbnxNzg8g9BsEKQ";
      this.map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/moonjuhan/ckeuxj63h0ooy19js1h2ezuqz",
        center: [127.07387104135374, 37.55047772513164],
        zoom: 3,
      });

      const startMarker = new mapboxgl.Marker()
        .setLngLat([127.07387104135374, 37.55047772513164])
        .addTo(this.map);
    },
    drawNetwork(process) {
      let mapboxgl = require("mapbox-gl/dist/mapbox-gl.js");
      console.log("DRAW");
      if (process.lng && process.lat) {
        var lastMarker = new mapboxgl.Marker()
          .setLngLat([process.lng, process.lat])
          .addTo(this.map);
      }

      // this.map.on("load", () => {
      //   this.map.addSource("lines", {
      //     type: "geojson",
      //     data: {
      //       type: "FeatureCollection",
      //       features: [
      //         {
      //           type: "Feature",
      //           properties: {
      //             color: "#F7455D", // red
      //           },
      //           geometry: {
      //             type: "LineString",
      //             coordinates: [
      //               [127.07387104135374, 37.55047772513164],
      //               [116.429686846067, 39.928359181991986],
      //             ],
      //           },
      //         },
      //       ],
      //     },
      //   });

      //   this.map.addLayer({
      //     id: "lines",
      //     type: "line",
      //     source: "lines",
      //     paint: {
      //       "line-width": 3,
      //       "line-color": ["get", "color"],
      //     },
      //   });
      // });
    },
    getLocation(process, updated) {
      this.$store.dispatch(T.GET_LOCATION_FROM_IP, {
        ip: process.remote_ip,
        cSuc: (data) => {
          process.lat = data.latitude;
          process.lng = data.longitude;
          if (updated) {
            updated = process;
          } else {
            this.drawNetwork(process);
            this.nowProcessList.push(process);
          }
        },
      });
    },
  },
};
</script>

<style lang="scss" scoped>
#map {
  height: 100%;
}
</style>