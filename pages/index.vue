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
    <div class="flex mt-4 gap-2" v-if="pageItems.length > 0">
      <div>Current page: 
        <span class="font-bold">{{ currentPage + 1 }}</span>
      </div>
      <Menu :model="pageItems" />
      <div>
        <Textarea class="mt-0 block w-full" :disabled="loading" v-model="pageItems[currentPage].text">
        </Textarea>
        <Button
          class="p-button-secondary mr-2"
          :loading="loading"
          label="Put selected text in the previous page"
          @click="putSelectedTextInPreviousPage"
        />
        <Button
          class="p-button-secondary mr-2"
          :loading="loading"
          label="Put selected text in the next page"
          @click="putSelectedTextInNextPage"
        />
        <Button
          class="p-button-outlined mt-4"
          :loading="loading"
          label="Text is not correct? Click here to fix it."
          @click="fixText"
        />
        <Button class="ml-2" :loading="loading" label="Listen" @click="speak" />
      </div>
    </div>
    <div
      class="flex gap-2 mt-4 align-items-center justify-content-center"
      v-if="loading"
    >
      <div>
        <ProgressSpinner />
      </div>
      <div class="text-xl font-bold">{{ status }}</div>
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
    <!-- <Button
      class="p-button-lg mt-4"
      :loading="loading"
      :label="status"
      @click="speak"
    />

    <div v-if="currentFileUrl">
      <h2>Generated audio</h2>
      <audio :src="currentFileUrl" controls></audio>
    </div> -->
  </div>
</template>

<script setup>
const appConfig = useAppConfig();
const text = ref("");
const loading = ref(false);

const status = ref("");
const currentFileUrl = ref("");

// const pageItems = ref([
//   {
//     label: "Page 1",
//     icon: "pi pi-file",
//     command: () => {
//       text.value = "Page 1 text";
//       //speak();
//     },
//   },
//   {
//     label: "Page 2",
//     icon: "pi pi-file",
//     command: () => {
//       text.value = "Page 2 text";
//       //speak();
//     },
//   },
//   {
//     label: "Page 3",
//     icon: "pi pi-file",
//     command: () => {
//       text.value = "Page 3 text";
//       //speak();
//     },
//   },
// ]);
const pageItems = ref([]);
const currentPage = ref(0);

const uploadFile = async (event) => {
  loading.value = true;
  status.value = "Uploading file...";

  const formData = new FormData();
  formData.append("pdfFile", event.target.files[0]);

  const resp = await $fetch(appConfig.pdfToTextApi + "/upload-pdf", {
    method: "POST",
    body: formData,
  });

  loading.value = false;
  resp.pages.forEach((page, index) => {
    pageItems.value.push({
      label: `Page ${index + 1}`,
      icon: "pi pi-file",
      command: () => {
        currentPage.value = index;
        //speak();
      },
      text: page,
    });
  });
};

const fixText = async () => {
  loading.value = true;
  status.value = "Fixing text...";

  const resp = await $fetch("/api/fixText", {
    method: "POST",
    body: {
      text: [pageItems.value[currentPage.value].text],
    },
  });

  pageItems.value[currentPage.value].text = resp.resp.responses[0];
  loading.value = false;
};

const speak = async () => {
  loading.value = true;

  status.value = "Generating audio...";
  console.log(text.value);
  const resp = await $fetch("/api/speak", {
    method: "POST",
    body: {
      text: pageItems.value[currentPage.value].text,
    },
  });
  loading.value = false;

  currentFileUrl.value = resp.url;
};

const getSelectedText = () => {
  const selection = window.getSelection();
  return selection.toString();
};

const putSelectedTextInPreviousPage = () => {
  let selectedText = getSelectedText();
  if (selectedText) {
    pageItems.value[currentPage.value - 1].text += selectedText;
  }

  // remove selected text from current page
  // const currentText = pageItems.value[currentPage.value].text;
  // const newText = currentText.replace(selectedText, "");

  // pageItems.value[currentPage.value].text = newText;
};

const putSelectedTextInNextPage = () => {
  let selectedText = getSelectedText();
  if (selectedText) {
    selectedText += pageItems.value[currentPage.value + 1].text;
  }
  // remove selected text from current page
  // const currentText = pageItems.value[currentPage.value].text;
  // const newText = currentText.replace(selectedText, "");

  // pageItems.value[currentPage.value].text = newText;
};
</script>
