<template>
  <div>
    Grid med produksjoner her!
  </div>
</template>

<script setup>
  // import { useMenu } from "@/store/navbar";

  definePageMeta({
    title: 'Produksjoner',
    layout: 'items',
    menu: [
      {label: 'Type', items: [
        {label: 'Alle', page: 'productions-sorted', params: {type: 'alle'}},
        {label: 'Film', page: 'productions-sorted', params: {type: 'film'}},
        {label: 'TV', page: 'productions-sorted', params: {type: 'tv'}},
      ]},
      {label: 'Sortering', items: [
        {label: 'Tittel', page: 'productions-sorted', params: {type: '', sort: 'tittel'}},
        {label: 'År', page: 'productions-sorted', params: {type: '', sort: 'aar'}},
        // {label: 'Tittel', page: 'productions-sorted', params: {type: $route.params.type, sort: 'tittel'}},
        // {label: 'År', page: 'productions-sorted', params: {type: $route.params.type, sort: 'aar'}},
      ]}
    ]
  })
</script>