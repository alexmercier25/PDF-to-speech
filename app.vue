<template>
  <div class="mx-4 md:mx-8">
    <h1>PDF Text to Speech</h1>
    <!-- <FileUpload /> -->
    <div class="w-full"><Textarea class="w-full" v-model="text" /></div>
    <Button label="Speak" @click="speak" />
  </div>
</template>

<script setup>
import "primevue/resources/themes/aura-light-green/theme.css";

const text = ref("");

const speak = async () => {
  const { data, pending } = await $fetch("/api/speak", {
    method: "POST",
    body: {
      text: text.value
    }
  });
};
</script>
