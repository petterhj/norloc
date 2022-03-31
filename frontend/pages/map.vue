<template>
  <div class="h-full">
    <LMap
      class="h-full"
      v-model="zoom"
      v-model:zoom="zoom"
      :center="[59.9239573,10.7466634]"
    >
      <!-- <LTileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      ></LTileLayer> -->
      <LTileLayer
        v-for="layer in tileLayers"
        :key="layer.name"
        :name="layer.name"
        :visible="layer.visible"
        :url="layer.url"
        :attribution="layer.attribution"
        :options="layer.options"
        layer-type="base"
      />

      <LControlLayers />
    </LMap>
  </div>
</template>

<script setup>
  import "leaflet/dist/leaflet.css"
  import { LMap, LTileLayer, LControlLayers } from "@vue-leaflet/vue-leaflet";

  const zoom = ref(14);

  const tileLayers = [
    {
      name: 'MapBox (norloc, mørk)',
      visible: true,
      attribution: '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      url: 'https://api.mapbox.com/styles/v1/{tileLayerId}/tiles/{z}/{x}/{y}?access_token={accessToken}',
      options: {
        tileLayerId: 'slekvak/cjly2r5d14zbm2rlxq8elklvk',
        accessToken: 'pk.eyJ1Ijoic2xla3ZhayIsImEiOiJjaXE4azdndnQwMDQ4aHhrcWZpM25rcDMxIn0.5ObHw68HeWzfLprlb5M5HA',
      }
    }, {
      name: 'Kartverket (topo, gråtone)',
      visible: false,
      attribution: '© Kartverket',
      url: 'https://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?layers=topo4graatone&zoom={z}&x={x}&y={y}',
    }, {
      name: 'OpenStreetMap',
      visible: false,
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    }
  ]

  definePageMeta({
    title: 'Kart',
    layout: 'full',
  })
</script>

<style>
/* https://github.com/Leaflet/Leaflet/issues/3575 */
.leaflet-tile-container img {
  border-radius: 0 !important;
  width: 256.5px !important;
  height: 256.5px !important;
}
</style>