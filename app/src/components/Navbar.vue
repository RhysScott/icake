<template>
  <div class="nav-wrapper" v-if="navbar.visible">
    <div class="nav-button" @click="router.back()">
      <component class="icon" :is="ArrowLeft" />
    </div>
    <div class="nav-title">
      <div class="label">{{ navbar.title }}</div>
    </div>
  </div>
</template>

<script setup>
import { useNavbar } from "@/stores/layout";
import { ArrowLeft } from "@lucide/vue";
import { useRouter } from "vue-router";

const router = useRouter();
const navbar = useNavbar();

</script>

<style lang="scss" scoped>
@use "@/styles/global.scss" as *;

.nav-wrapper {
  display: flex;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  height: $nav-height;
  padding: 0 0.3rem;
  align-items: center;
  color: $nav-text-default;
  background-color: $nav-bg;
  box-sizing: border-box;
}

.nav-button {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.nav-title {
  flex: 1;
  display: flex;
  justify-content: center;
  font-size: $font-lg;
  font-weight: bold;
  color: $nav-text-active;
}

.icon {
  width: $icon-size;
  height: $icon-size;
}

.label {
  font-size: $nav-font-size;
}
</style>
