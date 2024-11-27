<script setup lang="ts">
type ShockState = {
  voltage?: number;
  state?: boolean;
  frequency?: number;
  dutyCycle?: number;
};

const shockState = ref<ShockState>({});
const remoteState = useAsyncData(async () => {
  const response = await fetch(
    `http://${window.location.host}:8000/api/shock`,
    {
      method: "GET",
    }
  );
  const data = await response.json();
  return data as ShockState;
});
watch(
  () => remoteState.data.value,
  (data) => (shockState.value = { ...data })
);

let timeout: NodeJS.Timeout | null = null;
watch(
  () => ({ ...shockState.value }),
  () => {
    console.log("WTR");
    if (timeout) return;
    timeout = setTimeout(() => {
      timeout = null;
      fetch(`http://${window.location.host}:8000/api/shock`, {
        method: "POST",
        body: JSON.stringify({ ...shockState.value }),
        headers: {
          "Content-Type": "application/json",
        },
      });
    }, 200);
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
  <div class="w-full h-full flex flex-col p-10 !bg-base-100">
    <div class="flex flex-col content-center">
      <div>
        Shock Voltage: {{ Math.round((shockState.voltage || 0) * 100) }} %
      </div>
      <q-slider
        v-model="shockState.voltage"
        :min="0"
        :max="1"
        :step="0.05"
        class="mb-4 max-w-80"
      />
    </div>
    <div class="flex flex-col content-center">
      <div>Shock Frequency: {{ shockState.frequency }} Hz</div>
      <q-slider
        v-model="shockState.frequency"
        :min="0"
        :max="100000"
        :step="1"
        class="mb-4 max-w-80"
      />
    </div>
    <div class="flex flex-col content-center">
      <div>
        Shock Duty: {{ Math.round((shockState.dutyCycle || 0) * 100) }} %
      </div>
      <q-slider
        v-model="shockState.dutyCycle"
        :min="0"
        :max="1"
        :step="0.1"
        class="mb-4 max-w-80"
      />
    </div>

    <div class="flex flex-col content-center">
      <q-btn
        v-if="shockState.state"
        class="!bg-primary !text-primary-content"
        @click="toggleShocking"
      >
        <icon name="mdi:electricity" size="20" /> Enable Shock
      </q-btn>
      <q-btn
        v-else
        class="!bg-primary !text-primary-content"
        @click="toggleShocking"
      >
        Disable Shock
      </q-btn>
    </div>
  </div>
</template>
