---
title: Offline Document Ingestion & AI Note Synthesizer
category: Local AI & Document Processing
doc-status: Planned
priority: P1
created: 2026-10-28
target_subjects:
  - TAX
  - RFBT
  - AUD
  - FAR
  - AFAR
  - MAS
---

# Offline Document Ingestion & AI Note Synthesizer

## 1. Overview & Problem Statement
CPALE reviewees are constantly bombarded with physical handouts, photocopied reviewer notes, BIR Revenue Regulations / Circulars (RMCs), and newly signed tax/commercial laws (e.g., EOPT Act, CREATE Act). Manually transcribing physical pages into digital flashcards and structured study summaries is slow and tedious.

The **Offline Document Ingestion & AI Note Synthesizer** allows a student to snap a photo of a textbook page or upload a local PDF, and have the app convert it into clean, structured Markdown study guides and active-recall flashcards—**completely offline, with zero cloud dependency and zero cloud token fees**.

---

## 2. The 2-Stage Local AI Processing Pipeline

```
[ User Uploads PDF or Snaps Photo of Tax Law / Textbook ]
                             │
                             ▼
 ┌─────────────────────────────────────────────────────────┐
 │ Stage 1: Local On-Device OCR Engine                     │
 │  - Google ML Kit / MediaPipe Text Recognition (Android) │
 │  - Apple Vision Kit (iOS)                               │
 │  - Extracts raw unformatted text in < 800ms offline     │
 └───────────────────────────┬─────────────────────────────┘
                             │ (Raw text string)
                             ▼
 ┌─────────────────────────────────────────────────────────┐
 │ Batching & Windowing Chunk Controller                   │
 │  - Splits text into manageable 500-800 word chunks      │
 │  - Preserves paragraph & section integrity              │
 └───────────────────────────┬─────────────────────────────┘
                             │
                             ▼
 ┌─────────────────────────────────────────────────────────┐
 │ Stage 2: Local AI Synthesis (Gemini Nano / Gemma 2B)   │
 │  - Cleans OCR scanning artifacts and misspellings        │
 │  - Extracts core formulas & statutory thresholds        │
 │  - Generates structured Markdown notes & Flashcards     │
 └───────────────────────────┬─────────────────────────────┘
                             │
                             ▼
[ Stored in Local Database (ObjectBox / Drift) & Added to Study Hub ]
```

---

## 3. Detailed Stage Breakdown

### Stage 1: The Local Text Extractor (OCR)
- **Library:** `google_mlkit_text_recognition` for Flutter/Android; native Vision framework for iOS.
- **Function:** Reads camera image buffer or PDF page bitmap directly in memory. Extracts alphanumeric characters, numbers, and tabular blocks locally in under a second with 0ms network latency.
- **Pre-filtering:** Strips useless header/footer boilerplate (e.g., page numbers, publisher disclaimers).

### Stage 2: The On-Device AI Structuring Engine
- **Engine:** Google Gemini Nano (via Android AICore) or MediaPipe LLM Inference (quantized Gemma 2B).
- **System Prompt:**
```markdown
You are an expert Philippine CPA Reviewer and Legal Scholar.
Analyze the following raw OCR-extracted text from an accounting or tax document.

[RAW EXTRACTED TEXT]:
{extractedTextChunk}

TASKS:
1. Clean up any OCR typos or broken line breaks.
2. Extract all core formulas, thresholds, tax rates, and legal exceptions into a structured Markdown summary.
3. Formulate 2-3 punchy, high-yield Active Recall Q&A Flashcards based strictly on the text.
4. Output format: Valid JSON containing "summaryMarkdown" and "flashcards" array.
```

---

## 4. UI/UX Workflow
1. **Source Selection:** Bottom sheet offering: `[ 📷 Snap Document Photo ]` or `[ 📁 Import Local PDF ]`.
2. **Page Preview & Crop:** Examinee can crop margins or select specific pages (e.g., Pages 3 to 5).
3. **Processing Progress State:** A clean, neo-brutalist progress modal:
   - *"Stage 1/2: Optical Character Recognition (Extracting text...)"* [Progress: 100%]
   - *"Stage 2/2: On-Device AI Synthesis (Gemini Nano running...)"* [Pulsing progress indicator]
4. **Interactive Output Review:**
   - Left Tab: Rendered Markdown study note with syntax-highlighted accounting rules.
   - Right Tab: Generated flashcard preview with one-tap *"Add to My Spaced Repetition Deck"*.

---

## 5. Engineering Constraints & Solutions

| Constraint | Real-World Impact | Architecture Solution |
| :--- | :--- | :--- |
| **Context Window Limit** | Gemini Nano / Gemma 2B cannot ingest a 300-page PDF at once. | **Page-by-Page Batching:** The app processes documents sequentially, page-by-page or in 800-word logical chunks, combining the output notes into a unified study document. |
| **Mobile Inference Latency** | On-device LLM takes 3–7 seconds per dense page on a mid-range phone. | **Background Queue with Notification:** If a user uploads 5 pages, processing is handed to a background Dart isolate with an unobtrusive progress notification. |
| **Thermal & Battery Throttling** | Sustained NPU/GPU inference can heat up the device and drain battery. | **Automatic Throttling:** Limit concurrent page synthesis to 1 page at a time with a 500ms cooldown pause between batch chunks. Pause processing if device battery $< 15\%$. |
| **Image Resolution & OCR Noise** | Blurry camera photos lead to garbage OCR text. | Pre-processing image filter (grayscale conversion + adaptive threshold contrast enhancement) via `image` package before passing to OCR. |

