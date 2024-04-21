import fs from "fs";
import path from "path";

export default defineEventHandler(async (event): Promise<any> => {
  const body = await readBody(event);

  const text = body.text;

  // https://platform.openai.com/docs/guides/text-generation/managing-tokens

  const resp = await $fetch(process.env.PDFTOTEXT_API + "/fix-text", {
    method: "POST",
    body: {
      text: text,
    },
    headers: {
      "Content-Type": "application/json",
    },
  });

  console.log("resp", resp);

  return {
    resp,
  };
});
