import fs from "fs";
import path from "path";
import OpenAI from "openai";
import { put } from "@vercel/blob";

const openai = new OpenAI();

const speechFile = path.resolve("speech.mp3");

export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  const mp3 = await openai.audio.speech.create({
    model: "tts-1",
    voice: "alloy",
    input: body.text,
  });
  console.log(speechFile);
  const buffer = Buffer.from(await mp3.arrayBuffer());
  await fs.promises.writeFile(speechFile, buffer);

  const resp = await put("speech.mp3", buffer, {
    access: "public",
  });
    console.log(resp);

  return {
    ...resp,
  }
});
