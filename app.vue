<template>
  <div class="mx-4 md:mx-8">
    <h1>PDF Text to Speech</h1>
    <div>
      <label><h2>Choose a PDF file</h2></label>
      <FileUpload
        url="/api/read-pdf"
        :disabled="loading"
        name="pdfFile"
        accept="image/*"
      />
    </div>
    <h2>or</h2>
    <div class="w-full mb-4">
      <Textarea
        :disabled="loading"
        placeholder="Enter text here"
        class="w-full"
        v-model="text"
      />
    </div>
    <Button
      class="p-button-lg"
      :loading="loading"
      :label="status"
      @click="speak"
    />

    <div v-if="currentFileUrl">
      <h2>Generated audio</h2>
      <audio :src="currentFileUrl" controls></audio>
    </div>
  </div>
</template>

<script setup>
import "primevue/resources/themes/aura-light-green/theme.css";

const text = ref("");
const loading = ref(false);

const status = ref("Generate");
const currentFileUrl = ref("");

// const uploadFile = async (file) => {
//   loading.value = true;
//   status.value = "Uploading file...";

//   const formData = new FormData();
//   formData.append("pdfFile", file.files[0]);

//   const resp = await $fetch("/api/read-pdf", {
//     method: "POST",
//     body: file.files[0],
//   });

//   text.value = resp.text;
// };

const speak = async () => {
  loading.value = true;

  status.value = "Generating audio...";
  const resp = await $fetch("/api/speak", {
    method: "POST",
    body: {
      text: text.value,
    },
  });
  loading.value = false;

  currentFileUrl.value = resp.url;
};
</script>
