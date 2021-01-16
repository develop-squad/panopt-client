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
      currentMarkerList: [],
    };
  },
  computed: {
    ...mapGetters({
      processList: "getProcessList",
    }),
  },
  watch: {
    processList(newProcessList) {
      this.nowProcessList.forEach((process) => {
        if (!newProcessList.find((el) => el.processId == process.processId)) {
          // delete
          this.nowProcessList = this.nowProcessList.filter(
            (el) => el.processId !== process.processId
          );
          console.log("DELETE");
          this.deleteNetwork(process.processId, process.lng, process.lat);
        }
      });

      newProcessList.forEach((process) => {
        let thisProcess = this.nowProcessList.find(
          (el) => el.processId == process.processId
        );

        if (thisProcess) {
          if (thisProcess.remote_ip !== process.remote_ip) {
            console.log("Update");
            this.getLocation(process, thisProcess);
          }
        } else {
          console.log("Create");
          this.getLocation(process, 0);
        }
      });
    },
  },
  mounted() {
    this.initMapbox();
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

      const startMarker = new mapboxgl.Marker({
        color: "red",
      })
        .setLngLat([127.07387104135374, 37.55047772513164])
        .addTo(this.map);
    },
    drawNetwork(process) {
      let mapboxgl = require("mapbox-gl/dist/mapbox-gl.js");

      if (process.lng && process.lat) {
        var market = new mapboxgl.Marker()
          .setLngLat([process.lng, process.lat])
          .addTo(this.map);

        this.currentMarkerList.push(market);

        this.map.addSource(process.processId, {
          type: "geojson",
          data: {
            type: "FeatureCollection",
            features: [
              {
                type: "Feature",
                properties: {
                  color: "#F7455D", // red
                },
                geometry: {
                  type: "LineString",
                  coordinates: [
                    [127.07387104135374, 37.55047772513164],
                    [process.lng, process.lat],
                  ],
                },
              },
            ],
          },
        });

        this.map.addLayer({
          id: process.processId,
          type: "line",
          source: process.processId,
          paint: {
            "line-width": 3,
            "line-color": ["get", "color"],
          },
        });
      }
    },
    deleteNetwork(processId, lng, lat) {
      console.log(processId);
      this.currentMarkerList.find((el) => el._lngLat.lat == lat).remove();
      this.currentMarkerList.splice(
        this.currentMarkerList.findIndex((el) => el._lngLat.lat == lat),
        1
      );
      this.map.removeLayer(processId);
      this.map.removeSource(processId);
      this.nowProcessList = this.nowProcessList.filter(
        (el) => el.processId !== processId
      );

      console.log(this.map.getStyle());
    },
    getLocation(process, updated) {
      this.$store.dispatch(T.GET_LOCATION_FROM_IP, {
        ip: process.remote_ip,
        cSuc: (data) => {
          console.log("GETLOCATION", updated);
          process.lat = data.latitude;
          process.lng = data.longitude;
          if (updated) {
            console.log("UP");
            updated = process;
          } else {
            this.drawNetwork(process);
            this.nowProcessList.push(process);
          }
        },
        cErr: (err) => {
          console.log(err);
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