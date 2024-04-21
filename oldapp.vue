<template>
  <div class="mx-4 md:mx-8">
    <h1>PDF Text to Speech</h1>
    <div>
      <label><h2>Choose a PDF file</h2></label>
      <input
        type="file"
        :disabled="loading"
        name="pdfFile"
        accept="application/pdf"
        @change="uploadFile"
      />
    </div>

    <!-- <h2>Generated text</h2>
    <div class="w-full mb-4">
      <Textarea
        :disabled="loading"
        placeholder="Enter text here"
        class="w-full"
        v-model="text"
      />
    </div> -->
    <Button
      class="p-button-lg mt-4"
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

const appConfig = useAppConfig();

const text = ref("");
const loading = ref(false);

const status = ref("Generate");
const currentFileUrl = ref("");

const uploadFile = async (event) => {
  loading.value = true;
  status.value = "Uploading and extracting text from file...";

  const formData = new FormData();
  formData.append("pdfFile", event.target.files[0]);

  const resp = await $fetch(appConfig.pdfToTextApi + "/upload-pdf", {
    method: "POST",
    body: formData,
  });

  text.value = resp.text;
  loading.value = false;

  fixText()
};

const fixText = async () => {
  loading.value = true;
  status.value = "Fixing text...";

  const resp = await $fetch("/api/fixText", {
    method: "POST",
    body: {
      text: text.value,
    },
  });

  text.value = resp.resp.responses
  loading.value = false;

  speak();
}

const speak = async () => {
  loading.value = true;

  status.value = "Generating audio...";
  console.log(text.value)
  const resp = await $fetch("/api/speak", {
    method: "POST",
    body: {
      text: text.value[1]
    },
  });
  loading.value = false;

  currentFileUrl.value = resp.url;
};
</script>
