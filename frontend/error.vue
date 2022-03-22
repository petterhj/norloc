<template>
  <div class="flex flex-col h-screen">
    <Header />
    <section class="h-screen bg-white p-[1.2rem]" style="padding-top: 0; /* ? */">
      <div class="relative h-full bg-[url('~/assets/error-bg.jpg')] bg-cover bg-center">
        <div class="p-6">
          <h1 class="text-white mb-1">{{ statusMessage }} — {{ error.statusCode }}</h1>
          <h2 class="text-neutral-400">Du venner deg til det.</h2>
        </div>
        
        <div class="p-6 fixed bottom-2">
          <h3 class="m-0 text-neutral-400">
            <a
              class="mr-1 text-neutral-400 hover:text-white"
              href="https://www.imdb.com/title/tt0808185/"
              target="_blank"
            >
              Den brysomme mannen
            </a>
            <span class="year">(2006)</span>
          </h3>
          <h5 class="m-0 text-neutral-400">Nydalen stasjon, Nydalen, Oslo</h5>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const props = defineProps({
  error: Object
})

const statusMessage = computed(() => {
  if (props.error.statusCode == 404)
    return 'Denne siden eksisterer ikke'
  return props.error.statusMessage
})

</script>
