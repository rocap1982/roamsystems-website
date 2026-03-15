import fs from "fs";
import path from "path";

const API_KEY = process.env.GOOGLE_API_KEY;
if (!API_KEY) {
  console.error("Error: GOOGLE_API_KEY environment variable is not set.");
  process.exit(1);
}

const dateStamp = new Date().toISOString().slice(0, 10);
const batchNum = (() => {
  let n = 2;
  while (fs.existsSync(path.join("Gemini generated imges", `batch-${dateStamp}-v${n}`))) n++;
  return n;
})();
const OUTPUT_DIR = path.join("Gemini generated imges", `batch-${dateStamp}-v${batchNum}`);
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

// Reference images — prioritise the accurate generated images + best originals
const refImages = [
  // ACCURATE generated images from batch 1 (these got the layout RIGHT)
  path.join("Gemini generated imges", "batch-2026-03-13", "08-full-system-kitchen-coffee.png"),
  path.join("Gemini generated imges", "batch-2026-03-13", "07-detail-frame-closeup.png"),
  // Real product photos
  path.join("Gemini generated imges", "ebay-reference-photos", "01-interior-lifestyle-upholstered.jpg"),
  path.join("Gemini generated imges", "ebay-reference-photos", "02-cad-positions-diagram.jpg"),
  path.join("Gemini generated imges", "ebay-reference-photos", "03-workshop-frame-front.jpg"),
  // CAD renders
  path.join("Gemini generated imges", "sample drawings and photos for gemini", "1.PNG"),
  path.join("Gemini generated imges", "sample drawings and photos for gemini", "5.PNG"),
];

function loadImagePart(filePath) {
  const data = fs.readFileSync(filePath);
  const ext = path.extname(filePath).toLowerCase();
  const mimeType = ext === ".png" ? "image/png" : "image/jpeg";
  return {
    inlineData: {
      data: data.toString("base64"),
      mimeType,
    },
  };
}

// Much more specific layout description anchored to image 8's correct output
const PRODUCT_FORM = `CRITICAL LAYOUT INSTRUCTIONS — You MUST reproduce the EXACT interior layout shown in the first two reference images (the generated interior shot and the frame render). These are ACCURATE representations of the product. All other reference images provide additional form detail.

THE INTERIOR LAYOUT (copy this EXACTLY):
- This is a VW Transporter T6 campervan rear interior
- RIGHT SIDE (driver side): A LONG bench seat runs the full length of the right wall, from the rear doors to roughly the sliding door area. It has GREY side panels and MUSTARD/TAN quilted diamond-pattern seat cushions and backrest cushions
- REAR WALL: A SHORTER bench seat spans the rear wall, same grey/mustard upholstery, connecting to the right-side bench to form the U-shape. The backrest is a TALL FIXED UPRIGHT PANEL behind this rear bench — it does NOT fold or move
- LEFT SIDE (passenger side): A KITCHEN POD with GREY cabinets, OAK/WOOD worktop, and LED under-cabinet strip lighting. The kitchen has drawers and cupboard doors. Above the kitchen is an overhead storage locker
- FLOOR: Light oak/wood effect flooring throughout
- CEILING: BLACK headliner with WHITE LED strip lights running lengthwise
- WINDOWS: BLUE pleated concertina blinds on all rear and side windows
- The U-shape seating creates an open floor area between the benches and kitchen
- Storage boxes are integrated at the front corners of the U-shape frame, with cup holders and USB points
- Triangular steel bracing visible on the side panels of the frame
- A pull-out drawer underneath with a red battery box area

FRAME DETAILS:
- Textured black powder-coated steel tube frame
- Cross-member slat structure on the bed platform
- Precision laser-cut construction

BED MODE CONVERSION (IMPORTANT — the backrest does NOT fold):
- The backrest STAYS UPRIGHT at all times — it never folds or moves
- Instead, a HORIZONTAL PULL-OUT SECTION slides forward from the base of the rear bench/backrest area
- This pull-out section bridges the open floor gap between the benches
- Cushion boards then lay flat across the bench seats AND the pulled-out section, creating a continuous flat sleeping surface approximately 170cm x 158cm
- In bed mode the backrest is still visible standing upright behind the bed surface

DO NOT change the layout, proportions, colours, or arrangement. The product must look IDENTICAL to the reference images.`;

