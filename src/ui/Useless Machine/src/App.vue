<script setup>
import { RouterLink, RouterView } from 'vue-router';
import NavBar from "@/components/NavBar.vue";
import 'bootstrap/dist/js/bootstrap.min.js';
</script>

<template>
  <NavBar/>
  <RouterView />
</template>

<style>
@import 'bootstrap/dist/css/bootstrap.css'
</style>
