<template>
  <div>
    <div id="map"></div>
  </div>
</template>

<script>
import { T } from "../store/module/types";

export default {
  name: "PageIndex",
  mounted() {
    this.initMapbox();
  },
  methods: {
    initMapbox() {
      let mapboxgl = require("mapbox-gl/dist/mapbox-gl.js");

      mapboxgl.accessToken =
        "pk.eyJ1IjoibW9vbmp1aGFuIiwiYSI6ImNrZXV4Y3g0dzIxeDAyeHF2NXpqZmJ0d3YifQ.mQU_y-ckbnxNzg8g9BsEKQ";
      let map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/moonjuhan/ckeuxj63h0ooy19js1h2ezuqz",
      });
    },
    drawNetwork(params){

    }
  },
};
</script>

<style lang="scss" scoped>
#map {
  height: 100%;
}
</style>