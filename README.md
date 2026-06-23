# Y Studio — Chat & Vision AI 🌌

A clean, responsive, single-file AI studio inspired by the Gemini interface. This web application provides a unified chat experience that seamlessly toggles between natural language conversation and high-fidelity image generation—**zero API keys, sign-ups, or external machine learning dependencies required.**

Built on top of the free public **Pollinations.ai** text and image generation engines.

---

## ✨ Features

* **Intelligent Intent Routing:** Automatically detects whether you want to chat normally (e.g., *"Write a poem"*) or create art (e.g., *"Draw a cyberpunk city"*).
* **Engine & Model Control:** Fine-tune image generation on the fly using **FLUX.1** (High Fidelity) or **SDXL-Turbo** (Fast Render), customize exact pixel aspect ratios, or pin down a specific generation seed.
* **Fluid Conversations:** Contextual text chat powered by state-of-the-art LLMs (with choice toggles for GPT-4o or Mistral Large) with formatting optimizations.
* **Inline Gemini Aesthetics:** Immersive dark mode, custom animated shimmers that match your chosen image aspect ratio during generation, and contextual message bubbles.
* **One-Click Assets:** Inspect, open, or download generated image binary blobs natively directly inside the browser feed.

---

## 🛠️ Tech Stack & Architecture

This project is built purely with standard web technologies to match the simplicity of a single standalone execution layer:

* **HTML5 & CSS3:** Semantic elements, responsive flexbox layout, and custom keyframe loading animations.
* **Vanilla JavaScript (ES6+):** Native `fetch` API stream processing, dynamic `Blob` URL generation for secure local downloads, and state history keeping.
* **Backends:** Powered by `text.pollinations.ai` and `image.pollinations.ai`.

---

## 🚀 Quick Start

Because this app has zero builds or dependencies, running it locally is incredibly simple:

1. Clone or download this repository.
2. Open the `index.html` file directly in any modern desktop or mobile web browser.
3. Start creating!