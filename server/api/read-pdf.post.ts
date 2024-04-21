import fs from "fs";
import OpenAI from "openai";
import { put } from "@vercel/blob";

const openai = new OpenAI();

export default defineEventHandler(async (event) => {
  const file = await readMultipartFormData(event);
  try {
    const data = file[0].data;

    const buffer = Buffer.from(data);
    
    return {
      text: text,
    };
  } catch (error) {
    console.error("Error processing PDF data:", error);
    return {
      text: "Error: Unable to process PDF data",
    };
  }
});
