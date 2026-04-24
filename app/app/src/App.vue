<script setup>

import Navbar from '@/components/Navbar.vue';
import Tabbar from '@/components/Tabbar.vue';

</script>

<template>
  <div class="app-wrapper">
    <Navbar />
    <div class="main">
      <RouterView></RouterView>
    </div>
    <Tabbar />
  </div>
</template>

<style scoped>
.app-wrapper {
  height: 100vh;
  max-height: 100vh;
}
</style>
