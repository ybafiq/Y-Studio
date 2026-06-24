# Aqavox Technical Documentation

Aqavox is an advanced, multi-modal artificial intelligence workspace designed inside a single, portable `index.html` layout. The application integrates natural language parsing with real-time generative computer vision models without requiring complex backend frameworks, node builds, configurations, or localized API tokens.

---

## 🏛️ System Architecture

Aqavox relies on an anonymous client-to-server connection layer mapped directly to open-source inference grids.

```
                                  +-----------------------+
                                  |   Aqavox Web Engine   |
                                  | (Native JS Runtime)   |
                                  +-----------+-----------+
                                              |
                     +------------------------+------------------------+
                     | (Asynchronous Context HTTP Fetch Pipeline)      |
                     v                                                 v
       +-------------+-------------+                     +-------------+-------------+
       |    Text Pipeline (LLM)    |                     |   Vision Pipeline (Diffusion) |
       |  text.pollinations.ai     |                     |  image.pollinations.ai    |
       +---------------------------+                     +---------------------------+

```

### Technical Dependencies

To preserve portability as a standalone execution file, dependencies are tracked exclusively over distributed Content Delivery Networks (CDNs):

* **`marked.js` Engine:** Intercepts incoming raw model responses on the fly, auto-compiling standard text patterns into formatted semantic blocks and structural grid data.

---

## 🛠️ Feature Breakdown & Implementations

### 1. Dual Execution Modes

The workspace transitions between standard text dialogue processing and distinct graphic generation turns using an internal state variable toggle (`isVisionModeActive`):

* **Text Conversational State:** Standard queries process text streams through memory contexts. If previous visual instances exist, the app translates binary artifacts into short context blocks (`[System Info: An image was generated previously matching description...]`) so text engines can modify them on the fly.
* **Vision Synthesis State:** Clicking the mode icon shifts the layout into **Vision Mode**. Submissions intercept raw string bounds directly, bypass conversational text layers, and route strings straight through chosen Diffusion neural pipelines.

### 2. State Mapping & Caching

Session continuity is preserved via the browser’s native `localStorage` layer. Five distinct state keys map configuration variables permanently to secure local memory:

| Caching Storage Key | Targeted Value Property Mapping | Default Fallback Value |
| --- | --- | --- |
| `ystudio_history` | Persistent JSON Conversation Array History | Baseline `system` payload array |
| `ystudio_chat_model` | Selected Core Language Model Endpoint | `openai` (GPT-4o routing parameter) |
| `ystudio_img_model` | Active Image Synthesis Neural Framework | `flux` (FLUX.1 Base Node) |
| `ystudio_width` | Horizontal Dimensional Variable (Pixels) | `1024` |
| `ystudio_height` | Vertical Dimensional Variable (Pixels) | `1024` |
| `ystudio_seed` | Static Token Anchor Value (Neural Reproducibility) | Empty string (Random Generation) |

---

## 📦 Neural Model Specifications

Aqavox abstracts multiple deep learning architectures into simple client selections:

### Text/Language Engines

* **GPT-4o (`openai`):** Optimized for multi-turn structural text formatting and intricate reasoning prompts.
* **Mistral Large (`mistral`):** Strictly sequences message blocks; provides fast structural text inference speeds.
* **Llama 3 (`llama`):** Meta’s open-source parameters; ideal for creative brainstorming and fluid, direct dialogue responses.

### Vision/Diffusion Frameworks

* **FLUX.1 Base (`flux`):** High-fidelity model. Features optimal composition tracking, strict adherence to dense prompt structures, and accurate spelling tracking inside generations.
* **FLUX Realism (`flux-realism`):** Fine-tuned layer that removes digital textures, adding realistic camera grain, focal blurring, and organic surface reflections.
* **FLUX Anime (`flux-anime`):** Highly stylized vector art weights; translates inputs into vivid illustrations, graphic novel structures, or stylized concepts.
* **SDXL-Turbo (`turbo`):** High-speed model. Uses single-step synthesis logic to stream down a complete image box in under a second.

---

## 🎨 Layout Design & Interface Styling

The structural engine utilizes modular, semantic styling layers engineered for smooth 60fps responsiveness on desktop viewports and mobile touchscreens:

```
+---------------------------------------------------------+
| [=] Header Bar                                          |
+--------------------+------------------------------------+
|                    |                                    |
|  [Sidebar Drawer]  |  [Main Chat Feed Panel]            |
|                    |                                    |
|   * Settings       |   * User Dialog Bubbles            |
|   * Asset Vault    |   * Response Tables & Markdowns    |
|     Thumbnails     |   * Visual Image Display Cards     |
|                    |     w/ Macro Tuning Pills          |
|                    |                                    |
|                    +------------------------------------+
|                    | [O] Input text box           [>]   |
+--------------------+------------------------------------+

```

### Component Details

* **Defensive Markdown Table Layouts:** Formats raw pipe characters into neat, modern tables with alternating dark-grey backgrounds (`#111214`), light borders (`--border-color`), and highlighted headers (`--y-accent`) for scannable data layouts.
* **The Asset Vault:** A tabbed sidebar panel that reads local conversation data arrays and rehydrates a gallery grid. Clicking a thumbnail auto-preps the user's text box for quick iterative edits.
* **In-Feed Tuning Modifiers:** Appends pill buttons (`📷 Photorealistic`, `🎨 Anime Style`, `🌆 Cyberpunk`, `✏️ Sketch`) directly below images. Clicking one grabs the original prompt string, injects the chosen style modifier, and auto-submits a new rendering query.
* **Gemini-Inspired Sidebar:** Uses hardware-accelerated CSS `transform` and flex layouts to dynamically handle window scaling. On screens below `768px`, the sidebar pulls smooth overlay focus, preventing layout compression or layout clipping.

---

## 🚀 Operations & Deployment

### Quick Execution

Because Aqavox relies entirely on browser runtimes, it has **zero deployment dependencies** (no `npm install`, no `package.json`, and no compilation tools).

1. Copy the source layout into a file named exactly `index.html`.
2. Double-click the file to open it in any browser, or host it with one click on static hosting layers like GitHub Pages, Netlify, or Vercel.
3. Use the **"Reset Workspace"** action button in the sidebar to flush previous browser cookies or state caches whenever you need a fresh workspace session.