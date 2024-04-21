<template>
  <div class="mx-4">
    <div v-for="(page, index) in pages" :key="index">
      <h2 class="flex align-items-center">
        Page {{ index + 1 }}
        <Button text @click="pages.splice(index, 1)">Delete</Button>
      </h2>
      <Textarea
        class="w-full"
        v-model="page.content"
        :rows="page.content.split(' ').length / 10 / 2"
        :disabled="loading"
      />
      <a target="_blank" :href="page.audioUrl" v-if="page.audioUrl">
        Listen to audio
      </a>
    </div>
    <div>
      <Checkbox
        v-model="shouldFixText"
        class="mt-4"
        binary
        input-id="fixText"
      /><label for="fixText" class="ml-2">Fix text using AI?</label>
    </div>
    <Button
      label="Add page"
      class="p-button-lg p-button-secondary mt-4"
      @click="addPage"
      :loading="loading"
    />
    <Button
      label="Clear pages"
      class="p-button-lg mt-4 ml-4 p-button-secondary"
      @click="pages = []"
      :loading="loading"
    />
    <Button
      label="Generate audio"
      class="p-button-lg mt-4 ml-4"
      @click="generate"
      :loading="loading"
    />
  </div>
</template>

<script setup lang="ts">
const loading = ref(false);
const pages = ref([]);
const shouldFixText = ref(true);
const appConfig = useAppConfig();

const save = () => {
  localStorage.setItem("pages", JSON.stringify(pages.value));
};

const addPage = () => {
  pages.value.push({
    content: "",
  });
};

// onMounted(() => {
//   const savedPages = localStorage.getItem("pages");
//   if (savedPages) {
//     pages.value = JSON.parse(savedPages);
//   }
// });

//watch(pages, save, { deep: true });

const generate = async () => {
  console.log("Generating...");
  loading.value = true;

  // Iterate through each page one by one
  for (let index = 0; index < pages.value.length; index++) {
    const page = pages.value[index];

    if (shouldFixText.value) {
      console.log(`Fixing text for page #${index + 1}`);

      const resp = await useFetch("http://127.0.0.1:5000" + "/fix-text", {
        method: "POST",
        body: JSON.stringify({
          text: [page.content],
        }),
        headers: {
          "Content-Type": "application/json",
        },
      });

      const fixedText = resp.data.value.responses[0];
      pages.value[index].content = fixedText;
    }

    console.log(`Generating audio for page #${index + 1}`);

    const resp = await useFetch("/api/speak", {
      method: "POST",
      body: JSON.stringify({  // Ensure the body is correctly stringified
        text: page.content,
        fileName: `page-${index + 1}`,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    pages.value[index].audioUrl = resp.data.value?.downloadUrl;

    // Download the audio for the current page
    const link = document.createElement("a");
    link.href = page.audioUrl;
    link.download = `page-${index + 1}.mp3`;
    document.body.appendChild(link); // Append link to the body to ensure visibility
    link.click();
    document.body.removeChild(link); // Remove link after clicking
  }

  loading.value = false;
  console.log("Generation complete.");
};

</script>
