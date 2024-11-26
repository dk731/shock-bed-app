<script setup lang="ts">
async function shock() {}

async function toggleShocking() {}
</script>

<template>
  <div class="w-full h-full flex flex-col p-10 !bg-base-100">
    <div class="flex flex-col content-center">
      <q-btn class="!bg-primary !text-primary-content mb-2" @click="shock">
        <icon name="mdi:electricity" size="20" /> Shock
      </q-btn>
      <q-btn class="!bg-primary !text-primary-content" @click="shock">
        <icon name="mdi:electricity" size="20" /> Shock
      </q-btn>
    </div>
  </div>
</template>
