<script setup lang="ts">
const url = useRequestURL();

type ShockState = {
  voltage?: number;
  state?: boolean;
  frequency?: number;
  dutyCycle?: number;
};

const shockState = ref<ShockState>({});
const remoteState = useAsyncData(async () => {
  const response = await fetch(`http://${url.hostname}:8000/api/shock`, {
    method: "GET",
  });
  const data = await response.json();
  return data as ShockState;
});
watch(
  () => remoteState.data.value,
  (data) => (shockState.value = { ...data })
);

let timeout: NodeJS.Timeout | null = null;
const isUpdating = ref(false);
watch(
  () => ({ ...shockState.value }),
  () => {
    if (timeout) return;
    timeout = setTimeout(async () => {
      timeout = null;

      isUpdating.value = true;
      try {
        await fetch(`http://${url.hostname}:8000/api/shock`, {
          method: "POST",
          body: JSON.stringify({ ...shockState.value }),
          headers: {
            "Content-Type": "application/json",
          },
        });
      } catch (e) {
        console.error(e);
      }

      isUpdating.value = false;
    }, 300);
  }
);

async function toggleShocking() {
  shockState.value.state = !shockState.value.state;
}

onMounted(() => {
  if (remoteState.data.value) shockState.value = { ...remoteState.data.value };
});
</script>

<template>
  <div class="w-full h-full flex flex-col !bg-base-100 p-10 px-[20%]">
    <div>
      Shock Voltage: {{ Math.round((shockState.voltage || 0) * 100) }} %
    </div>
    <q-slider
      v-model="shockState.voltage"
      :min="0"
      :max="1"
      :step="0.05"
      class="mb-4"
    />

    <div>Shock Frequency: {{ shockState.frequency }} Hz</div>
    <q-slider
      v-model="shockState.frequency"
      :min="0"
      :max="500"
      :step="1"
      class="mb-4"
    />

    <div>Shock Duty: {{ Math.round((shockState.dutyCycle || 0) * 100) }} %</div>
    <q-slider
      v-model="shockState.dutyCycle"
      :min="0"
      :max="1"
      :step="0.1"
      class="mb-4"
    />

    <q-btn
      v-if="!shockState.state"
      class="!bg-primary !text-primary-content mb-8"
      @click="toggleShocking"
    >
      <icon name="mdi:electricity" size="20" /> Enable Shock
    </q-btn>
    <q-btn
      v-else
      class="!bg-primary !text-primary-content mb-8"
      @click="toggleShocking"
    >
      Disable Shock
    </q-btn>

    <q-linear-progress v-if="isUpdating" query />
  </div>
</template>
