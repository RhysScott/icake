<template>
  <div class="tab-wrapper" v-if="tabbar.visible">
    <div
      class="tab-button"
      :class="{ active: route.path === tab.path }"
      v-for="(tab, index) in tabs"
      key="index"
      @click="router.push(tab.path)"
    >
      <component class="icon" :is="tab.component" />
      <div class="label">{{ tab.label }}</div>
    </div>
  </div>
</template>

<script setup>
import { useTabbar } from "@/stores/layout";
import { Cake, CakeSlice, CupSoda, House, UserRound } from "@lucide/vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const tabbar = useTabbar();

const tabs = [
  { label: "首页", component: House, path: "/" },
  { label: "蛋糕", component: Cake, path: "/cake" },
  { label: "甜品", component: CakeSlice, path: "/dessert" },
  { label: "饮品", component: CupSoda, path: "/drink" },
  { label: "我的", component: UserRound, path: "/profile" },
];
</script>

<style lang="scss" scoped>
@use "@/styles/global.scss" as *;

.tab-wrapper {
  display: flex;
  width: 7.5rem;
  max-width: 7.5rem;
  justify-content: space-around;
  position: fixed;
  padding: 0.2rem 0;
  bottom: 0;
  left: 0;
  color: $nav-text-default;
  background-color: $nav-bg;
}

.tab-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.06rem;
  font-size: $font-md;
  cursor: pointer;

  &.active {
    color: $nav-text-active !important;
    font-weight: bold;
  }
}

.icon {
  width: $icon-size;
  height: $icon-size;
}

.label {
  font-size: $font-sm;
}
</style>
