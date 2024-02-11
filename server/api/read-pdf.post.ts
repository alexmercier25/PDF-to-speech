import fs from "fs";
import OpenAI from "openai";
import { put } from "@vercel/blob";

const openai = new OpenAI();

export default defineEventHandler(async (event) => {
  const file = await readMultipartFormData(event);
  try {
    const data = file[0].data;

    const buffer = Buffer.from(data);
    await fs.promises.writeFile("file.png", buffer);

    const resp = await put("file.png", buffer, {
      access: "public",
    });

    const visionResp = await openai.chat.completions.create({
      model: "gpt-4-vision-preview",
      messages: [
        {
          role: "user",
          content: [
            { type: "text", text: "Donne moi tout le texte de cette image, le plus précis possible." },
            {
              type: "image_url",
              image_url: {
                url: resp.url,
              },
            },
          ],
        },
      ],
    });

    const text = visionResp.choices[0]
    console.log(text)
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
