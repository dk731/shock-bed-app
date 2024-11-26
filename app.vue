<script setup lang="ts">
const $q = useQuasar();

$q.screen.setDebounce(0);
$q.dark.set(true);
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