const prompts = [
  // 1. Hero lifestyle — rear doors open, bed mode, coastal
  `${PRODUCT_FORM}

Generate a photorealistic image of this EXACT interior in BED MODE: The VW Transporter T6 is parked at a scenic UK coastal cliff top. The rear barn doors are wide open showing the coastline and a golden hour sunset. Inside, the U-shape system is converted to bed mode — the horizontal pull-out section has slid forward from the rear bench, and cushion boards lay flat across the entire surface creating a continuous bed. The tall backrest panel remains UPRIGHT behind the bed (it does NOT fold). The sleeping area is dressed with a cozy white duvet, pillows, and a teal throw blanket. The LED ceiling strips provide warm light. The kitchen pod with oak worktop is visible on the left side. Shot from directly behind the van looking in. Premium lifestyle magazine quality.`,

  // 2. Seating mode — breakfast scene, campsite morning
  `${PRODUCT_FORM}

Generate a photorealistic image of this EXACT interior in SEATING MODE: Shot from the sliding side door looking into the VW T6 interior. The long right-side bench and rear bench are visible with the grey/mustard upholstered cushions. A small wooden table is deployed from the wall between the benches. Two coffee cups, croissants, and a small breakfast spread sit on the table. The kitchen pod with oak worktop is on the far left. Morning sunlight streams through the windows (blue pleated blinds partially open). Green campsite visible outside. The ceiling LED strips are on. Warm, inviting, premium feel.`,

  // 3. Bed mode — forest dawn, from inside looking out
  `${PRODUCT_FORM}

Generate a photorealistic image of this EXACT interior in BED MODE: Viewpoint is from INSIDE the van near the front, looking towards the open rear barn doors. The horizontal pull-out section has extended forward and cushion boards lay flat across the benches and pull-out, creating a continuous bed surface. The tall backrest remains UPRIGHT behind the bed. White duvet and beige/cream pillows on the bed. The kitchen pod with oak worktop is on the left. The open rear doors reveal a misty pine forest at dawn with soft golden light filtering through trees. LED strip lights glow warmly on the black ceiling. Blue pleated blinds on side windows. Atmospheric, dreamy, lifestyle photography.`,

  // 4. Rear view — seating mode, showing full U-shape from outside
  `${PRODUCT_FORM}

Generate a photorealistic image of this EXACT interior in SEATING MODE: The VW T6 rear barn doors are open. Camera is positioned outside the van looking straight in at the rear. The full U-shape layout is visible — the long bench along the right wall and the shorter bench across the rear, both with grey sides and mustard quilted cushions. The kitchen pod with oak worktop and grey cabinets is on the left. Overhead locker above kitchen. LED strips on ceiling. The van is parked at a scenic campsite with mountains in the background. Bright daylight. Clean, architectural product photography.`,

  // 5. Side door — person enjoying the interior, lake view
  `${PRODUCT_FORM}

Generate a photorealistic image of this EXACT interior in SEATING MODE: The VW T6 sliding side door is open. A woman sits on the long right-side bench reading a book, legs stretched along the bench. The grey/mustard cushions are clearly visible. The kitchen pod with oak worktop is across from her on the left side. A coffee cup sits on the kitchen worktop. Through the open sliding door and windows: a mountain lake at golden hour. LED ceiling strips on. Blue pleated blinds on rear windows. Shot from outside through the sliding door. Adventure lifestyle photography.`,

  // 6. Evening camp — bed mode with warm glow
  `${PRODUCT_FORM}

Generate a photorealistic image of this EXACT interior in BED MODE: The VW T6 is at a campsite during blue hour (just after sunset). Rear barn doors open. Inside, the horizontal pull-out section has extended forward creating a flat bed surface with the backrest remaining UPRIGHT behind it. The bed is dressed with bedding and pillows. The LED strip lights on the ceiling cast a warm glow inside. The kitchen pod with oak worktop is on the left, a small lamp on the counter. Outside the rear doors: two folding camp chairs and a small table with a camping lantern. Dark blue sky with some stars. The warm interior contrasts beautifully against the cool blue twilight outside. Lifestyle adventure photography.`,

  // 7. Detail shot — frame quality close-up (KEEP — this was accurate)
  `${PRODUCT_FORM}

Generate a photorealistic close-up detail image: Focus on the Roam Systems U-shape frame's build quality. Show the textured black powder-coated steel frame, the precision laser-cut construction, the integrated cup holders in the storage box, and the cross-member slat structure of the bed platform. The backrest is in the upright position. Clean studio-style lighting highlighting the metalwork quality. Shot at a 45-degree angle to show depth and construction detail. Premium product photography style with shallow depth of field.`,

  // 8. Full system with kitchen pod — morning coffee (KEEP — this was accurate)
  `${PRODUCT_FORM}

Generate a photorealistic image: Interior of a VW Transporter T6 campervan showing the COMPLETE Roam Systems setup. The U-shape seating system with grey/mustard upholstered cushions in SEATING MODE. A kitchen pod on the left side with an oak worktop — a steaming coffee cup and a French press on the counter. An aluminium overhead locker above the kitchen. Morning sunlight through the windows. Shot from the rear of the van looking forward. The interior looks premium, tidy, and well-designed. Lifestyle photography quality.`,

  // 9. Tailgate camping — outdoor lifestyle with interior visible
  `${PRODUCT_FORM}

Generate a photorealistic image: VW Transporter T6 parked on green grass at a UK countryside campsite. Rear barn doors wide open. The EXACT interior is visible — the U-shape seating with grey/mustard cushions in SEATING MODE, kitchen pod with oak worktop on the left, LED ceiling strips on. Outside the rear of the van: two black folding camp chairs, a small wooden camping table with mugs and a bottle of wine, a camping lantern. Rolling green hills and trees in the background. Late afternoon golden light. The scene shows the van as a comfortable adventure basecamp.`,

  // 10. Conversion showcase — seating vs bed split
  `${PRODUCT_FORM}

Generate a photorealistic split-image showing the EXACT same interior in TWO configurations side by side:
LEFT HALF — SEATING MODE: The U-shape with grey/mustard cushions, backrest upright, showing the long right bench and rear bench. Kitchen pod visible on left. A small table deployed. LED ceiling lights on.
RIGHT HALF — BED/SLEEPING MODE: The same interior but with the horizontal pull-out section extended forward from the rear bench, cushion boards laid flat across the entire surface creating a continuous bed. The backrest remains upright behind the bed. White duvet and pillows on the bed. Kitchen pod still visible on left. LED ceiling lights on.
Both halves show the same VW T6 interior from the same rear-looking-forward angle. Clean dividing line between the two halves. Labels "Seating Position" and "Sleeping Position" at the bottom. Bright, even lighting. Product demonstration style.`,
];

async function generateImage(prompt, index) {
  const label = prompt.split("\n\n")[1]?.slice(0, 80) || `Prompt ${index + 1}`;
  console.log(`\n[${index + 1}/${prompts.length}] ${label}...`);

  const loadedImages = refImages
    .filter((f) => fs.existsSync(f))
    .map(loadImagePart);

  console.log(`  Reference images loaded: ${loadedImages.length}`);

  // Primary: gemini-2.5-flash-image (native image generation)
  // Fallback: gemini-3-pro-image-preview
  const models = ["gemini-2.5-flash-image", "gemini-3-pro-image-preview"];

  const body = {
    contents: [
      {
        role: "user",
        parts: [...loadedImages, { text: prompt }],
      },
    ],
    generationConfig: {
      responseModalities: ["TEXT", "IMAGE"],
    },
  };

  try {
    let data = null;

    for (const model of models) {
      const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${API_KEY}`;
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (response.ok) {
        data = await response.json();
        console.log(`  Model: ${model}`);
        break;
      } else {
        const errText = await response.text();
        console.error(`  ${model} error (${response.status}): ${errText.slice(0, 300)}`);
      }
    }

    if (!data) {
      console.error("  All models failed.");
      return;
    }

    await processResponse(data, index);
  } catch (err) {
    console.error(`  Error: ${err.message}`);
  }
}

async function processResponse(data, index) {
  let imageCount = 0;

  if (data.candidates?.[0]?.content?.parts) {
    for (const part of data.candidates[0].content.parts) {
      if (part.inlineData) {
        const mimeType = part.inlineData.mimeType || "image/png";
        const ext = mimeType.includes("png") ? "png" : "jpg";
        const promptTag = [
          "hero-coastal-bed",
          "seating-breakfast-campsite",
          "bed-forest-dawn",
          "rear-view-seating-mountains",
          "side-door-lake-reading",
          "evening-camp-blue-hour",
          "detail-frame-closeup",
          "full-system-kitchen-coffee",
          "tailgate-camping-setup",
          "conversion-showcase",
        ][index] || `scene-${index + 1}`;

        const filename = `${String(index + 1).padStart(2, "0")}-${promptTag}.${ext}`;
        const outPath = path.join(OUTPUT_DIR, filename);
        const buf = Buffer.from(part.inlineData.data, "base64");
        fs.writeFileSync(outPath, buf);
        console.log(`  Saved: ${outPath} (${(buf.length / 1024).toFixed(0)} KB)`);
        imageCount++;
      }
      if (part.text) {
        console.log(`  Gemini note: ${part.text.slice(0, 200)}`);
      }
    }
  }

  if (imageCount === 0) {
    console.log("  No images in response. Response preview:");
    console.log(JSON.stringify(data, null, 2).slice(0, 1000));
  }
}

async function main() {
  console.log("=== Roam Systems U-Shape Image Generator v2 ===");
  console.log(`Output: ${OUTPUT_DIR}`);
  console.log(`Date: ${dateStamp}`);
  console.log(`Prompts: ${prompts.length}`);

  const found = refImages.filter((f) => fs.existsSync(f));
  console.log(`\nReference images: ${found.length}/${refImages.length} found`);
  found.forEach((f) => console.log(`  - ${path.basename(f)}`));

  if (found.length < 4) {
    console.error("\nNot enough reference images found. Aborting.");
    process.exit(1);
  }

  for (let i = 0; i < prompts.length; i++) {
    await generateImage(prompts[i], i);
    // Small delay between requests to avoid rate limiting
    if (i < prompts.length - 1) {
      console.log("  Waiting 3s before next request...");
      await new Promise((r) => setTimeout(r, 3000));
    }
  }

  console.log(`\nDone! Generated images in: ${OUTPUT_DIR}`);
  console.log("Review the output and pick your favourites.");
}

main();
